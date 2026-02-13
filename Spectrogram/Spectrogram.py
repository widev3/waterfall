import os
from Spectrogram.CSV import read as read_csv
from Spectrogram.IQ import read as read_iq


class Spectrogram(object):
    def __init__(self):
        self.properties = None
        self.frequencies = None
        self.rel_ts = None
        self.abs_ts = None
        self.mags = None
        self.freqs = None
        self.um = None

    def read(self, filename: str):
        fn, ext = os.path.splitext(filename)
        if ext == ".csv":
            (
                self.properties,
                self.frequencies,
                self.rel_ts,
                self.abs_ts,
                self.freqs,
                self.mags,
                self.um,
            ) = read_csv(filename)
        elif ext in [".iq", ".wav"]:
            (
                self.properties,
                self.frequencies,
                self.rel_ts,
                self.abs_ts,
                self.freqs,
                self.mags,
                self.um,
            ) = read_iq(filename)

    def time_slice(self, x):
        return self.mags[x]

    def freq_slice(self, x):
        return [item[x] for item in self.mags]

    def apply_lo(self, lo: float):
        self.freqs = list(map(lambda x: x + lo, self.freqs))

    def remove_lo(self, lo: float):
        self.apply_lo(-lo)
