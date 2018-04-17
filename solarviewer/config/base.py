"""Abstract base classes and default types"""
import copy
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict

from qtpy import QtWidgets

from solarviewer.config import content_ctrl_name
from solarviewer.config.ioc import RequiredFeature
from solarviewer.ui.dialog import Ui_Dialog
from solarviewer.util import classproperty

V_ID = 0


def generateVId():
    """Viewer ID generation function"""
    global V_ID
    V_ID += 1
    return V_ID


class DataType(Enum):
    """Default data types"""
    MAP = "SunPy Map"
    MAP_CUBE = "SunPy Composite Map"
    SERIES = "SunPy Series"
    PLAIN_2D = "2D FITS"
    ANY = "Any"
    NONE = ""


class ViewerType(Enum):
    """Default viewer types"""
    MPL = "Matplotlib"
    GINGA = "Ginga"
    ANY = "Any"
    NONE = ""


class FileType(Enum):
    """Predefined file types"""
    FITS = {"FITS": ["fits", "fit", "fts"]}


class ItemConfig:
    """Configuration class for menu items"""

    def __init__(self):
        self.menu_path = ""
        self.title = ""
        self.supported_data_types = []
        self.supported_viewer_types = []

    def setMenuPath(self, path: str):
        self.menu_path = path
        return self

    def setTitle(self, title: str):
        self.title = title
        return self

    def setSupportedData(self, data_types: List[DataType]):
        self.supported_data_types = data_types
        return self

    def addSupportedData(self, data_type: DataType):
        self.supported_data_types.append(data_type)
        return self

    def setSupportedViewer(self, viewer_types: List[ViewerType]):
        self.supported_data_types = viewer_types
        return self

    def addSupportedViewer(self, viewer_type: ViewerType):
        self.supported_viewer_types.append(viewer_type)
        return self


class ToolbarConfig:
    """Configuration class for menu items"""

    def __init__(self):
        self.menu_path = ""
        self.supported_data_types = []
        self.supported_viewer_types = []

    def setMenuPath(self, path: str):
        self.menu_path = path
        return self

    def setSupportedData(self, data_types: List[DataType]):
        self.supported_data_types = data_types
        return self

    def addSupportedData(self, data_type: DataType):
        self.supported_data_types.append(data_type)
        return self

    def setSupportedViewer(self, viewer_types: List[ViewerType]):
        self.supported_data_types = viewer_types
        return self

    def addSupportedViewer(self, viewer_type: ViewerType):
        self.supported_viewer_types.append(viewer_type)
        return self


class ViewerConfig:
    """Configuration class for viewers"""

    def __init__(self):
        self.menu_path = ""
        self.multi_file = False
        self.file_types = FileType.FITS.value

    def setMenuPath(self, path: str):
        self.menu_path = path
        return self

    def setMultiFile(self, value: str):
        self.multi_file = value
        return self

    def setFileType(self, value: Dict[str, List[str]]):
        self.file_types = value
        return self


class DataModel(ABC):
    """Base class for viewer controller models"""
    path = None


class Controller(ABC):
    """Base class for registering controllers"""

    @classproperty
    def name(cls) -> str:
        """Unique identifier for registering the controller"""
        return cls.__name__


class ViewerController(ABC):
    """Base class for viewer controllers"""
    _data_type = DataType.NONE
    _viewer_type = ViewerType.NONE
    _v_id = None

    def __init__(self):
        self._v_id = generateVId()

    @classmethod
    @abstractmethod
    def fromFile(cls, file) -> 'ViewerController':
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def fromModel(cls, model: DataModel) -> 'ViewerController':
        raise NotImplementedError

    @classproperty
    @abstractmethod
    def viewer_config(self) -> ViewerConfig:
        raise NotImplementedError

    @property
    @abstractmethod
    def model(self) -> DataModel:
        raise NotImplementedError

    @property
    @abstractmethod
    def view(self) -> QtWidgets.QWidget:
        raise NotImplementedError

    @abstractmethod
    def updateModel(self, model):
        raise NotImplementedError

    @abstractmethod
    def getTitle(self) -> str:
        raise NotImplementedError

    @property
    def v_id(self) -> int:
        return self._v_id

    @property
    def data_type(self) -> str:
        return self._data_type

    @property
    def viewer_type(self) -> str:
        return self._viewer_type

    def close(self):
        self.view.deleteLater()


class ActionController(Controller):
    """Base class for action items"""

    @property
    @abstractmethod
    def item_config(self) -> ItemConfig:
        raise NotImplementedError

    @abstractmethod
    def onAction(self):
        raise NotImplementedError


class DialogController(Controller):
    """Base class for dialog items"""
    content_ctrl = RequiredFeature(content_ctrl_name)

    def __init__(self):
        self._dlg_view = QtWidgets.QDialog()
        self._dlg_view.setWindowTitle(self.item_config.title)
        self._dlg_ui = Ui_Dialog()
        self._dlg_ui.setupUi(self._dlg_view)

        self.setupContent(self._dlg_ui.content)
        self._dlg_ui.button_box.accepted.connect(self._onOk)
        self._dlg_ui.button_box.rejected.connect(self._onCancel)

    @property
    @abstractmethod
    def item_config(self) -> ItemConfig:
        raise NotImplementedError

    @abstractmethod
    def setupContent(self, content_widget):
        raise NotImplementedError

    @abstractmethod
    def onDataChanged(self, viewer_ctrl: ViewerController):
        raise NotImplementedError

    @abstractmethod
    def modifyData(self, data_model: DataModel) -> DataModel:
        raise NotImplementedError

    @property
    def view(self) -> QtWidgets.QDialog:
        viewer_ctrl = self.content_ctrl.getViewerController()
        self.onDataChanged(viewer_ctrl)
        return self._dlg_view

    def _onOk(self):
        viewer_ctrl = self.content_ctrl.getViewerController()
        model = self.modifyData(copy.deepcopy(viewer_ctrl.model))
        self.content_ctrl.setDataModel(model)

    def _onCancel(self):
        pass


class ToolController(Controller):
    """Base class for tool items"""

    @property
    @abstractmethod
    def item_config(self) -> ItemConfig:
        raise NotImplementedError

    @property
    @abstractmethod
    def view(self) -> QtWidgets:
        raise NotImplementedError
