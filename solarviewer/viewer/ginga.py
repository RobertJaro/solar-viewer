from qtpy import QtWidgets, QtCore
from sunpy.map import Map

from solarviewer.config.base import DataType, ViewerType, ViewerController, Viewer, DataModel, ViewerConfig
from solarviewer.util import classproperty
from solarviewer.viewer.map import MapModel


class GingaMapViewerController(ViewerController):
    data_type = DataType.MAP
    viewer_type = ViewerType.GINGA

    def __init__(self, model):
        ViewerController.__init__(self)

        self._model = model
        self._view = GingaViewer()
        self._view.updateModel(model)

    @classmethod
    def fromFile(cls, file):
        s_map = Map(file)
        s_map.path = file

        model = MapModel(s_map)
        return cls(model)

    @classmethod
    def fromModel(cls, model):
        return cls(model)

    @classproperty
    def viewer_config(self) -> ViewerConfig:
        return ViewerConfig().setMenuPath("File/Open SunPy Map/Ginga").addRequiredPackage("ginga")

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
        return self._model.title


class GingaViewer(Viewer):
    def __init__(self):
        Viewer.__init__(self)

        from ginga.qtw.ImageViewCanvasQt import ImageViewCanvas
        fi = ImageViewCanvas(render='widget')
        fi.enable_autocuts('on')
        fi.set_autocut_params('zscale')
        fi.enable_autozoom('on')
        fi.set_bg(0.2, 0.2, 0.2)
        fi.ui_setActive(True)
        fi.enable_draw(False)
        self.fitsimage = fi

        bd = fi.get_bindings()
        bd.enable_all(True)

        w = fi.get_widget()
        w.resize(512, 512)

        vbox = QtWidgets.QVBoxLayout()
        vbox.setContentsMargins(QtCore.QMargins(2, 2, 2, 2))
        vbox.setSpacing(1)
        vbox.addWidget(w, stretch=1)
        self.setLayout(vbox)

    def updateModel(self, model: DataModel):
        from ginga import AstroImage
        image = AstroImage.AstroImage()
        image.load_data(model.data)
        self.fitsimage.set_image(image)
        self.rendered.set()
