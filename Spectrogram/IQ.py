import numpy as np
from scipy.io import wavfile
from scipy.signal import spectrogram


def read(filename: str):
    properties = []
    center_freq = 90.215e6  # Central frequency in Hz
    sample_rate = 2.4e6  # Sample rate of the IQ data in Hz

    fs, iq_data = wavfile.read(filename)
    iq = iq_data[:, 0] + 1j * iq_data[:, 1]

    freqs, abs_ts, mags = spectrogram(
        iq,
        fs=sample_rate,
        window="hann",
        nperseg=2048,
        noverlap=1536,
        scaling="density",
        mode="magnitude",
        return_onesided=False,
    )

    mags = np.fft.fftshift(mags, axes=0)
    freqs = np.fft.fftshift(freqs)
    mags = list(map(list, zip(*mags)))
    freqs = freqs + np.max(freqs) + center_freq
    rel_ts = list(map(lambda x: x - abs_ts[0], abs_ts))
    um = []

    return properties, rel_ts, abs_ts, freqs, mags, um
