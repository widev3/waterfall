import os
import globals
from Spectrogram.Spectrogram import Spectrogram

from ux.Computer import Computer
from ui.Computer import Ui_Dialog
from despyner.QtMger import WindowManager
from ux.MplSpecCanvas import MplSpecCanvas
from despyner.QtMger import set_icon, i_name
from ux.Mpl2DPlotCanvas import Mpl2DPlotCanvas
from single_include import QFileDialog, Qt, numpy as np


class Dashboard:
    def __init__(self, ui, dialog, args=None):
        self.ui = ui
        self.dialog = dialog
        self.args = args
        self.bands = list(map(lambda x: f"{x["band"]}: {x["value"]}", self.args["lo"]))
        self.__canvas_spec = None
        self.__filename = None
        self.__memory = []

        self.dialog.setWindowState(Qt.WindowMaximized)

        set_icon(self.ui.pushButtonFileOpen, i_name.FILE_OPEN, globals.theme, True)
        set_icon(
            self.ui.labelOffsetsView, i_name.CADENCE, globals.theme, True, (30, 30)
        )

        self.ui.comboBoxOffsetsView.currentIndexChanged.connect(
            self.__comboBoxOffsetsViewCurrentIndexChanged
        )

        self.ui.horizontalSliderGammaView.valueChanged.connect(
            self.__horizontalSliderGammaViewValueChanged
        )

        self.ui.horizontalSliderGammaView.setValue(self.args["viewer"]["gamma"] * 1000)

        self.ui.comboBoxOffsetsView.addItems(self.bands)

        self.ui.pushButtonFileOpen.clicked.connect(self.__open_track)
        self.ui.pushButtonAdd.clicked.connect(self.__add_track)
        self.ui.pushButtonRemove.clicked.connect(self.__remove_track)
        self.ui.pushButtonCompute.clicked.connect(self.__open_signal_computer)

        self.__canvas_spec = MplSpecCanvas(
            lambda a, b, c, d, e: self.update_spec(a, b, c, d, e)
        )
        self.ui.verticalLayoutSpec.addWidget(self.__canvas_spec.get_toolbar())
        self.ui.verticalLayoutSpec.addWidget(self.__canvas_spec)

        self.__freq_plot = Mpl2DPlotCanvas(labels=("frequency", "intensity"))
        self.ui.verticalLayoutTime.addWidget(self.__freq_plot.get_toolbar())
        self.ui.verticalLayoutTime.addWidget(self.__freq_plot)

        self.__time_plot = Mpl2DPlotCanvas(labels=("intensity", "time"))
        self.ui.verticalLayoutFreq.addWidget(self.__time_plot.get_toolbar())
        self.ui.verticalLayoutFreq.addWidget(self.__time_plot)

        self.__total_plot = Mpl2DPlotCanvas(labels=("time", "intensity"))
        self.ui.verticalLayoutTotal.addWidget(self.__total_plot.get_toolbar())
        self.ui.verticalLayoutTotal.addWidget(self.__total_plot)

    def __comboBoxOffsetsViewCurrentIndexChanged(self, d):
        self.__lo = self.args["lo"][d]["value"]
        if self.__filename:
            self.__load_track()

    def __horizontalSliderGammaViewValueChanged(self, d):
        d /= 1000
        self.ui.labelGammaView.setText(str(d))
        if self.__canvas_spec:
            self.__canvas_spec.im.norm.gamma = d
            self.__canvas_spec.fig.canvas.draw()
            self.__canvas_spec.fig.canvas.flush_events()

    def __open_track(self):
        supported = {}
        supported[".csv"] = "CSV"
        supported[".iq"] = "IQ"
        supported[".cf32"] = "CF32"
        supported[".wav"] = "WAV"
        supported[".iq.gz"] = "GZIP IQ"
        supported[".cf32.gz"] = "GZIP cf32"
        supported[".wav.gz"] = "GZIP WAV"
        filename, _ = QFileDialog.getOpenFileUrl(
            parent=None,
            caption="Spectrogram file",
            filter=";;".join(
                list(map(lambda x: f"{supported[x]} Files (*{x})", supported.keys()))
            ),
        )

        if filename:
            self.__filename = filename.path()
            self.__load_track()
        else:
            self.__filename = None

    def update_spec(self, data, plot, array, data_exact, span):
        # update freq plot
        y = self.__spec.time_slice(array[1])
        xy = zip(self.__spec.frequencies, y)
        xy = list(filter(lambda x: x[0] >= span[0][0] and x[0] <= span[0][1], xy))
        x = list(map(lambda x: x[0], xy))
        y = list(map(lambda x: x[1], xy))
        self.__freq_plot.set_data(x, y)
        pwr = sum(np.power(10, np.array(y) / 10 - 3)) * 10**6
        self.ui.lineEditFMin.setText("{:e}".format(self.__freq_plot.xlim[0]))
        self.ui.lineEditFMax.setText("{:e}".format(self.__freq_plot.xlim[1]))
        self.ui.lineEditTPwr.setText("{:e}".format(pwr))

        # update time plot
        x = self.__spec.freq_slice(array[0])
        xy = zip(x, self.__spec.rel_ts)
        xy = list(filter(lambda x: x[1] >= span[1][0] and x[1] <= span[1][1], xy))
        x = np.array(list(map(lambda x: x[0], xy)))
        y = np.array(list(map(lambda x: x[1], xy)))
        self.__time_plot.set_data(x, y)
        pwr = sum(np.power(10, np.array(y) / 10 - 3)) * 10**6
        self.ui.lineEditTMin.setText("{:e}".format(self.__time_plot.xlim[0]))
        self.ui.lineEditTMax.setText("{:e}".format(self.__time_plot.xlim[1]))
        self.ui.lineEditFPwr.setText("{:e}".format(pwr))

    def __load_track(self):
        self.__spec = Spectrogram()
        self.__spec.read(self.__filename)
        self.__spec.apply_lo(self.__lo)
        self.__canvas_spec.set_data(self.__spec, self.args["viewer"])
        self.__total_plot.set_data(
            self.__spec.rel_ts,
            np.sum(np.power(10, np.array(self.__spec.magnitude) / 10 - 3), axis=1),
        )

        self.ui.lineEditFilename.setText(self.__filename)
        self.ui.lineEditTMin.setText("{:e}".format(min(self.__spec.rel_ts)))
        self.ui.lineEditTMax.setText("{:e}".format(max(self.__spec.rel_ts)))
        self.ui.lineEditFMin.setText("{:e}".format(min(self.__spec.frequencies)))
        self.ui.lineEditFMax.setText("{:e}".format(max(self.__spec.frequencies)))

    def __add_track(self):
        f = f"[{"{:e}".format(self.__freq_plot.xlim[0])}, {"{:e}".format(self.__freq_plot.xlim[1])}] MHz"
        t = f"[{"{:e}".format(self.__time_plot.xlim[0])}, {"{:e}".format(self.__time_plot.xlim[1])}] sec"
        self.ui.listWidgetSignals.addItem(f"{f}, {t}")
        self.__memory.append((self.__freq_plot.get_data(), self.__time_plot.get_data()))

    def __remove_track(self):
        print(self.ui.listWidgetSignals)

    def __open_signal_computer(self):
        args = {"memory": self.__memory, "spec": self.__spec}
        win = WindowManager(ui=Ui_Dialog, ux=Computer, args=args, parent=self.dialog)
        win.show()
