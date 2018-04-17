from abc import abstractmethod
from threading import Thread

from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from qtpy import QtWidgets

from solarviewer.ui.plot import Ui_Plot


class PlotWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_Plot()
        self.ui.setupUi(self)

        self.initMainCanvas()

        self.redraw()

    def initMainCanvas(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.toolbar.setVisible(False)
        FigureCanvas.setSizePolicy(self.canvas,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self.canvas)
        self.canvas.hide()
        self.ui.verticalLayout.addWidget(self.canvas)

    def redraw(self):
        Thread(target=self._onRedraw).start()

    def _onRedraw(self):
        self.canvas.hide()
        self.ui.progress.show()
        self.draw()
        self.canvas.draw()
        self.ui.progress.hide()
        self.canvas.show()

    @abstractmethod
    def draw(self):
        raise NotImplementedError
