import datetime
import pandas as pd
from io import StringIO


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

    def spectrogram(chunk):
        def parse_dt(d):
            try:
                return datetime.datetime.strptime(d, "%H:%M:%S:%f").timestamp()
            except:
                return None

        csv_data = StringIO("\n".join(chunk))
        df = pd.read_csv(csv_data, header=[0, 1, 2], low_memory=False)
        df = df.dropna(axis=1, how="any")
        df = df.apply(pd.to_numeric, errors="coerce")

        rel_ts = [parse_dt(x[1]) for x in df.columns][1:]
        rel_ts = [rel_ts[0] - x for x in rel_ts]
        abs_ts = [x[0] for x in df.columns][1:]
        freqs = df[df.columns[0]].values
        mags = df.drop(df.columns[0], axis=1).T.values

        um = {}
        um["time"] = "ms"
        um["freqs"] = df.columns[0][-1].split("[")[-1].split("]")[0]
        um["mags"] = df.columns[1][-1].split("[")[-1].split("]")[0]

        return rel_ts, abs_ts, freqs, mags, um

    def read_csv_from_spm(chunks):
        def properties(chunk):
            df = pd.read_csv(StringIO("".join(chunk)), sep=",")
            return df.set_index("Name").to_dict(orient="index")

        # def frequencies(chunk):
        #     df = pd.read_csv(StringIO("".join(chunk)), sep=",")
        #     return list(df["Frequency [Hz]"])

        p = properties(chunks[0])
        s = spectrogram(chunks[2])
        return p, s[0], s[1], s[2], s[3], s[4]

    chunks = split_file_by_empty_lines(filename)
    if len(chunks) == 1:
        return spectrogram(chunks)
    elif len(chunks) == 3:
        return read_csv_from_spm(chunks)
