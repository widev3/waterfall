import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator


def tot(arr):
    return 10 * np.log10(np.sum(np.power(10, arr / 10)))


def fft(fig, x, y):
    fig.canvas.manager.set_window_title("FFT")
    pwr = np.power(10, np.array(y) / 10)
    fft_mag = np.fft.fft(pwr)
    fft_freq = np.fft.fftfreq(len(pwr), d=(x[1] - x[0]))
    x = fft_freq[fft_freq > 0]
    y = np.abs(fft_mag[fft_freq > 0])
    return (x, y)


def attributes(ax, args):
    ax.set_title(args.data[0])
    ax.minorticks_on()
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(axis="both", which="major", length=7)
    ax.tick_params(axis="both", which="minor", length=4, color="gray")
    ax.grid(which="major", linestyle="-", linewidth=0.5, alpha=0.5)
    ax.grid(which="minor", linestyle=":", linewidth=0.5, alpha=0.4)
    plt.show(block=False)
