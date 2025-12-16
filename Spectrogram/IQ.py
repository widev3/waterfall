import numpy as np
from scipy.signal import spectrogram
from scipy.io import wavfile


def read(filename: str):
    properties = []
    center_freq = 90.3e6  # Central frequency in Hz
    sample_rate = 2.4e6  # Sample rate of the IQ data in Hz

    # iq_data = np.fromfile(filename, dtype=np.float32)
    # iq_data = iq_data[0::2] + 1j * iq_data[1::2]  # Convert to complex

    fs, iq_data = wavfile.read(filename)
    iq_data = iq_data[:, 0] + 1j * iq_data[:, 1]

    # Compute the spectrogram
    frequencies, abs_ts, magnitude = spectrogram(
        iq_data,
        fs=sample_rate,
        nperseg=1024,
        noverlap=512,
        scaling="density",
        mode="magnitude",
        return_onesided=False,
    )

    frequencies = list(filter(lambda x: not x < 0, frequencies))
    magnitude = list(map(list, zip(*magnitude)))
    magnitude = list(map(lambda x: x[len(frequencies) :], magnitude))

    # Adjust frequency axis to actual RF frequencies
    # frequencies = frequencies + center_freq
    # frequencies = []
    rel_ts = list(map(lambda x: x - abs_ts[0], abs_ts))
    # abs_ts = []
    # magnitude = [[]]
    um = []

    return properties, frequencies, rel_ts, abs_ts, magnitude, um
