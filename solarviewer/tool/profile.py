from enum import Enum

import astropy.units as u
import numpy as np
from matplotlib.widgets import Cursor

from solarviewer.app.plot import PlotWidget
from solarviewer.config.base import ViewerController, ItemConfig, DataType, ViewerType
from solarviewer.config.impl import ViewerToolController
from solarviewer.ui.profile import Ui_Profile


class ProfileController(ViewerToolController):

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setTitle("Profile").setMenuPath("Tools/Profile").addSupportedData(
            DataType.MAP).addSupportedViewer(ViewerType.MPL)

    def setupContent(self, content_widget):
        self._ui = Ui_Profile()
        self._ui.setupUi(content_widget)
        self._ui.horizontal_radio.toggled.connect(lambda x: self.onModeChange(Mode.HORIZONTAL) if x else None)
        self._ui.vertical_radio.toggled.connect(lambda x: self.onModeChange(Mode.VERTICAL) if x else None)
        self._ui.free_radio.toggled.connect(lambda x: self.onModeChange(Mode.FREE_LINE) if x else None)
        self._ui.none_radio.toggled.connect(lambda x: self.onModeChange(Mode.NONE) if x else None)
        self._ui.reset_button.clicked.connect(lambda x: self._resetProfile())

        self.model = ProfileModel()

    def connect(self, viewer_ctrl: ViewerController):
        self.model.figure = viewer_ctrl.view.figure
        self.model.connection_id = viewer_ctrl.view.figure.canvas.mpl_connect('button_press_event', self.onFigureClick)
        self.cursor = Cursor(self.model.getAxes(), useblit=True, horizOn=False, vertOn=False)
        self.onModeChange(self.model.mode)
        self.model.map = viewer_ctrl.model.map

    def disconnect(self, viewer_ctrl: ViewerController):
        self._removeLine(False)
        self._removeCursor()
        viewer_ctrl.view.figure.canvas.mpl_disconnect(self.model.connection_id)

    def _removeCursor(self):
        if self.cursor:
            del self.cursor
            self.cursor = None

    def _removeLine(self, refresh=True):
        if self.model.line is None:
            return
        self.model.line.remove()
        self.model.line = None
        if refresh:
            self.model.getCanvas().draw()

    def _removeProfile(self):
        if self.model.profile is None:
            return
        self.model.profile.deleteLater()
        self.model.profile = None

    def onModeChange(self, mode):
        self.cursor.horizOn = mode is Mode.HORIZONTAL
        self.cursor.vertOn = mode is Mode.VERTICAL
        self.model.mode = mode

    def _resetProfile(self):
        self.model.points = []
        self._removeLine()
        self._removeProfile()

    def onFigureClick(self, event):
        mode = self.model.mode
        if mode is Mode.NONE:
            return
        self._removeProfile()
        coordinates = self._extractCoordinates(self.model.map, event)
        if mode is Mode.FREE_LINE:
            self.model.points.append([coordinates[0], coordinates[1]])
            self._drawFreeLine()
            if len(self.model.points) <= 1:
                return
            profile_view = FreeLineProfilePanel(self.model.map, self.model.points)
        if mode is Mode.VERTICAL:
            profile_view = VerticalProfilePanel(self.model.map, coordinates)
        if mode is Mode.HORIZONTAL:
            profile_view = HorizontalProfilePanel(self.model.map, coordinates)
        self.model.profile = profile_view
        self._ui.profile_box.layout().addWidget(profile_view)

    def _drawFreeLine(self):
        x_ax, y_ax = np.transpose(self.model.points)
        self._removeLine(False)
        self.model.line = self.model.getAxes().plot(x_ax, y_ax, "-o", color="r")[0]
        self.model.getCanvas().draw()

    def _extractCoordinates(self, sotMap, event):
        x = int(np.rint(event.xdata))
        y = int(np.rint(event.ydata))
        coord = sotMap.pixel_to_world(event.xdata * u.pixel, event.ydata * u.pixel)
        return [x, y, coord.Tx.value, coord.Ty.value]


class ProfileModel:
    def __init__(self):
        self.enabled = None
        self.mode = Mode.NONE
        self.points = []
        self.line = None
        self.profile = None
        self.connection_id = None
        self.map = None
        self.figure = None

    def getAxes(self):
        return self.figure.axes[0]

    def getCanvas(self):
        return self.figure.canvas


class Mode(Enum):
    NONE = "None"
    VERTICAL = "Vertical"
    HORIZONTAL = "Horizontal"
    FREE_LINE = "Free Line"


# only valid for non-rotated
class VerticalProfilePanel(PlotWidget):
    def __init__(self, map, coordinates):
        PlotWidget.__init__(self)
        self.updateModel((map, coordinates))

    def draw(self, model):
        map, coordinates = model
        x, y, x_data, y_data = coordinates
        self.createVerticalProfile(map, x, y, x_data, y_data)

    def createVerticalProfile(self, map, x, y, x_data, y_data):
        vertical_data = np.transpose(map.data)[x]
        yrange_min = map.yrange.min().to(u.arcsec).value
        yrange_max = map.yrange.max().to(u.arcsec).value
        y_scale = map.scale[1].to(u.arcsec / u.pix).value
        x_axis = np.arange(yrange_min, yrange_max, y_scale)[:len(vertical_data)]  # crop overlap
        ax = self.figure.add_subplot(111)
        ax.plot(x_axis, vertical_data, zorder=1)
        ax.scatter([y_data], [vertical_data[y]], color="red", zorder=2)  # mark selected pixel
        ax.xaxis.set_label_text("Y-position [arcsec]")
        ax.set_title("Longitude: %f arcsec" % x_data)


# only valid for non-rotated
class HorizontalProfilePanel(PlotWidget):
    def __init__(self, map, coordinates):
        PlotWidget.__init__(self)
        self.updateModel((map, coordinates))

    def draw(self, model):
        map, coordinates = model
        x, y, x_data, y_data = coordinates
        self.createHorizontalProfile(map, x, y, x_data, y_data)

    def createHorizontalProfile(self, map, x, y, x_data, y_data):
        horizontal_data = map.data[y]
        xrange_min = map.xrange.min().to(u.arcsec).value
        xrange_max = map.xrange.max().to(u.arcsec).value
        x_scale = map.scale[0].to(u.arcsec / u.pix).value
        x_axis = np.arange(xrange_min, xrange_max, x_scale)
        ax = self.figure.add_subplot(111)
        ax.plot(x_axis, horizontal_data, zorder=1)
        ax.scatter([x_data], [horizontal_data[x]], color="red", zorder=2)  # mark selected pixel
        ax.xaxis.set_label_text("X-position [arcsec]")
        ax.set_title("Latitude: %f arcsec" % y_data)


class FreeLineProfilePanel(PlotWidget):
    def __init__(self, map, points):
        values = []
        x0 = None
        y0 = None
        for x1, y1 in points:
            if x0 is not None and y0 is not None:
                length = int(np.hypot(x1 - x0, y1 - y0))
                x, y = np.linspace(x0, x1, length), np.linspace(y0, y1, length)
                # Extract the values along the line
                values = np.append(values, map.data[y.astype(np.int), x.astype(np.int)])
            x0 = x1
            y0 = y1
        PlotWidget.__init__(self)
        self.updateModel(values)

    def draw(self, values):
        if len(values) <= 1:
            return
        ax = self.figure.add_subplot(111)
        ax.plot(values)
        ax.get_xaxis().set_ticks([])
