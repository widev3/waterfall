import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.widgets import Cursor
from matplotlib.ticker import AutoMinorLocator


def read(spec, args):
    spec.read(args.filename)


def apply_lo(spec, args):
    spec.apply_lo(args.lo)


def show(spec, args):
    if args.show == "waterfall":
        fig, ax = plt.subplots()
        fig.canvas.manager.set_window_title("Waterfall")

        im = ax.imshow(
            X=spec.mags,
            norm=colors.PowerNorm(
                gamma=0.5,
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
        ax.set_title(args.filename)

        ax.minorticks_on()
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())

        ax.tick_params(axis="both", which="major", length=7)
        ax.tick_params(axis="both", which="minor", length=4, color="gray")

        ax.grid(which="major", linestyle="-", linewidth=0.5, alpha=0.5)
        ax.grid(which="minor", linestyle=":", linewidth=0.5, alpha=0.4)

        fig.tight_layout(rect=[0.04, 0.04, 0.99, 0.99])

        cursor = Cursor(ax, useblit=True, color="red", linewidth=1)

        plt.show()
