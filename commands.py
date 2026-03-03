import matplotlib

matplotlib.use("QtAgg")

import utils
import numpy as np
import pandas as pd
import show as _show
import spectrogram.Spectrogram as Spec

specs = {}


def nx(prop, l):
    return specs[prop[-1] if len(prop) == l else "."]


def load(args):
    spec = Spec.Spectrogram()
    spec.read(args.load[0])
    specs[args.load[1] if len(args.load) == 2 else "."] = spec


def lo(args):
    nx(args.lo, 2).apply_lo(args.lo[0])


def trange(args):
    nx(args.trange, 3).range(trange=args.trange)


def frange(args):
    nx(args.frange, 3).range(frange=args.frange)


def tslice(args):
    nx(args.tslice, 2).tslice = args.tslice[0]


def fslice(args):
    nx(args.fslice, 2).fslice = args.fslice[0]


def compute(args):
    if args.compute[0] == "tot":
        spec = nx(args.compute, 2)
        print(f"{utils.tot(spec.mags)} {spec.um["mags"]}")
    elif args.compute[0] == "max":
        spec = nx(args.compute, 2)
        print(f"{np.max(spec.mags)} {spec.um["mags"]}")
    elif args.compute[0] == "min":
        spec = nx(args.compute, 2)
        print(f"{np.min(spec.mags)} {spec.um["mags"]}")
    elif args.compute[0] == "fslice":
        spec = nx(args.compute, 3)
        y = np.array(spec.freq_slice(val=spec.fslice)[1])
        if args.compute[1] == "tot":
            print(f"{utils.tot(y)} {spec.um["mags"]}")
        elif args.compute[1] == "max":
            print(f"{np.max(y)} {spec.um["mags"]}")
        elif args.compute[1] == "min":
            print(f"{np.min(y)} {spec.um["mags"]}")
    elif args.compute[0] == "tslice":
        spec = nx(args.compute, 3)
        y = np.array(spec.time_slice(val=spec.tslice)[1])
        if args.compute[1] == "tot":
            print(f"{utils.tot(y)} {spec.um["mags"]}")
        elif args.compute[1] == "max":
            print(f"{np.max(y)} {spec.um["mags"]}")
        elif args.compute[1] == "min":
            print(f"{np.min(y)} {spec.um["mags"]}")

def show(args):
    spec = nx(args.show, 2)
    if args.show[0] == "waterfall":
        _show.waterfall(spec)
    elif args.show[0] == "tslice":
        _show.tslice(spec)
    elif args.show[0] == "fslice":
        _show.fslice(spec)
    elif args.show[0] == "ftot":
        _show.ftot(spec)
    elif args.show[0] == "ttot":
        _show.ttot(spec)
