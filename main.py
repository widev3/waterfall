import sys

sys.dont_write_bytecode = True

import os.path
import argparse
import commands


setup = {
    "load": {
        "help": "File to load",
        "type": [str, str],  # file to load, object name
        "default": None,
        "func": commands.load,
    },
    "lo": {
        "help": "Local oscillator [Hz]",
        "type": [float, str],  # lo value, object name
        "default": 0,
        "func": commands.lo,
    },
    "show": {
        "help": "Show plot",
        "type": [str, str],  # plot type, object name
        "default": None,
        "func": commands.show,
    },
    "tslice": {
        "help": "Set time slice in the filename unit of measure",
        "type": [float, str],  # tslice value, object name
        "default": None,
        "func": commands.tslice,
    },
    "fslice": {
        "help": "Set frequency slice in the filename unit of measure",
        "type": [float, str],  # fslice value, object name
        "default": None,
        "func": commands.fslice,
    },
    "compute": {
        "help": "Call the compute module to perform calculations",
        "type": [str, str, str],  # ???
        "default": None,
        "func": commands.compute,
    },
    "frange": {
        "help": "Frequency range",
        "type": [float, float, str],  # fstart, fstop, object name
        "default": None,
        "func": commands.frange,
    },
    "trange": {
        "help": "Time range",
        "type": [float, float, str],  # tstart, tstop, object name
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
parser.add_argument("--script", help="Script file to execute", type=str, default=None)
ps = parser.parse_args()


# just an empty class for setattr
class Empty:
    pass


args = Empty()

l = []
if ps.script:
    if os.path.isfile(ps.script):
        with open(ps.script) as f:
            l = [line.rstrip() for line in f]

idx = 0
cmds = {}
while True if not l else idx < len(l):
    idx += 1
    uins = (l[idx - 1] if l else input(f"{(idx):03} \U0001fa81 ")).split()

    if len(uins) == 0:
        continue

    (k, v) = (uins[0], uins[1:])
    if k not in setup:
        print(f"{(idx):03} \U0001fadf  {k}: command not found")
        continue

    v = [t(e) for e, t in zip(v, setup[k]["type"])]
    setattr(args, k, v)
    if k in setup and setup[k]["func"]:
        cmds[idx] = (k, v)
        setup[k]["func"](args)
