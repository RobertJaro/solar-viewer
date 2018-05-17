import os

from astropy.io import fits
from astropy.wcs import WCS
from matplotlib.colors import Normalize

from solarviewer.app.plot import PlotWidget
from solarviewer.config.base import ViewerController, DataType, ViewerType, ViewerConfig, DataModel, Viewer
from solarviewer.util import classproperty
from solarviewer.viewer.util import MPLCoordinatesMixin


class Plain2DModel(DataModel):
    def __init__(self, data):
        self._data = data
        self.plot_settings = {"norm": Normalize(vmin=data.min(), vmax=data.max()), "cmap": "gray"}
        self.wcs = None

    @property
    def data(self):
        return self._data


class AstroPyViewer(PlotWidget):

    def __init__(self):
        PlotWidget.__init__(self)

    def draw(self, model):
        try:
            self.figure.clear()
            plot_settings = model.plot_settings
            self.ax = self.figure.add_subplot(111, projection=model.wcs)
            image = self.ax.imshow(model.data, **plot_settings)
        except Exception as ex:
            self.figure.clear()
            self.figure.text(0.5, 0.5, s="Error during rendering data: " + str(ex), ha="center", va="center")


class AstroPyViewerController(ViewerController, MPLCoordinatesMixin):
    data_type = DataType.PLAIN_2D
    viewer_type = ViewerType.MPL

    def __init__(self, model):
        ViewerController.__init__(self)

        self._model = model
        self._view = AstroPyViewer()
        self._view.updateModel(model)

        MPLCoordinatesMixin.__init__(self)

    @classproperty
    def viewer_config(self) -> ViewerConfig:
        return ViewerConfig().setMenuPath("File/Open 2D FITS/MPL")

    @classmethod
    def fromFile(cls, file):
        hdu = cls._getFitsHDU(file)
        model = Plain2DModel(hdu.data)
        model.wcs = WCS(hdu.header)
        model.title = os.path.basename(file)

        return cls(model)

    @classmethod
    def fromModel(cls, model):
        return cls(model)

    def getTitle(self) -> str:
        return self._model.title

    def getView(self):
        return self.view

    def getContent(self):
        return self.model

    def setContent(self, model):
        self.model = model
        self.view.model = model

    @property
    def model(self) -> DataModel:
        return self._model

    @property
    def view(self) -> Viewer:
        return self._view

    def updateModel(self, model):
        self._model = model
        self._view.updateModel(model)

    @classmethod
    def _getFitsHDU(cls, path):
        hdu_list = fits.open(path)
        hdu_list.verify("silentfix")
        for hdu in hdu_list:
            if hdu.data is not None:
                return hdu
