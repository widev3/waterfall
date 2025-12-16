import os
from Spectrogram.CSV import read as read_csv
from Spectrogram.IQ import read as read_iq


class Spectrogram(object):
    def __init__(self):
        self.properties = None
        self.frequencies = None
        self.rel_ts = None
        self.abs_ts = None
        self.magnitude = None
        self.um = None

    def read(self, filename: str):
        fn, ext = os.path.splitext(filename)
        if ext == ".csv":
            (
                self.properties,
                self.frequencies,
                self.rel_ts,
                self.abs_ts,
                self.magnitude,
                self.um,
            ) = read_csv(filename)
        elif ext in [".iq", ".wav"]:
            (
                self.properties,
                self.frequencies,
                self.rel_ts,
                self.abs_ts,
                self.magnitude,
                self.um,
            ) = read_iq(filename)

    def time_slice(self, x):
        return self.magnitude[x]

    def freq_slice(self, x):
        return [item[x] for item in self.magnitude]

    def apply_lo(self, lo: float):
        self.frequencies = list(map(lambda x: x + lo, self.frequencies))

    def remove_lo(self, lo: float):
        self.apply_lo(-lo)
