import numpy as np
from scipy.signal import spectrogram
from scipy.io import wavfile


def read(filename: str):
    properties = []
    center_freq = 90.215e6  # Central frequency in Hz
    sample_rate = 2.4e6  # Sample rate of the IQ data in Hz

    fs, iq_data = wavfile.read(filename)
    iq = iq_data[:, 0] + 1j * iq_data[:, 1]

    frequencies, abs_ts, magnitude = spectrogram(
        iq,
        fs=sample_rate,
        window="hann",
        nperseg=2048,
        noverlap=1536,
        scaling="density",
        mode="magnitude",
        return_onesided=False,
    )

    magnitude = np.fft.fftshift(magnitude, axes=0)
    frequencies = np.fft.fftshift(frequencies)
    magnitude = list(map(list, zip(*magnitude)))
    frequencies = frequencies + np.max(frequencies) + center_freq
    rel_ts = list(map(lambda x: x - abs_ts[0], abs_ts))
    um = []

    return properties, frequencies, rel_ts, abs_ts, magnitude, um
