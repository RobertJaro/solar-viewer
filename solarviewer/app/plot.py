from abc import abstractmethod
from threading import Thread

from PyQt5.QtCore import pyqtSignal
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from qtpy import QtWidgets, QtCore

from solarviewer.config.base import Viewer, DataModel
from solarviewer.ui.plot import Ui_Plot


class PlotWidget(Viewer):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_Plot()
        self.ui.setupUi(self)

        self.initMainCanvas()

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

    def updateModel(self, model: DataModel):
        self._model = model
        self.redraw()

    def redraw(self):
        self.rendered = False
        self.canvas.hide()
        self.ui.progress.show()
        thread = RedrawThread(self, self._model)
        thread.finished.connect(self._afterRedraw)
        thread.start()

    def _afterRedraw(self):
        self.ui.progress.hide()
        self.canvas.show()
        self.rendered = True
        self.finished.emit()

    @abstractmethod
    def draw(self, data_model: DataModel):
        raise NotImplementedError


class RedrawThread(QtCore.QObject, Thread):
    finished = pyqtSignal()

    def __init__(self, plot_widget, model):
        self.plot_widget = plot_widget
        self.model = model

        QtCore.QObject.__init__(self)
        Thread.__init__(self)

    def run(self):
        self.plot_widget.draw(self.model)
        self.plot_widget.canvas.draw()
        self.finished.emit()
