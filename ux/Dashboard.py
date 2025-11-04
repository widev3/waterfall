import globals
from Spectrogram import Spectrogram
from single_include import QFileDialog, Qt
from ux.MplSpecCanvas import MplSpecCanvas
from despyner.QtMger import set_icon, i_name
from ux.Mpl2DPlotCanvas import Mpl2DPlotCanvas


class Dashboard:
    def __init__(self, ui, dialog, args=None):
        self.ui = ui
        self.dialog = dialog
        self.args = args
        self.bands = list(map(lambda x: f"{x["band"]}: {x["value"]}", self.args["lo"]))
        self.__canvas_spec = None
        self.__filename = None

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

        self.__canvas_spec = MplSpecCanvas(
            lambda a, b, c, d, e: self.update_slice_canvas(a, b, c, d, e)
        )
        self.ui.verticalLayoutSpec.addWidget(self.__canvas_spec.get_toolbar())
        self.ui.verticalLayoutSpec.addWidget(self.__canvas_spec)

        self.__canvas_freq = Mpl2DPlotCanvas(labels=("frequency", "intensity"))
        self.ui.verticalLayoutTime.addWidget(self.__canvas_freq.get_toolbar())
        self.ui.verticalLayoutTime.addWidget(self.__canvas_freq)

        self.__canvas_time = Mpl2DPlotCanvas(labels=("intensity", "time"))
        self.ui.verticalLayoutFreq.addWidget(self.__canvas_time.get_toolbar())
        self.ui.verticalLayoutFreq.addWidget(self.__canvas_time)

    def __comboBoxOffsetsViewCurrentIndexChanged(self, d):
        self.__lo = self.args["lo"][d]["value"]
        self.__load_track()

    def __horizontalSliderGammaViewValueChanged(self, d):
        d /= 1000
        self.ui.labelGammaView.setText(str(d))
        if self.__canvas_spec:
            self.__canvas_spec.im.norm.gamma = d
            self.__canvas_spec.fig.canvas.draw()
            self.__canvas_spec.fig.canvas.flush_events()

    def __open_track(self):
        filename, _ = QFileDialog.getOpenFileUrl(
            parent=None,
            caption="Open Spectrogram CSV",
            filter="CSV Files (*.csv);;All Files (*)",
        )

        self.__filename = filename.path() if filename else self.__filename
        self.__load_track()

    def update_slice_canvas(self, data, plot, array, data_exact, span):
        # update freq plot
        time = self.__spec.time_slice(array[1])
        xy = zip(self.__spec.spec["f"], time)
        xy = list(filter(lambda x: x[0] >= span[0][0] and x[0] <= span[0][1], xy))
        pwr = sum(list(map(lambda x: 10 ** (x[1] / 10 - 3), xy))) * 10**6
        self.ui.lineEditTPwr.setText("{:e}".format(pwr))
        self.__canvas_freq.set_data(
            list(map(lambda x: x[0], xy)), list(map(lambda x: x[1], xy))
        )

        # update time plot
        freq = self.__spec.freq_slice(array[0])
        xy = zip(freq, self.__spec.spec["r"])
        xy = list(filter(lambda x: x[1] >= span[1][0] and x[1] <= span[1][1], xy))
        pwr = sum(list(map(lambda x: 10 ** (x[0] / 10 - 3), xy))) * 10**6
        self.ui.lineEditFPwr.setText("{:e}".format(pwr))
        self.__canvas_time.set_data(
            list(map(lambda x: x[0], xy)), list(map(lambda x: x[1], xy))
        )

    def __load_track(self):
        if not self.__filename:
            return

        self.ui.lineEditFilename.setText(self.__filename)
        self.__spec = Spectrogram()
        self.__spec.read_file(
            self.__filename, self.args["viewer"]["separator"], self.__lo
        )
        self.__canvas_spec.set_data(self.__spec.spec, self.args["viewer"])
