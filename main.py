import sys

sys.dont_write_bytecode = True

from os import path
from PySide6.QtWidgets import QApplication
from despyner.SingletonSplash import SingletonSplash


def abs_path(filename, ref_position=__file__):
    return path.abspath(path.join(path.dirname(ref_position), filename))


app = QApplication(sys.argv)
SingletonSplash(abs_path("wide3.png", __file__))
SingletonSplash().message("Loading...")

import Config
from despyner.QtMger import WindowManager
from ui.Dashboard import Ui_Dialog
from ux.Dashboard import Dashboard

if __name__ == "__main__":
    SingletonSplash().message("Starting...")
    Config.Config("config.json")
    c = Config.Config().config
    win = WindowManager(Ui_Dialog, Dashboard, c)
    win.show()
    SingletonSplash().close()
    sys.exit(app.exec())
