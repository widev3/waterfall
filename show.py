import utils
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors


def waterfall(spec, args):
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
        extent=[args.frange[0], args.frange[1], args.trange[0], args.trange[1]],
    )

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label(f"Magnitude [{spec.um["mags"]}]")
    ax.set_xlabel(f"Frequency [{spec.um["freqs"]}]")
    ax.set_ylabel(f"Time [{spec.um["time"]}]")
    utils.attributes(ax, args)
    return spec


def tslice(spec, args):
    (x, y) = spec.time_slice(val=args.tslice[0])
    mask = (x >= args.frange[0]) & (x <= args.frange[1])
    (x, y) = (x[mask], y[mask])
    fig, ax = plt.subplots()
    if len(args.show) == 2:
        if args.show[1] == "fft":
            (x, y) = utils.fft(fig, x, y)
        elif args.show[1] == "ifft":
            pass
    else:
        fig.canvas.manager.set_window_title("Time slice")

    (line,) = ax.plot(x, y, color="C0", linewidth=1.5)
    ax.set_xlabel(f"Frequency [{spec.um["freqs"]}]")
    ax.set_ylabel(f"Magnitude [{spec.um["mags"]}]")
    utils.attributes(ax, args)
    return spec


def fslice(spec, args):
    (x, y) = spec.freq_slice(val=args.fslice[0])
    mask = (x >= args.trange[0]) & (x <= args.trange[1])
    (x, y) = (x[mask], y[mask])
    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title("Frequency slice")
    (line,) = ax.plot(x, y, color="C0", linewidth=1.5)
    ax.set_xlabel(f"Time [{spec.um["time"]}]")
    ax.set_ylabel(f"Magnitude [{spec.um["mags"]}]")
    utils.attributes(ax, args)
    return spec


def ftot(spec, args):
    x = spec.freqs
    y = 10 * np.log10(np.sum(np.power(10, spec.mags / 10), axis=0))
    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title("Total for frequency")
    (line,) = ax.plot(x, y, color="C0", linewidth=1.5)
    ax.set_xlabel(f"Frequency [{spec.um["freqs"]}]")
    ax.set_ylabel(f"Magnitude [{spec.um["mags"]}]")
    utils.attributes(ax, args)
    return spec


def ttot(spec, args):
    x = spec.rel_ts
    y = 10 * np.log10(np.sum(np.power(10, spec.mags / 10), axis=1))
    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title("Total for time")
    (line,) = ax.plot(x, y, color="C0", linewidth=1.5)
    ax.set_xlabel(f"Time [{spec.um["freqs"]}]")
    ax.set_ylabel(f"Magnitude [{spec.um["mags"]}]")
    utils.attributes(ax, args)
    return spec
