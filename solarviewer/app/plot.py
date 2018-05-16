from abc import abstractmethod

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from qtpy import QtWidgets

from solarviewer.config.base import Viewer, DataModel
from solarviewer.ui.plot import Ui_Plot
from solarviewer.util import executeTask


class PlotWidget(Viewer):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_Plot()
        self.ui.setupUi(self)

        self.initMainCanvas()
        self.rendered.clear()

    def initMainCanvas(self):
        self.figure = plt.figure()
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
        self.rendered.clear()
        self.canvas.hide()
        self.ui.progress.show()
        executeTask(self._redraw, [], self._afterRedraw)

    def _redraw(self):
        self.draw(self._model)
        self.canvas.draw()

    def _afterRedraw(self):
        self.ui.progress.hide()
        self.canvas.show()
        self.rendered.set()

    @abstractmethod
    def draw(self, data_model: DataModel):
        raise NotImplementedError
