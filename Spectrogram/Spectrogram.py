import os
from Spectrogram.RSCSVFromSPM import RSCSVFromSPM
from Spectrogram.IQ import IQ


class Spectrogram(object):
    def __init__(self):
        self.__driver = None
        self.__driver_dict = {}
        self.__driver_dict[".iq"] = IQ()
        self.__driver_dict[".csv"] = RSCSVFromSPM()

    def read(self, filename: str):
        fn, ext = os.path.splitext(filename)
        self.__driver = self.__driver_dict[ext]

        self.properties, self.frequencies, spectrogram = self.__driver.read(filename)
        self.rel_ts, self.abs_ts, self.magnitude, self.um = spectrogram

    def time_slice(self, x):
        return self.spec["m"][x]

    def freq_slice(self, x):
        return [item[x] for item in self.spec["m"]]

    def apply_lo(self, lo: float):
        self.__driver.frequencies = list(
            map(lambda x: x + lo, self.__driver.frequencies)
        )

    def remove_lo(self, lo: float):
        self.apply_lo(-lo)
