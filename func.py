import matplotlib

matplotlib.use("QtAgg")

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.ticker import AutoMinorLocator


def read(spec, args):
    spec.read(args.dataset[0])


def apply_lo(spec, args):
    spec.apply_lo(args.lo[0])


def compute(spec, args):
    def tot(arr):
        return 10 * np.log10(np.sum(np.power(10, arr / 10)))

    if args.compute[0] == "tot":
        print(f"{tot(spec.mags)} {spec.um["mags"]}")
    elif args.compute[0] == "max":
        print(f"{np.max(spec.mags)} {spec.um["mags"]}")
    elif args.compute[0] == "min":
        print(f"{np.min(spec.mags)} {spec.um["mags"]}")
    elif args.compute[0] == "fft":
        print("fft")
    elif args.compute[0] == "fslice":
        y = np.array(spec.freq_slice(val=args.fslice[0])[1])
        if args.compute[1] == "tot":
            print(f"{tot(y)} {spec.um["mags"]}")
        elif args.compute[1] == "max":
            print(f"{np.max(y)} {spec.um["mags"]}")
        elif args.compute[1] == "min":
            print(f"{np.min(y)} {spec.um["mags"]}")
        elif args.compute[0] == "fft":
            print("fft")
    elif args.compute[0] == "tslice":
        y = np.array(spec.time_slice(val=args.tslice[0])[1])
        if args.compute[1] == "tot":
            print(f"{tot(y)} {spec.um["mags"]}")
        elif args.compute[1] == "max":
            print(f"{np.max(y)} {spec.um["mags"]}")
        elif args.compute[1] == "min":
            print(f"{np.min(y)} {spec.um["mags"]}")
        elif args.compute[0] == "fft":
            print("fft")


def show(spec, args):
    def attributes(ax):
        ax.set_title(args.dataset[0])
        ax.minorticks_on()
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(axis="both", which="major", length=7)
        ax.tick_params(axis="both", which="minor", length=4, color="gray")
        ax.grid(which="major", linestyle="-", linewidth=0.5, alpha=0.5)
        ax.grid(which="minor", linestyle=":", linewidth=0.5, alpha=0.4)
        # fig.tight_layout(rect=[0.04, 0.04, 0.99, 0.99])
        # plt.tight_layout(rect=[0.04, 0.04, 0.99, 0.99])
        plt.show(block=False)

    if args.show[0] == "waterfall":
        fig, ax = plt.subplots()
        fig.canvas.manager.set_window_title("Waterfall")

        im = ax.imshow(
            X=spec.mags,
            norm=colors.PowerNorm(
                gamma=0.8,
                vmin=np.min(spec.mags),
                vmax=np.max(spec.mags),
            ),
            cmap="viridis",
            aspect="auto",
            interpolation="none",
            origin="lower",
            extent=[
                np.min(spec.freqs),
                np.max(spec.freqs),
                np.min(spec.rel_ts),
                np.max(spec.rel_ts),
            ],
        )

        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label(f"Magnitude [{spec.um["mags"]}]")
        ax.set_xlabel(f"Frequency [{spec.um["freqs"]}]")
        ax.set_ylabel(f"Time [{spec.um["time"]}]")
        attributes(ax)
    elif args.show[0] == "tslice":
        (x, y) = spec.time_slice(val=args.tslice[0])
        fig, ax = plt.subplots()
        if len(args.show) > 1:
            if args.show[1] == "fft":
                fig.canvas.manager.set_window_title("FFT of time slice")
                power_watts = np.power(10, np.array(y) / 10)
                fft_mag = np.fft.fft(power_watts)
                fft_freq = np.fft.fftfreq(len(power_watts), d=(x[1] - x[0]))
                x = fft_freq
                y = np.abs(fft_mag)
            elif args.show[1] == "ifft":
                pass
        else:
            fig.canvas.manager.set_window_title("Time slice")

        (line,) = ax.plot(x, y, color="C0", linewidth=1.5)
        ax.set_xlabel(f"Frequency [{spec.um["freqs"]}]")
        ax.set_ylabel(f"Magnitude [{spec.um["mags"]}]")
        attributes(ax)
    elif args.show[0] == "fslice":
        (x, y) = spec.freq_slice(val=args.fslice[0])
        fig, ax = plt.subplots()
        fig.canvas.manager.set_window_title("Frequency slice")
        (line,) = ax.plot(x, y, color="C0", linewidth=1.5)
        ax.set_xlabel(f"Time [{spec.um["time"]}]")
        ax.set_ylabel(f"Magnitude [{spec.um["mags"]}]")
        attributes(ax)
    elif args.show[0] == "ftot":
        (x, y) = (
            spec.freqs,
            10 * np.log10(np.sum(np.power(10, spec.mags / 10), axis=0)),
        )
        fig, ax = plt.subplots()
        fig.canvas.manager.set_window_title("Total for frequency")
        (line,) = ax.plot(x, y, color="C0", linewidth=1.5)
        ax.set_xlabel(f"Frequency [{spec.um["freqs"]}]")
        ax.set_ylabel(f"Magnitude [{spec.um["mags"]}]")
        attributes(ax)
    elif args.show[0] == "ttot":
        (x, y) = (
            spec.rel_ts,
            10 * np.log10(np.sum(np.power(10, spec.mags / 10), axis=1)),
        )
        fig, ax = plt.subplots()
        fig.canvas.manager.set_window_title("Total for time")
        (line,) = ax.plot(x, y, color="C0", linewidth=1.5)
        ax.set_xlabel(f"Time [{spec.um["freqs"]}]")
        ax.set_ylabel(f"Magnitude [{spec.um["mags"]}]")
        attributes(ax)
