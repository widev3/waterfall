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
        "func": commands.tslice,
    },
    "fslice": {
        "help": "Set frequency slice in the filename unit of measure",
        "type": float,
        "default": None,
        "func": commands.fslice,
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
        "func": commands.frange,
    },
    "trange": {
        "help": "Time range",
        "type": float,
        "default": None,
        "func": commands.trange,
    },
    "int": {
        "help": "Interactive mode",
        "action": "store_true",
        "default": None,
        "func": None,
    },
}

parser = argparse.ArgumentParser(description="Waterfall")

for s in setup:
    if "type" in setup[s]:
        parser.add_argument(
            f"--{s}",
            help=setup[s]["help"],
            # type=setup[s]["type"],
            default=setup[s]["default"],
        )
    elif "action" in setup[s]:
        parser.add_argument(
            f"--{s}",
            help=setup[s]["help"],
            action=setup[s]["action"],
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
    v = uins[1:]
    if k not in setup:
        idx += 1
        if k in ["help"]:
            print(f"{(idx):03} \U0001f393 helper")
            parser.print_help()
        else:
            print(f"{(idx):03} \U0001fadf  command not found")

        continue

    setattr(args, k, v)
    if k in setup:
        commands[idx] = (k, v)
        if setup[k]["func"]:
            spec = setup[k]["func"](spec, args)
