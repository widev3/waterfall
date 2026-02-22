from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
from single_include import numpy as np
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar,
)


class Mpl2DPlotCanvas(FigureCanvasQTAgg):
    def __init__(self, labels: str | str = None):
        self.fig = Figure()
        self.__axes = self.fig.add_subplot(111)

        if labels:
            self.__axes.set_xlabel(labels[0])
            self.__axes.set_ylabel(labels[1])

        (self.__im,) = self.__axes.plot([], [])
        self.fig.tight_layout()
        self.__cursor = Cursor(
            self.__axes, horizOn=True, vertOn=True, color="black", linewidth=1
        )
        super().__init__(self.fig)

    def set_data(self, x, y):
        self.__im.set_xdata(x)
        self.__im.set_ydata(y)
        self.__axes.set_xlim(min(x), max(x))
        self.__axes.set_ylim(min(y), max(y))
        self.__set_ticks()
        self.fig.tight_layout()
        self.draw()

    def get_data(self):
        return (self.__im.get_xdata(), self.__im.get_ydata())

    def get_toolbar(self):
        self.toolbar = NavigationToolbar(self, coordinates=True)
        return self.toolbar

    def set_scale(self, x=None, y=None):
        if x:
            self.__axes.set_xscale(x)
        if y:
            self.__axes.set_yscale(y)

    def __set_ticks(self):
        self.xlim = self.__axes.get_xlim()
        mx = self.xlim[0]
        Mx = self.xlim[1]
        self.__axes.set_xticks(np.arange(mx, Mx, (Mx - mx) / 10))
        self.__axes.set_xticks(np.arange(mx, Mx, (Mx - mx) / 30), minor=True)

        self.ylim = self.__axes.get_ylim()
        my = self.ylim[0]
        My = self.ylim[1]
        self.__axes.set_yticks(np.arange(my, My, (My - my) / 10))
        self.__axes.set_yticks(np.arange(my, My, (My - my) / 30), minor=True)

        self.__axes.grid(which="minor", alpha=0.2)
        self.__axes.grid(which="major", alpha=0.5)
