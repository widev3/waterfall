import matplotlib

matplotlib.use("QtAgg")

import utils
import numpy as np
import pandas as pd
import show as _show

savings = {}


def data(spec, args):
    spec.read(args.data[0])
    args.frange = np.array([np.min(spec.freqs), np.max(spec.freqs)])
    args.trange = np.array([np.min(spec.rel_ts), np.max(spec.rel_ts)])
    return spec


def lo(spec, args):
    spec.apply_lo(args.lo[0])
    args.frange += args.lo[0]
    args.trange += args.lo[0]
    return spec


def trange(spec, args):
    spec.range(trange=args.trange)
    return spec


def frange(spec, args):
    spec.range(frange=args.frange)
    return spec


def tslice(spec, args):
    pass


def fslice(spec, args):
    pass


def compute(spec, args):
    if args.compute[0] == "tot":
        print(f"{utils.tot(spec.mags)} {spec.um["mags"]}")
    elif args.compute[0] == "max":
        print(f"{np.max(spec.mags)} {spec.um["mags"]}")
    elif args.compute[0] == "min":
        print(f"{np.min(spec.mags)} {spec.um["mags"]}")
    elif args.compute[0] == "fslice":
        y = np.array(spec.freq_slice(val=args.fslice[0])[1])
        if args.compute[1] == "tot":
            print(f"{utils.tot(y)} {spec.um["mags"]}")
        elif args.compute[1] == "max":
            print(f"{np.max(y)} {spec.um["mags"]}")
        elif args.compute[1] == "min":
            print(f"{np.min(y)} {spec.um["mags"]}")
    elif args.compute[0] == "tslice":
        y = np.array(spec.time_slice(val=args.tslice[0])[1])
        if args.compute[1] == "tot":
            print(f"{utils.tot(y)} {spec.um["mags"]}")
        elif args.compute[1] == "max":
            print(f"{np.max(y)} {spec.um["mags"]}")
        elif args.compute[1] == "min":
            print(f"{np.min(y)} {spec.um["mags"]}")


def export(spec, args):
    if len(args.export) == 2 and args.export[0] == "tslice":
        (x, y) = spec.time_slice(val=args.tslice[0])
        df = pd.DataFrame(
            {f"Frequency [{spec.um["freqs"]}]": x, f"Magnitude [{spec.um["mags"]}]": y}
        )
        df.to_csv(args.export[1], index=False)


def show(spec, args):
    if args.show[0] == "waterfall":
        return _show.waterfall(spec, args)
    elif args.show[0] == "tslice":
        return _show.tslice(spec, args)
    elif args.show[0] == "fslice":
        return _show.fslice(spec, args)
    elif args.show[0] == "ftot":
        return _show.ftot(spec, args)
    elif args.show[0] == "ttot":
        return _show.ttot(spec, args)
