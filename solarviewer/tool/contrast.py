import numpy as np
from PyQt5.QtGui import QColor
from qtpy import QtWidgets

from solarviewer.app.plot import PlotWidget
from solarviewer.config.base import ItemConfig, ViewerType, DataType, DataModel
from solarviewer.config.impl import DataToolController
from solarviewer.ui.contrast import Ui_Contrast
from solarviewer.viewer.map import SunPyMapModel, MapViewerController


class ContrastController(DataToolController):

    def __init__(self):
        self._view: QtWidgets.QWidget = None
        self._ui: Ui_Contrast = None
        self._hist: ContrastHist = None
        self._map = None

        DataToolController.__init__(self)

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setTitle("Contrast Adjustment").setMenuPath("Tools\\Contrast").addSupportedViewer(
            ViewerType.MPL).addSupportedData(DataType.MAP)

    def setupContent(self, content_widget):
        self._view = content_widget
        self._ui = Ui_Contrast()
        self._ui.setupUi(content_widget)

        self._ui.color_above.setColor(QColor("blue"))
        self._ui.color_below.setColor(QColor("red"))
        self._ui.histo_plot.setVisible(False)
        self._ui.histo_button.clicked.connect(self.toggleHist)

    def onDataChanged(self, viewer_ctrl: MapViewerController):
        if self._hist:
            self._ui.histo_button.click()
        self._map = viewer_ctrl.model.map
        self._ui.spin_max.setValue(100)

    def modifyData(self, data_model: SunPyMapModel) -> DataModel:
        return data_model

    def toggleHist(self):
        if self._hist:
            self._hist.close()
            self._hist = None
            return
        self._hist = ContrastHist(self._map)
        self._ui.histo_plot.layout().addWidget(self._hist)


class ContrastHist(PlotWidget):
    def __init__(self, map):
        self.map = map
        self.ax = None
        PlotWidget.__init__(self)

    def draw(self):
        min_value = np.nanmin(self.map.data)
        max_value = np.nanmax(self.map.data)

        self.ax = self.figure.add_subplot(1, 1, 1)
        self.ax.hist(self.map.data.ravel(), bins=300, range=(min_value, max_value), fc='k', ec='k')

    def plotLine(self, x):
        line = self.ax.axvline(x)
        self.canvas.draw()
        return line
