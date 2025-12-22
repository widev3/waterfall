import sys

sys.dont_write_bytecode = True

from os import path
from PySide6.QtWidgets import QApplication
from despyner.SingletonSplash import SingletonSplash


def abs_path(filename, ref_position=__file__):
    return path.abspath(path.join(path.dirname(ref_position), filename))


app = QApplication(sys.argv)
SingletonSplash(abs_path("wide3.ico", __file__))
SingletonSplash().message("Loading...")

import despyner.Config as Config
from ui.Dashboard import Ui_Dialog
from ux.Dashboard import Dashboard
from despyner.QtMger import WindowManager

if __name__ == "__main__":
    SingletonSplash().message("Starting...")
    default_config = {
        "lo": [
            {"value": 0, "band": None},
            {"value": 5150000000, "band": "C"},
            {"value": 9750000000, "band": "Ku Tone OFF"},
            {"value": 10600000000, "band": "Ku Tone ON"},
        ],
        "viewer": {"gamma": 0.45, "cmap": "berlin"},
    }
    Config.Config("config.json", default_config)
    win = WindowManager(Ui_Dialog, Dashboard, Config.Config().config)
    win.show()
    SingletonSplash().close()
    sys.exit(app.exec())
