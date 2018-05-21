from copy import copy

from astropy import units as u
from sunpy.map import Map

from solarviewer.app.plot import PlotWidget
from solarviewer.config.base import ViewerController, DataType, ViewerType, ViewerConfig, DataModel, Viewer
from solarviewer.util import classproperty
from solarviewer.viewer.util import MPLCoordinatesMixin


class MapModel(DataModel):
    def __init__(self, s_map):
        self.plot_preferences = {"show_colorbar": False, "show_limb": False, "contours": False,
                                 "draw_grid": False}
        self.map = s_map

        self._cmap = s_map.plot_settings.get("cmap", None)
        self.cmap_preferences = {"over": None, "under": None}
        self.norm = s_map.plot_settings.get("norm", None)
        self.interpolation = s_map.plot_settings.get("interpolation", None)
        self.origin = s_map.plot_settings.get("origin", None)

    @property
    def data(self):
        return self.map.data

    def setData(self, data):
        self.map._data = data

    @property
    def title(self):
        try:
            return self.map.name
        except:
            return "Map"

    def setCMap(self, cmap):
        self._cmap = cmap

    @property
    def cmap(self):
        cmap = copy(self._cmap)
        over = self.cmap_preferences["over"]
        under = self.cmap_preferences["under"]
        if over:
            cmap.set_over(over)
        if under:
            cmap.set_under(under)
        return cmap


class MapViewerController(ViewerController, MPLCoordinatesMixin):
    data_type = DataType.MAP
    viewer_type = ViewerType.MPL

    def __init__(self, model):
        ViewerController.__init__(self)

        self._model = model
        self._view = MapViewer()
        self._view.updateModel(model)

        MPLCoordinatesMixin.__init__(self)

    @classproperty
    def viewer_config(self) -> ViewerConfig:
        return ViewerConfig().setMenuPath("File/Open SunPy Map/MPL")

    @classmethod
    def fromFile(cls, file):
        s_map = Map(file)
        s_map.path = file

        model = MapModel(s_map)
        return cls(model)

    @classmethod
    def fromModel(cls, model):
        return cls(model)

    @property
    def view(self) -> Viewer:
        return self._view

    @property
    def model(self) -> MapModel:
        return self._model

    def updateModel(self, model):
        self._model = model
        self._view.updateModel(model)

    def getTitle(self):
        return self._model.title

    def redraw(self):
        self._view.redraw()

    def getZoomedMap(self):
        x = self.view.figure.axes[0].get_xlim()
        y = self.view.figure.axes[0].get_ylim()
        bl = [x[0], y[0]]
        tr = [x[1], y[1]]
        current_map = self.model.map
        sub_map = current_map.submap(bl * u.pixel, tr * u.pixel)
        sub_map.plot_settings = current_map.plot_settings  # preserve settings
        return sub_map

    def getZoomedData(self):
        return self.getZoomedMap().data


class MapViewer(PlotWidget):

    def __init__(self):
        PlotWidget.__init__(self)

    def draw(self, model):
        self.figure.clear()
        try:
            s_map = model.map
            ax = self.figure.add_subplot(111, projection=s_map)
            image = ax.imshow(model.data, cmap=model.cmap, norm=model.norm,
                              interpolation=model.interpolation, origin=model.origin)
            plot_preferences = model.plot_preferences
            if plot_preferences["show_colorbar"]:
                self.figure.colorbar(image)
            if plot_preferences["show_limb"]:
                s_map.draw_limb(axes=ax)
            if plot_preferences["contours"]:
                levels = sorted(plot_preferences["contours"])
                s_map.draw_contours(levels * u.percent, axes=ax)
            if plot_preferences["draw_grid"]:
                s_map.draw_grid(grid_spacing=10 * u.deg, axes=ax)
        except Exception as ex:
            self.figure.clear()
            self.figure.text(0.5, 0.5, s="Error during rendering data: " + str(ex), ha="center", va="center")
