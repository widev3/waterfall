import io
import datetime
import pandas as pd
from io import StringIO
from dateutil import parser


class IQ(object):

    @staticmethod
    def read(filename: str):
        def split_file_by_empty_lines(file):
            with open(file, "r") as file:
                lines = file.readlines()
                chunks = []
                current_chunk = []

                for line in lines:
                    if line.strip() == "":
                        if current_chunk:
                            chunks.append(current_chunk)
                            current_chunk = []
                    else:
                        current_chunk.append(line)

                if current_chunk:
                    chunks.append(current_chunk)

            return chunks

        def properties(chunk):
            pd_data = pd.read_csv(io.StringIO("".join(chunk)), sep=",")
            return pd_data.set_index("Name").to_dict(orient="index")

        def frequencies(chunk):
            pd_data = pd.read_csv(io.StringIO("".join(chunk)), sep=",")
            return list(pd_data["Frequency [Hz]"])

        def spectrogram(chunk):
            def parse_dt(d):
                try:
                    return parser.parse(d, dayfirst=True).timestamp()
                except:
                    try:
                        return parser.parse(d, dayfirst=False).timestamp()
                    except:
                        try:
                            return datetime.datetime.strptime(
                                d, "%H:%M:%S:%f"
                            ).timestamp()
                        except:
                            return None

            csv_data = "\n".join(chunk)
            df = pd.read_csv(StringIO(csv_data), header=[0, 1], low_memory=False)
            df = df.dropna(axis=1, subset=[df.index[-1]], how="any")
            magnitude = df.copy()
            magnitude.columns = range(magnitude.shape[1])
            magnitude = magnitude.drop(columns=0)
            magnitude.columns = range(magnitude.shape[1])
            magnitude = magnitude.drop(index=0)
            magnitude.index -= 1
            magnitude = magnitude.astype(float).values.tolist()
            magnitude = list(map(list, zip(*magnitude)))

            abs_ts, rel_ts = zip(*df.columns)
            abs_ts = list(filter(lambda x: x, list(map(lambda x: parse_dt(x), abs_ts))))
            rel_ts = list(filter(lambda x: x, list(map(lambda x: parse_dt(x), rel_ts))))
            rel_ts = list(map(lambda x: rel_ts[0] - x, rel_ts))

            um = {}
            um["time"] = "ms"
            um["frequency"] = "Hz"
            um["magnitude"] = "dBm"

            return rel_ts, abs_ts, magnitude, um

        chunks = split_file_by_empty_lines(filename)
        return properties(chunks[0]), frequencies(chunks[1]), spectrogram(chunks[2])
