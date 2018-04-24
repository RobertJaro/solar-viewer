import sip

import astropy.units as u
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFileDialog
from matplotlib.widgets import Cursor
from qtpy import QtWidgets, QtGui

from solarviewer.config.base import ItemConfig, ViewerController, DataType, ViewerType
from solarviewer.config.impl import ViewerToolController
from solarviewer.ui.selection import Ui_Selection


class SelectionModel:

    def __init__(self):
        self.view = None
        self.map = None
        self.points = []
        self.fig_points = []
        self.marker_colour = QColor(255, 0, 0)
        self.text_colour = QColor(0, 0, 255)

    def getCanvas(self):
        return self.view.figure.canvas

    def getAxes(self):
        return self.view.figure.axes[0]

    def getMarkerColour(self):
        return (self.marker_colour.red() / 255, self.marker_colour.green() / 255, self.marker_colour.blue() / 255)

    def getTextColour(self):
        return (self.text_colour.red() / 255, self.text_colour.green() / 255, self.text_colour.blue() / 255)

    def isEnabled(self):
        return self.view is not None and not sip.isdeleted(self.view)


class SelectionController(ViewerToolController):

    def __init__(self):
        self.model = SelectionModel()
        self.cursor = None
        self.connection_id = None

        ViewerToolController.__init__(self)

    def setupContent(self, content_widget):
        self._view = content_widget
        self._ui = Ui_Selection()
        self._ui.setupUi(self._view)
        self.table = self._ui.selection_table
        self._ui.marker_color.setColor(self.model.marker_colour)
        self._ui.text_color.setColor(self.model.text_colour)

        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        self._ui.import_button.clicked.connect(self.onImport)
        self._ui.export_button.clicked.connect(self.onExport)
        self._ui.clear_button.clicked.connect(self.onClear)
        self._ui.marker_color.colorChanged.connect(self.onStyleChange)
        self._ui.text_color.colorChanged.connect(self.onStyleChange)

        QtWidgets.QShortcut(QtGui.QKeySequence(Qt.Key_Delete, Qt.Key_Backspace), self.table, self.onRemoveSelected)

    def manageViewerController(self, viewer_ctrl: ViewerController):
        self.clearViewerController()
        self.model.view = viewer_ctrl.view
        self.model.map = viewer_ctrl.model.map
        self._initListener()

    def clearViewerController(self):
        self._removeCursor()
        self.onClear()

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setTitle("Highlight Values").setMenuPath("Tools\\Highlight Values").addSupportedData(
            DataType.MAP).addSupportedViewer(ViewerType.MPL)

    def onFigureClick(self, event):
        if self.model.view.toolbar._active is not None:
            return
        coord = self.model.map.pixel_to_world(event.xdata * u.pixel, event.ydata * u.pixel)
        data = self.model.map.data[int(np.rint(event.ydata)), int(np.rint(event.xdata))]
        self.model.points.append([event.xdata * u.pix, event.ydata * u.pix, coord.Tx,
                                  coord.Ty, data])
        index = self.onAdd(coord.Tx, coord.Ty, data)
        self._drawPoint(event.xdata, event.ydata, index)

    def onAdd(self, x, y, data):
        row_pos = self.table.rowCount()
        self.table.insertRow(row_pos)
        self.table.setItem(row_pos, 0, QtWidgets.QTableWidgetItem("{}".format(x)))
        self.table.setItem(row_pos, 1, QtWidgets.QTableWidgetItem("{}".format(y)))
        self.table.setItem(row_pos, 2, QtWidgets.QTableWidgetItem("{}".format(data)))
        return row_pos

    def onClear(self):
        self.model.points.clear()
        for point in self.model.fig_points:
            point.remove()
        self.model.fig_points = []
        self.table.setRowCount(0)
        if self.model.isEnabled():
            self.model.getCanvas().draw()

    def onExport(self, evt):
        path, _ = QFileDialog.getSaveFileName(None, filter="CSV files (*.csv);;Text files (*.txt)")
        if not path:
            return
        data = [["{}".format(xp), "{}".format(yp), "{}".format(x), "{}".format(y), "{}".format(d)]
                for xp, yp, x, y, d in self.model.points]
        np.savetxt(path, data, delimiter=";", header="x_pixel;y_pixel;x;y;resources", fmt="%s")

    def onImport(self, evt):
        path, _ = QFileDialog.getOpenFileName(None, filter="CSV files (*.csv);;Text files (*.txt)")
        if not path:
            return
        self.onClear()
        data = np.loadtxt(path, dtype="str", delimiter=";").reshape(-1, 5)
        self.model.points = [
            [self._parseUnitString(xp), self._parseUnitString(yp), self._parseUnitString(x), self._parseUnitString(y),
             float(d)] for xp, yp, x, y, d in data]
        self._redrawPoints()

    def onRemoveSelected(self):
        for row in set([i.row() for i in self.table.selectedIndexes()]):
            self.table.removeRow(row)
            del self.model.points[row]
        self._redrawPoints()

    def onStyleChange(self):
        self.model.marker_colour = self._ui.marker_color.color()
        self.model.text_colour = self._ui.text_color.color()
        self._redrawPoints()

    def _initListener(self):
        self._removeCursor()
        ax = self.model.getAxes()
        self.connection_id = self.model.getCanvas().mpl_connect('button_press_event', self.onFigureClick)
        self.cursor = Cursor(ax, useblit=True, horizOn=True, vertOn=True)

    def _drawPoint(self, x, y, i, refresh=True):
        self.model.fig_points.append(self.model.getAxes().scatter(x, y, color=self.model.getMarkerColour()))
        self.model.fig_points.append(self.model.getAxes().annotate(i + 1, (x, y), color=self.model.getTextColour()))
        if refresh:
            self.model.getCanvas().draw()

    def _drawPoints(self):
        for p in self.model.points:
            i = self.onAdd(p[2], p[3], p[4])
            self._drawPoint(p[0].value, p[1].value, i, False)
        self.model.getCanvas().draw()

    def _redrawPoints(self):
        for point in self.model.fig_points:
            point.remove()
        self.model.fig_points = []
        self.table.setRowCount(0)
        self._drawPoints()

    def _parseUnitString(self, s):
        v, unit = s.split(" ")
        return float(v) * u.Unit(unit)

    def _removeCursor(self):
        if self.connection_id:
            self.model.getCanvas().mpl_disconnect(self.connection_id)
            self.connection_id = None
        if self.cursor:
            del self.cursor
            self.cursor = None
