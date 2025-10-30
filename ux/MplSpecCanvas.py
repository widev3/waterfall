import numpy as np
from matplotlib import colors
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar,
)


class MplSpecCanvas(FigureCanvasQTAgg):
    def __init__(self, button_press_event=None):
        self.__button_press_event = button_press_event
        self.__x = None

        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        self.axes.set_xlabel("time")
        self.axes.set_ylabel("frequency")

        self.__xlim = self.axes.get_xlim()
        self.__ylim = self.axes.get_ylim()

        self.fig.canvas.mpl_connect(
            "button_press_event", self.__internal_button_press_event
        )
        self.axes.callbacks.connect("xlim_changed", self.__internal_xlim_changed)
        self.axes.callbacks.connect("ylim_changed", self.__internal_ylim_changed)

        self.im = self.axes.imshow(X=[[]], aspect="auto")
        # self.__fig.colorbar(self.__im)
        self.fig.tight_layout()
        super().__init__(self.fig)

    def set_data(self, sp, conf):
        self.__sp = sp
        self.im = self.axes.imshow(
            X=self.__sp["m"],
            norm=colors.PowerNorm(
                gamma=conf["gamma"],
                vmin=np.min(self.__sp["m"]),
                vmax=np.max(self.__sp["m"]),
            ),
            cmap=conf["cmap"],
            aspect="auto",
            interpolation="none",
            origin="lower",
            extent=[
                min(self.__sp["r"]),
                max(self.__sp["r"]),
                min(self.__sp["f"]),
                max(self.__sp["f"]),
            ],
        )

        mx = min(self.__sp["r"])
        Mx = max(self.__sp["r"])
        self.axes.set_xticks(np.arange(mx, Mx, (Mx - mx) / 10))
        self.axes.set_xticks(np.arange(mx, Mx, (Mx - mx) / 30), minor=True)

        my = min(self.__sp["f"])
        My = max(self.__sp["f"])
        self.axes.set_yticks(np.arange(my, My, (My - my) / 10))
        self.axes.set_yticks(np.arange(my, My, (My - my) / 30), minor=True)

        self.axes.grid(which="minor", alpha=0.2)
        self.axes.grid(which="major", alpha=0.5)

        self.fig.tight_layout()
        self.draw()

    def __internal_button_press_event(self, x=None):
        def get_idx(arr, val):
            return list(filter(lambda y: val >= y[1], enumerate(arr)))[-1]

        self.__x = x if x else self.__x
        if self.__button_press_event and self.__x:
            idx_x = get_idx(self.__sp["r"], self.__x.xdata)
            idx_y = get_idx(self.__sp["f"], self.__x.ydata)

            data = (self.__x.xdata, self.__x.ydata)  # respect of plot data (interpol)
            plot = (self.__x.x, self.__x.y)  # respect of plot frame
            array = (idx_x[0], idx_y[0])  # respect of array indices
            data_exact = (idx_x[1], idx_y[1])  # respect of plot data (no interpol)

            span = (self.__xlim, self.__ylim)  # respect of plot data (interpol)
            self.__button_press_event(data, plot, array, data_exact, span)

    def __internal_xlim_changed(self, x):
        self.__xlim = self.axes.get_xlim()
        self.__internal_button_press_event()

    def __internal_ylim_changed(self, y):
        self.__ylim = self.axes.get_ylim()
        self.__internal_button_press_event()

    def get_toolbar(self):
        self.toolbar = NavigationToolbar(self, coordinates=False)
        return self.toolbar
