import sys

sys.dont_write_bytecode = True

import argparse
import func as func
import Spectrogram.Spectrogram as Spec


setup = {
    "data": {
        "help": "File to load",
        "type": str,
        "default": None,
        "func": func.data,
    },
    "lo": {
        "help": "Local oscillator [Hz]",
        "type": float,
        "default": 0,
        "func": func.lo,
    },
    "show": {
        "help": "Show plot",
        "type": str,
        "default": None,
        "func": func.show,
    },
    "tslice": {
        "help": "Set time slice in the filename unit of measure",
        "type": float,
        "default": None,
        "func": None,
    },
    "fslice": {
        "help": "Set frequency slice in the filename unit of measure",
        "type": float,
        "default": None,
        "func": None,
    },
    "compute": {
        "help": "Call the compute module to perform calculations",
        "type": str,
        "default": None,
        "func": func.compute,
    },
    "export": {
        "help": "Plot to save in csv",
        "type": str,
        "default": None,
        "func": func.export,
    },
    "frange": {
        "help": "Frequency range",
        "type": float,
        "default": None,
        "func": None,
    },
    "trange": {
        "help": "Time range",
        "type": float,
        "default": None,
        "func": None,
    },
}

parser = argparse.ArgumentParser(description="Waterfall")
parser.add_argument("-i", "--int", help="Interactive mode", action="store_true")

for s in setup:
    parser.add_argument(
        f"--{s}",
        help=setup[s]["help"],
        type=setup[s]["type"],
        default=setup[s]["default"],
    )

args = parser.parse_args()
spec = Spec.Spectrogram()

idx = 0
while True:
    k = None
    v = None
    if args.int:
        uin = input(f"{(idx+1):03} waterfall> ")
        uins = uin.split()
        k = uins[0]
        if k not in setup:
            print(f"{k}: command not found")
            continue

        v = uins[1:]
        v = list(map(lambda x: setup[k]["type"](x), v))
        setattr(args, k, v)
    elif idx < len(args.__dict__):
        k = list(args.__dict__)[idx]
        v = getattr(args, k)
    else:
        break

    idx += 1
    if k in setup:
        if setup[k]["func"]:
            setup[k]["func"](spec, args)
