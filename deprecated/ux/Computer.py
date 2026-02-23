from deprecated.single_include import numpy as np
from ux.Mpl2DPlotCanvas import Mpl2DPlotCanvas


class Computer:
    def __init__(self, ui, dialog, args=None):
        self.ui = ui
        self.dialog = dialog
        self.args = args

        self.ui.lineEdit.returnPressed.connect(self.__lineEditReturnPressed)

        self.__plot = Mpl2DPlotCanvas(labels=("frequency", "intensity"))
        self.ui.verticalLayout.addWidget(self.__plot.get_toolbar())
        self.ui.verticalLayout.addWidget(self.__plot)

    def __lineEditReturnPressed(self):
        eq = self.ui.lineEdit.text()
        for c in range(ord("A"), ord("Z")):
            expr = f'np.array(self.args["memory"][{c-65}][0][1])'
            eq = eq.replace(chr(c), expr)

        result = eval(eq)
        self.__plot.set_data(self.args["memory"][0][0][0], result)
