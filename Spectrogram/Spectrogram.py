import os
import magic
import numpy as np
from Spectrogram.IQ import read as read_iq
from Spectrogram.CSV import read as read_csv


class Spectrogram(object):
    def __init__(self):
        self.properties = None
        self.rel_ts = None
        self.abs_ts = None
        self.mags = None
        self.freqs = None
        self.orig_freqs = np.array([])
        self.um = None

    def read(self, filename: str):
        fn, ext = os.path.splitext(filename)
        if not ext:
            with open(filename, "rb") as f:
                file_type = magic.from_buffer(f.read(2048), mime=True)
                if file_type:
                    ext = f".{file_type.split("/")[-1]}"

        if ext == ".csv":
            (
                self.properties,
                self.rel_ts,
                self.abs_ts,
                self.freqs,
                self.mags,
                self.um,
            ) = read_csv(filename)
        elif ext in [".iq", ".wav"]:
            (
                self.properties,
                self.rel_ts,
                self.abs_ts,
                self.freqs,
                self.mags,
                self.um,
            ) = read_iq(filename)

    def time_slice(self, idx=None, val=None):
        if idx:
            return (self.freqs, self.mags[idx])
        if val:
            idx = min(range(len(self.rel_ts)), key=lambda i: abs(self.rel_ts[i] - val))
            return self.time_slice(idx)

    def freq_slice(self, idx=None, val=None):
        if idx:
            return (self.rel_ts, [item[idx] for item in self.mags])
        if val:
            idx = min(range(len(self.freqs)), key=lambda i: abs(self.freqs[i] - val))
            return self.freq_slice(idx)

    def apply_lo(self, lo: float):
        if not self.orig_freqs.any():
            self.orig_freqs = self.freqs
        self.freqs = list(map(lambda x: x + lo, self.orig_freqs))

    def remove_lo(self, lo: float):
        self.apply_lo(-lo)

    def set_scale(self, mag):
        if mag == "linear":
            self.mags = np.power(10, self.mags / 10)
            self.um["mags"] = "mW"
        elif mag == "log":
            self.mags = np.log(self.mags)
            self.um["mags"] = "dBm"
