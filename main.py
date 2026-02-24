import sys

sys.dont_write_bytecode = True

import argparse
import commands
import spectrogram.Spectrogram as Spec


setup = {
    "data": {
        "help": "File to load",
        "type": str,
        "default": None,
        "func": commands.data,
    },
    "lo": {
        "help": "Local oscillator [Hz]",
        "type": float,
        "default": 0,
        "func": commands.lo,
    },
    "show": {
        "help": "Show plot",
        "type": str,
        "default": None,
        "func": commands.show,
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
        "func": commands.compute,
    },
    "export": {
        "help": "Plot to save in csv",
        "type": str,
        "default": None,
        "func": commands.export,
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
commands = {}
while True:
    k = None
    v = None
    idx += 1
    uin = input(f"{(idx):03} \U0001fa81 ")
    uins = uin.split()

    if len(uins) == 0:
        continue

    k = uins[0]
    if k not in setup:
        idx += 1
        print(f"{(idx):03} \U0001fadf  command not found")
        continue

    v = uins[1:]
    v = list(map(lambda x: setup[k]["type"](x), v))
    setattr(args, k, v)

    if k in setup:
        commands[idx] = (k, v)
        if setup[k]["func"]:
            setup[k]["func"](spec, args)
