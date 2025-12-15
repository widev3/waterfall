import io
import datetime
import pandas as pd
from io import StringIO
from dateutil import parser


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

    def read_csv_from_spm(chunks):
        def properties(chunk):
            df = pd.read_csv(io.StringIO("".join(chunk)), sep=",")
            return df.set_index("Name").to_dict(orient="index")

        def frequencies(chunk):
            df = pd.read_csv(io.StringIO("".join(chunk)), sep=",")
            return list(df["Frequency [Hz]"])

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
            magnitude = [[float(x) for x in x[1:]] for x in df.values[1:]]
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

        return properties(chunks[0]), frequencies(chunks[1]), spectrogram(chunks[2])

    def read_csv(content):
        df = pd.read_csv(io.StringIO("".join(content[0])), sep=",")

        properties = []
        frequencies = list(map(lambda x: float(x), list(df)[1:]))

        abs_ts = list(map(lambda x: float(x), list(df[df.columns[0]])))
        rel_ts = rel_ts = list(map(lambda x: x - abs_ts[0], abs_ts))
        magnitude = [[x for x in x[1:]] for x in df.values]

        um = {}
        um["time"] = "ms"
        um["frequency"] = "Hz"
        um["magnitude"] = "dBm"

        return properties, frequencies, rel_ts, abs_ts, magnitude, um

    chunks = split_file_by_empty_lines(filename)
    if len(chunks) == 1:
        return read_csv(chunks)
    elif len(chunks) == 3:
        a = read_csv_from_spm(chunks)
        return a[0], a[1], a[2][0], a[2][1], a[2][2], a[2][3]
