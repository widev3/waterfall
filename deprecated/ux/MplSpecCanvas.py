import numpy as np
from matplotlib import colors
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar,
)


class MplSpecCanvas(FigureCanvasQTAgg):
    def __init__(self, button_press_event=None):
        self.__button_press_event = button_press_event
        self.__ms_ev = None

        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        self.axes.set_xlabel("frequency")
        self.axes.set_ylabel("time")

        self.__xlim = self.axes.get_xlim()
        self.__ylim = self.axes.get_ylim()

        self.fig.canvas.mpl_connect(
            "button_press_event", self.__internal_button_press_event
        )
        self.axes.callbacks.connect("xlim_changed", self.__internal_xlim_changed)
        self.axes.callbacks.connect("ylim_changed", self.__internal_ylim_changed)

        self.__cursor = Cursor(
            self.axes, horizOn=True, vertOn=True, color="white", linewidth=1
        )
        self.im = self.axes.imshow(X=[[]], aspect="auto")
        self.fig.tight_layout()
        super().__init__(self.fig)

    def set_data(self, sp, conf):
        self.__sp = sp
        self.im = self.axes.imshow(
            X=self.__sp.mags,
            norm=colors.PowerNorm(
                gamma=conf["gamma"],
                vmin=np.min(self.__sp.mags),
                vmax=np.max(self.__sp.mags),
            ),
            cmap=conf["cmap"],
            aspect="auto",
            interpolation="none",
            origin="lower",
            extent=[
                np.min(self.__sp.freqs),
                np.max(self.__sp.freqs),
                np.min(self.__sp.rel_ts),
                np.max(self.__sp.rel_ts),
            ],
        )

        self.__set_ticks()
        self.fig.tight_layout()
        self.draw()

    def get_toolbar(self):
        self.toolbar = NavigationToolbar(self, coordinates=True)
        return self.toolbar

    def __set_ticks(self):
        self.__xlim = self.axes.get_xlim()
        mx = self.__xlim[0]
        Mx = self.__xlim[1]
        self.axes.set_xticks(np.arange(mx, Mx, (Mx - mx) / 10))
        self.axes.set_xticks(np.arange(mx, Mx, (Mx - mx) / 30), minor=True)

        self.__ylim = self.axes.get_ylim()
        my = self.__ylim[0]
        My = self.__ylim[1]
        self.axes.set_yticks(np.arange(my, My, (My - my) / 10))
        self.axes.set_yticks(np.arange(my, My, (My - my) / 30), minor=True)

        self.axes.grid(which="minor", alpha=0.2)
        self.axes.grid(which="major", alpha=0.5)

    def __internal_button_press_event(self, x=None):
        def get_idx(arr, val):
            return list(filter(lambda y: val >= y[1], enumerate(arr)))[-1]

        self.__ms_ev = x if x else self.__ms_ev
        if self.__button_press_event and self.__ms_ev:
            idx_x = get_idx(self.__sp.freqs, self.__ms_ev.xdata)
            idx_y = get_idx(self.__sp.rel_ts, self.__ms_ev.ydata)

            data = (self.__ms_ev.xdata, self.__ms_ev.ydata)  # wr plot data
            plot = (self.__ms_ev.x, self.__ms_ev.y)  # wr plot frame
            array = (idx_x[0], idx_y[0])  # wr array indices
            data_exact = (idx_x[1], idx_y[1])  # wr plot data

            span = (self.__xlim, self.__ylim)  # wr plot data
            self.__button_press_event(data, plot, array, data_exact, span)
            self.__set_ticks()

    def __internal_xlim_changed(self, x):
        self.__xlim = self.axes.get_xlim()
        self.__internal_button_press_event()

    def __internal_ylim_changed(self, y):
        self.__ylim = self.axes.get_ylim()
        self.__internal_button_press_event()
