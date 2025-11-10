import io
import datetime
import pandas as pd
from io import StringIO
from dateutil import parser
from single_include import numpy as np


class Spectrogram(object):
    def __init__(self):
        pass

    def __split_file_by_empty_lines(self):
        with open(self.__filename, "r") as file:
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

    def __properties(self, file):
        return pd.read_csv(io.StringIO("".join(file)), sep=self.__separator)

    def __frequencies(self, file):
        return pd.read_csv(io.StringIO("".join(file)), sep=self.__separator)

    def __spectrogram(self, file):
        def try_parse_dt(d):
            try:
                return parser.parse(d, dayfirst=True).timestamp()
            except:
                try:
                    return parser.parse(d, dayfirst=False).timestamp()
                except:
                    try:
                        return datetime.datetime.strptime(d, "%H:%M:%S:%f").timestamp()
                    except:
                        return None

        csv_data = "\n".join(file)
        df = pd.read_csv(StringIO(csv_data), header=[0, 1])
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
        abs_ts = abs_ts[1:]
        abs_tss = list(map(lambda x: try_parse_dt(x), abs_ts))
        rel_ts = rel_ts[1:]
        zero_time = try_parse_dt(rel_ts[0])
        rel_tss = list(map(lambda x: try_parse_dt(x), rel_ts))
        rel_tss = list(map(lambda x: zero_time - x if x else None, rel_tss))

        frequency = list(map(lambda x: float(x), df.iloc[:, 0][1:]))

        # TODO improve by computing programmatically the um
        um = {}
        um["time"] = "ms"
        um["frequency"] = "Hz"
        um["magnitude"] = "dBm"

        return {
            "r": rel_tss,
            "a": abs_tss,
            "f": list(map(lambda x: x + self.__lo, frequency)),
            "m": magnitude,
            "u": um,
        }

    def read_file(self, filename: str, separator: str, lo: float):
        self.__filename = filename
        self.__separator = separator
        self.__lo = lo

        chunks = self.__split_file_by_empty_lines()
        self.prop = self.__properties(chunks[0])
        self.freq = self.__frequencies(chunks[1])
        self.spec = self.__spectrogram(chunks[2])

    def write_file(self, filename: str):
        self.prop.to_csv(filename, index=False, header=False)
        with open(filename, "a") as f:
            f.write("\n")

        self.freq.to_csv(filename, mode="a", index=False)
        with open(filename, "a") as f:
            f.write("\n")

        df = pd.DataFrame()

        row = [
            ["Timestamp (Relative)"]
            + list(
                map(
                    lambda x: datetime.datetime.strftime(
                        datetime.datetime.fromtimestamp(x),
                        "%H:%M:%S %m/%d/%Y",
                    ),
                    self.spec["r"],
                )
            )
        ]
        df = pd.concat([df, pd.DataFrame(row)])

        row = [["Frequency [Hz]"] + ["Magnitude [dBm]"] * len(self.spec["m"][0])]
        df = pd.concat([df, pd.DataFrame(row)])

        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    map(
                        lambda x: [x[1]] + list(self.spec["m"][x[0]]),
                        enumerate(self.spec["f"]),
                    )
                ),
            ]
        )

        df.columns = ["Timestamp (Absolute)"] + list(
            map(
                lambda x: datetime.datetime.strftime(
                    datetime.datetime.fromtimestamp(x), "%H:%M:%S %m/%d/%Y"
                ),
                self.spec["a"],
            )
        )
        df.to_csv(filename, mode="a", index=False)

    def time_slice(self, x):
        return self.spec["m"][x]

    def freq_slice(self, x):
        return [item[x] for item in self.spec["m"]]
