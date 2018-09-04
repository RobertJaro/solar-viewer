import os
from copy import copy

from astropy.io.fits import getdata, getheader
from astropy.wcs import WCS
from ndcube import NDCube, NDCubeSequence

from solarviewer.app.plot import PlotWidget
from solarviewer.config.base import ViewerController, Viewer, DataModel, ViewerConfig, DataType, ViewerType
from solarviewer.viewer.util import MPLCoordinatesMixin


class NDCubeModel(DataModel):
    def __init__(self, cube, files):
        self._cmap = None
        self.cmap_preferences = {"over": None, "under": None}
        self.image_axes = [-1, -2]

        self.cube = cube
        if len(files) == 1:
            self.title = "NDCube {}".format(os.path.basename(files[0]))
        else:
            self.title = "NDCubeSequence ({} cubes)".format(len(files))

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

    def setCMap(self, cmap):
        self._cmap = cmap


class NDCubeView(PlotWidget):

    def draw(self, data_model: NDCubeModel):
        self.figure.clear()
        data_model.cube.plot(fig=self.figure, cmap=data_model.cmap, image_axes=data_model.image_axes)


class NDCubeViewerController(ViewerController, MPLCoordinatesMixin):
    viewer_config = ViewerConfig().setMenuPath("File/Open NDCube").setMultiFile(True)

    def __init__(self, model):
        ViewerController.__init__(self)

        self._model = model
        self._view = NDCubeView()
        self._view.updateModel(self._model)

        MPLCoordinatesMixin.__init__(self)

    @classmethod
    def fromFile(cls, files: str) -> 'ViewerController':
        cubes = [NDCube(getdata(f), WCS(getheader(f))) for f in files]
        if len(cubes) == 1:
            cube = cubes[0]
        else:
            cube = NDCubeSequence(cubes)
        model = NDCubeModel(cube, files)
        return cls(model)

    @classmethod
    def fromModel(cls, model: DataModel) -> 'ViewerController':
        return cls(model)

    @property
    def model(self) -> DataModel:
        return self._model

    @property
    def view(self) -> Viewer:
        return self._view

    def updateModel(self, model):
        self._view.updateModel(model)
        self._model = model

    def getTitle(self) -> str:
        return str(self._model.title)

    @property
    def data_type(self) -> str:
        return DataType.NDCUBE

    @property
    def viewer_type(self) -> str:
        return ViewerType.NDCUBE
