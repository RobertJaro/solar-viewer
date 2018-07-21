from matplotlib import pyplot as plt
from radiospectra.sources import CallistoSpectrogram
from sunpy.time import get_day

from solarviewer.app.plot import PlotWidget
from solarviewer.config.base import DataModel, ViewerController, Viewer, ViewerConfig, DataType, ViewerType
from solarviewer.viewer.util import MPLCoordinatesMixin


class CallistoModel(DataModel):

    def __init__(self, spectrogram: CallistoSpectrogram):
        self.spectrogram = spectrogram
        self.vmin = None
        self.vmax = None
        self.colorbar = True
        self.linear = True
        self.substract_background = False


class CallistoViewer(PlotWidget):

    def draw(self, data_model: CallistoModel):
        plt.figure(self.figure.number)  # TODO: replace workaround
        img = data_model.spectrogram
        if data_model.substract_background:
            img = img.subtract_bg()
        img.plot(colorbar=data_model.colorbar, vmin=data_model.vmin, vmax=data_model.vmax,
                 linear=data_model.linear, showz=True)


class CallistoViewerController(ViewerController, MPLCoordinatesMixin):
    viewer_config = ViewerConfig().setMenuPath("File/Open Spectrogram/Callisto/From File").setMultiFile(True)

    def __init__(self, model):
        ViewerController.__init__(self)

        self._model: CallistoModel = model
        self._view: CallistoViewer = CallistoViewer()
        self._view.updateModel(model)

        MPLCoordinatesMixin.__init__(self)

    @classmethod
    def fromFile(cls, files) -> 'ViewerController':
        list = [CallistoSpectrogram.read(file) for file in files]
        spectrogram = CallistoSpectrogram.join_many(list)
        model = CallistoModel(spectrogram)
        return cls(model)

    @classmethod
    def fromModel(cls, model: DataModel) -> 'ViewerController':
        return cls(model)

    @classmethod
    def fromSpectrogram(cls, spectrogram):
        model = CallistoModel(spectrogram)
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

    def getTitle(self) -> str:
        img = self._model.spectrogram
        return ' '.join(
            [get_day(img.start).strftime("%d %b %Y"), 'Radio flux density', '(' + ', '.join(img.instruments) + ')', ])

    @property
    def data_type(self) -> str:
        return DataType.SPECTROGRAM

    @property
    def viewer_type(self) -> str:
        return ViewerType.MPL
