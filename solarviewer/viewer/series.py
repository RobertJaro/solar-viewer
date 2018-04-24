from sunpy.timeseries import TimeSeries

from solarviewer.app.plot import PlotWidget
from solarviewer.config.base import ViewerController, DataModel, ViewerConfig, DataType, ViewerType, Viewer
from solarviewer.util import classproperty
from solarviewer.viewer.util import MPLCoordinatesMixin


class TimeSeriesModel(DataModel):
    def __init__(self, time_series):
        self.title = "{} ({:%Y-%m-%d %H:%M:%S})".format(time_series.source.upper(), time_series.time_range.start)
        self.series = time_series


class TimeSeriesViewerController(ViewerController, MPLCoordinatesMixin):
    data_type = DataType.SERIES
    viewer_type = ViewerType.MPL

    def __init__(self, model: TimeSeriesModel):
        ViewerController.__init__(self)

        self._model = model
        self._view = TimeSeriesViewer(model)

        MPLCoordinatesMixin.__init__(self)

    @classmethod
    def fromFile(cls, file):
        series = TimeSeries(file)
        model = TimeSeriesModel(series)
        return cls(model)

    @classmethod
    def fromModel(cls, model):
        return cls(model)

    @classproperty
    def viewer_config(self) -> ViewerConfig:
        return ViewerConfig().setMenuPath("File\\Open SunPy Timeseries")

    @property
    def model(self) -> DataModel:
        return self._model

    @property
    def view(self) -> Viewer:
        return self._view

    def updateModel(self, model):
        self.model = model

    def getTitle(self) -> str:
        return self._model.title


class TimeSeriesViewer(PlotWidget):

    def __init__(self, model: TimeSeriesModel):
        self.series = model.series
        PlotWidget.__init__(self)

    def draw(self):
        ax = self.figure.gca()
        self.series.plot(axes=ax)
