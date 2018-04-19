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
        self._hist: _ContrastHist = None
        self._model = ContrastModel()

        DataToolController.__init__(self)

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setTitle("Contrast Adjustment").setMenuPath("Tools\\Contrast").addSupportedViewer(
            ViewerType.MPL).addSupportedData(DataType.MAP)

    def setupContent(self, content_widget):
        self._view = content_widget
        self._ui = Ui_Contrast()
        self._ui.setupUi(content_widget)

        self._ui.histo_plot.setVisible(False)
        self._ui.histo_button.clicked.connect(self.toggleHist)
        self._ui.min_max_button.clicked.connect(self._onAdjustMinMax)
        self._ui.average_button.clicked.connect(self._onAdjustAvg)
        self._ui.peak_button.clicked.connect(self._onAdjustPeak)
        self._ui.spin_min.valueChanged.connect(self._onMin)
        self._ui.spin_max.valueChanged.connect(self._onMax)

    def onDataChanged(self, viewer_ctrl: MapViewerController):
        if self._hist:
            self._ui.histo_button.click()
        m = viewer_ctrl.model
        self._model.min = m.norm.vmin if m.norm.vmin else 0
        self._model.max = m.norm.vmax if m.norm.vmax else 0
        self._model.map = m.map
        self._applyValues()

        over = viewer_ctrl.model.cmap_preferences["over"]
        under = viewer_ctrl.model.cmap_preferences["under"]
        over = QColor(over) if over else None
        under = QColor(under) if under else None
        self._ui.over_color.setColor(over)
        self._ui.over_check.setChecked(over is not None)
        self._ui.under_color.setColor(under)
        self._ui.under_check.setChecked(under is not None)
        self._ui.color_clipped.setChecked(over is not None or under is not None)

    def modifyData(self, data_model: SunPyMapModel) -> DataModel:
        data_model.norm.vmin = self._model.min
        data_model.norm.vmax = self._model.max

        data_model.cmap_preferences["over"] = None
        data_model.cmap_preferences["under"] = None
        if self._ui.color_clipped.isChecked():
            if self._ui.over_check.isChecked():
                c = self._ui.over_color.color()
                data_model.cmap_preferences["over"] = c.name() if c else None
            if self._ui.under_check.isChecked():
                c = self._ui.under_color.color()
                data_model.cmap_preferences["under"] = c.name() if c else None

        return data_model

    def toggleHist(self):
        if self._hist:
            self._hist.close()
            self._hist = None
            return
        self._hist = _ContrastHist(self._model.map, self._drawLines)
        self._ui.histo_plot.layout().addWidget(self._hist)

    def _applyValues(self):
        min = np.nanmin(self._model.data)
        max = np.nanmax(self._model.data)
        self._ui.spin_min.setMinimum(min)
        self._ui.spin_min.setMaximum(max)
        self._ui.spin_max.setMinimum(min)
        self._ui.spin_max.setMaximum(max)

        v_min = self._model.min
        v_max = self._model.max
        self._ui.spin_min.setValue(v_min)
        self._ui.spin_max.setValue(v_max)

        self._drawLines()

    def _drawLines(self):
        if not self._hist:
            return
        self._drawMinLine()
        self._drawMaxLine()

    def _drawMaxLine(self, *args):
        if self._model.max_line is not None:
            self._model.max_line.remove()
        self._model.max_line = self._hist.plotLine(x=self._model.max)

    def _drawMinLine(self, *args):
        if self._model.min_line is not None:
            self._model.min_line.remove()
        self._model.min_line = self._hist.plotLine(x=self._model.min)

    def _onMin(self, val):
        self._model.min = val
        if self._hist:
            self._drawMinLine()

    def _onMax(self, val):
        self._model.max = val
        if self._hist:
            self._drawMaxLine()

    def _onAdjustMinMax(self):
        data = self._model.data
        self._model.min = np.nanmin(data)
        self._model.max = np.nanmax(data)
        self._applyValues()

    def _onAdjustAvg(self):
        data = self._model.data
        self._model.min = np.nanmin(data)
        self._model.max = np.nanmean(data) + 3 * np.nanstd(data)
        self._applyValues()

    def _onAdjustPeak(self):
        data = self._model.data
        hist = np.histogram(data, 300, range=(np.nanmin(data), np.nanmax(data)))
        peak = hist[1][hist[0].argmax()]
        width = 3 * np.nanstd(data)
        self._model.min = peak - width
        self._model.max = peak + width
        self._applyValues()


class _ContrastHist(PlotWidget):
    def __init__(self, map, init):
        self.data = map.data
        self.ax = None
        PlotWidget.__init__(self)
        self.init = init

    def draw(self):
        min_value = np.nanmin(self.data)
        max_value = np.nanmax(self.data)

        self.ax = self.figure.add_subplot(1, 1, 1)
        self.ax.hist(self.data.ravel(), bins=300, range=(min_value, max_value), fc='k', ec='k')
        self.init()  # workaround for plot line delay

    def plotLine(self, x):
        line = self.ax.axvline(x)
        self.canvas.draw()
        return line


class ContrastModel:
    def __init__(self):
        self.min = None
        self.max = None
        self.min_line = None
        self.max_line = None
        self.map = None

    @property
    def data(self):
        return self.map.data
