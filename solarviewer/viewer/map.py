from copy import copy

from astropy import units as u
from sunpy.map import Map

from solarviewer.app.plot import PlotWidget
from solarviewer.app.statusbar import StatusBarController
from solarviewer.config.base import ViewerController, DataType, ViewerType, ViewerConfig, DataModel
from solarviewer.config.ioc import RequiredFeature
from solarviewer.util import classproperty


class SunPyMapModel(DataModel):
    def __init__(self, s_map):
        self._plot_preferences = {"show_colorbar": False, "show_limb": False, "draw_contours": False,
                                  "draw_grid": False}
        self.map = s_map

        self.cmap = s_map.plot_settings.get("cmap", None)
        self.cmap_preferences = {"over": None, "under": None}
        self.norm = s_map.plot_settings.get("norm", None)
        self.interpolation = s_map.plot_settings.get("interpolation", None)
        self.origin = s_map.plot_settings.get("origin", None)

    def setData(self, data):
        self.map = Map(data, self.map.meta)

    @property
    def data(self):
        return self.map.data

    @property
    def title(self):
        try:
            return self.map.name
        except:
            return "Map"

    @property
    def plot_preferences(self):
        return self._plot_preferences


class MapViewerController(ViewerController):
    data_type = DataType.MAP
    viewer_type = ViewerType.MPL
    status_bar_ctrl: StatusBarController = RequiredFeature(StatusBarController.name)

    def __init__(self, model):
        ViewerController.__init__(self)

        self._model = model
        self._view = MapViewer(model)

        # add coordinates of mouse courser to status bar
        self.view.canvas.mpl_connect('motion_notify_event', self.onMapMotion)

    @classproperty
    def viewer_config(self) -> ViewerConfig:
        return ViewerConfig().setMenuPath("File\\Open SunPy Map\\MPL")

    @classmethod
    def fromFile(cls, file):
        s_map = Map(file)
        s_map.path = file

        model = SunPyMapModel(s_map)
        return cls(model)

    @classmethod
    def fromModel(cls, model):
        return cls(model)

    @property
    def view(self):
        return self._view

    @property
    def model(self) -> SunPyMapModel:
        return self._model

    def onMapMotion(self, event):
        if event.inaxes:
            message = event.inaxes.format_coord(event.xdata, event.ydata)
            self.status_bar_ctrl.setText(message)

    def updateModel(self, model):
        self._model = model
        self._view.model = model
        self._view.redraw()

    def getTitle(self):
        return self._model.title

    def redraw(self):
        self._view.redraw()


class MapViewer(PlotWidget):

    def __init__(self, model: SunPyMapModel):
        self.model = model
        PlotWidget.__init__(self)

    def draw(self):
        self.figure.clear()
        try:
            s_map = self.model.map
            ax = self.figure.add_subplot(111, projection=s_map)
            image = ax.imshow(self.model.data, cmap=self._initCMap(), norm=self.model.norm,
                              interpolation=self.model.interpolation, origin=self.model.origin)
            plot_preferences = self.model.plot_preferences
            if plot_preferences["show_colorbar"]:
                self.figure.colorbar(image)
            if plot_preferences["show_limb"]:
                s_map.draw_limb(axes=ax)
            if plot_preferences["draw_contours"]:
                s_map.draw_contours([10, 20, 30, 40, 50, 60, 70, 80, 90] * u.percent, axes=ax)
            if plot_preferences["draw_grid"]:
                s_map.draw_grid(grid_spacing=10 * u.deg, axes=ax)
        except Exception as ex:
            self.figure.clear()
            self.figure.text(0.5, 0.5, s="Error during rendering data: " + str(ex), ha="center", va="center")

    def _initCMap(self):
        cmap = copy(self.model.cmap)
        over = self.model.cmap_preferences["over"]
        under = self.model.cmap_preferences["under"]
        if over:
            cmap.set_over(over)
        if under:
            cmap.set_under(under)

        return cmap
