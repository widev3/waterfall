import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar,
)


class Mpl2DPlotCanvas(FigureCanvasQTAgg):
    def __init__(self, labels: str | str = None):
        self.__fig = Figure()
        self.__axes = self.__fig.add_subplot(111)

        if labels:
            self.__axes.set_xlabel(labels[0])
            self.__axes.set_ylabel(labels[1])

        (self.__im,) = self.__axes.plot([], [])
        self.__fig.tight_layout()
        super().__init__(self.__fig)

    def set_data(self, x, y):
        mx = min(x)
        Mx = max(x)
        self.__axes.set_xticks(np.arange(mx, Mx, (Mx - mx) / 10))
        self.__axes.set_xticks(np.arange(mx, Mx, (Mx - mx) / 30), minor=True)

        my = min(y)
        My = max(y)
        self.__axes.set_yticks(np.arange(my, My, (My - my) / 10))
        self.__axes.set_yticks(np.arange(my, My, (My - my) / 30), minor=True)

        self.__axes.grid(which="minor", alpha=0.2)
        self.__axes.grid(which="major", alpha=0.5)

        self.__im.set_xdata(x)
        self.__im.set_ydata(y)
        self.__axes.set_xlim(mx, Mx)
        self.__axes.set_ylim(my, My)
        self.__fig.tight_layout()
        self.draw()

    def get_toolbar(self):
        self.toolbar = NavigationToolbar(self, coordinates=False)
        return self.toolbar
