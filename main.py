import argparse
import func as func
import Spectrogram.Spectrogram as Spec


setup = {
    "filename": {
        "help": "File to load",
        "type": str,
        "default": None,
        "func": func.read,
    },
    "lo": {
        "help": "Local oscillator [Hz]",
        "type": float,
        "default": 0,
        "func": func.apply_lo,
    },
    "show": {
        "help": "Show plot",
        "type": str,
        "default": None,
        "func": func.show,
    },
    "tslice": {
        "help": "Time or frequency slice",
        "type": float,
        "default": None,
        "func": None,
    },
}

parser = argparse.ArgumentParser(description="Waterfall")
parser.add_argument("--i", help="Interactive mode", action="store_true")

for s in setup:
    parser.add_argument(
        f"-{s[0]}",
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
    if args.i:
        uin = input(f"{(idx+1):03} waterfall> ")
        uins = uin.split()
        k = uins[0]
        if k not in setup:
            print(f"{k}: command not found")
            continue

        v = uins[1:]
        v = list(map(lambda x: setup[k]["type"](x), v))
        v = v[0] if isinstance(v, list) and len(v) == 1 else v
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
