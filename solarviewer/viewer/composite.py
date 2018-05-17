from matplotlib import pyplot as plt
from sunpy.map import Map

from solarviewer.app.plot import PlotWidget
from solarviewer.config.base import DataModel, DataType, ViewerType, ViewerController, ViewerConfig, Viewer
from solarviewer.util import classproperty
from solarviewer.viewer.util import MPLCoordinatesMixin


class CompositeMapModel(DataModel):
    def __init__(self, c_map):
        self.composite_map = c_map


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
        comp_map = Map(files, composite=True)
        a = 0.5
        for i in range(len(files)):
            comp_map.set_alpha(i, a)

        model = CompositeMapModel(comp_map)
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
