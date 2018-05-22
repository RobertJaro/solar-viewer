from matplotlib import pyplot as plt
from sunpy.map import Map

from solarviewer.app.plot import PlotWidget
from solarviewer.config.base import DataModel, DataType, ViewerType, ViewerController, ViewerConfig, Viewer
from solarviewer.util import classproperty
from solarviewer.viewer.util import MPLCoordinatesMixin


class CompositeMapModel(DataModel):
    c_id = 0

    def __init__(self, maps):
        self.maps = {self._generateId(): (map, self._defaultSettings()) for map in maps}

    @property
    def composite_map(self):
        comp_map = Map(composite=True)
        for i, (c_id, (m, settings)) in enumerate(self.maps.items()):
            comp_map.add_map(m, settings["zorder"], settings["alpha"] / 100)
            if settings["levels"]:
                comp_map.set_levels(i, sorted(settings["levels"]), True)
        return comp_map

    def _defaultSettings(self):
        settings = {"zorder": 0, "alpha": 50, "levels": False}
        return settings

    def _generateId(self):
        self.c_id += 1
        return self.c_id


class CompositeMapViewerController(ViewerController, MPLCoordinatesMixin):
    data_type = DataType.MAP_COMPOSITE
    viewer_type = ViewerType.MPL

    def __init__(self, model):
        ViewerController.__init__(self)

        self._model = model
        self._view = CompositeMapViewer()
        self._view.updateModel(model)

        MPLCoordinatesMixin.__init__(self)

    @classproperty
    def viewer_config(self) -> ViewerConfig:
        return ViewerConfig().setMenuPath("File/Open SunPy Composite Map/From File").setMultiFile(True)

    @classmethod
    def fromFile(cls, files):
        maps = [Map(file) for file in files]
        model = CompositeMapModel(maps)
        return cls(model)

    @classmethod
    def fromModel(cls, model):
        return cls(model)

    @property
    def model(self) -> DataModel:
        return self._model

    @property
    def view(self) -> Viewer:
        return self._view

    def updateModel(self, model):
        self._model = model
        self._view.updateModel(model)

    def getTitle(self):
        return "Composite Map"


class CompositeMapViewer(PlotWidget):

    def __init__(self):
        PlotWidget.__init__(self)

    def draw(self, model: CompositeMapModel):
        self.figure.clear()
        plt.figure(self.figure.number)
        axes = self.figure.gca()
        model.composite_map.plot(axes=axes, title="")
