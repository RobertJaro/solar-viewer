"""Abstract base classes and default types"""
import copy
from abc import ABC, abstractmethod
from enum import Enum
from threading import Event
from typing import List, Dict

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget

from solarviewer.config import content_ctrl_name
from solarviewer.config.ioc import RequiredFeature
from solarviewer.ui.dialog import Ui_Dialog
from solarviewer.util import classproperty

V_ID = 0


def generateVId():
    """Viewer ID generation function."""
    global V_ID
    V_ID += 1
    return V_ID


class DataType(Enum):
    """Default data types."""
    MAP = "SunPy Map"
    MAP_COMPOSITE = "SunPy Composite Map"
    SERIES = "SunPy Series"
    PLAIN_2D = "2D FITS"
    SPECTROGRAM = "SunPy Spectrogram"
    NDCUBE = "NDCube"
    ANY = "Any"
    NONE = ""


class ViewerType(Enum):
    """Default viewer types."""
    MPL = "Matplotlib"
    GINGA = "Ginga"
    NDCUBE = "NDCUBE"
    ANY = "Any"


class FileType(Enum):
    """Predefined file types."""
    FITS = {"FITS": ["fits", "fit", "fts"]}


class ItemConfig:
    """Configuration class for menu items."""

    def __init__(self):
        self.menu_path = ""
        self.title = ""
        self.supported_data_types = []
        self.supported_viewer_types = []
        self.shortcut = None
        self.orientation = QtCore.Qt.LeftDockWidgetArea

    def setMenuPath(self, path: str) -> "ItemConfig":
        """
        Set the menu path.

        :param path: The path for the action in the menu. Separated by '/'.
        :type path: str
        :return: self
        :rtype: ItemConfig
        """
        self.menu_path = path
        return self

    def setTitle(self, title: str) -> "ItemConfig":
        """
        Set the text in the window title.

        :param title: The title text.
        :type title: str
        :return: self
        :rtype: ItemConfig
        """
        self.title = title
        return self

    def setOrientation(self, orientation: QtCore.Qt.DockWidgetArea) -> "ItemConfig":
        """
        Set the alignment in the main window.

        :param orientation: The Qt dock position
        :type orientation: DockWidgetArea
        :return: self
        :rtype: ItemConfig
        """
        self.orientation = orientation
        return self

    def setSupportedData(self, data_types: List[DataType]) -> "ItemConfig":
        """
        Set the list of supported data types.

        :param data_types: List of data types.
        :type data_types: List[DataType]
        :return: self
        :rtype: ItemConfig
        """
        self.supported_data_types = data_types
        return self

    def addSupportedData(self, data_type: DataType) -> "ItemConfig":
        """
        Add data type to the supported data types.

        :param data_type: The data type to add.
        :type data_type: DataType
        :return: self
        :rtype: ItemConfig
        """
        self.supported_data_types.append(data_type)
        return self

    def setSupportedViewer(self, viewer_types: List[ViewerType]) -> "ItemConfig":
        """
        Set the list of supported viewer types.

        :param viewer_types: List of viewer types.
        :type viewer_types: List[ViewerType]
        :return: self
        :rtype: ItemConfig
        """
        self.supported_data_types = viewer_types
        return self

    def addSupportedViewer(self, viewer_type: ViewerType) -> "ItemConfig":
        """
        Add viewer type to the supported viewer types.

        :param viewer_type: The viewer type to add.
        :type viewer_type: ViewerType
        :return: self
        :rtype: ItemConfig
        """
        self.supported_viewer_types.append(viewer_type)
        return self

    def setShortcut(self, key_sequence: QtGui.QKeySequence) -> "ItemConfig":
        """
        Set a shortcut to execute the associated action within the main window.

        :param key_sequence: The Qt key sequence.
        :type key_sequence: QKeySequence
        :return: self
        :rtype: ItemConfig
        """
        self.shortcut = key_sequence
        return self


class ToolbarConfig:
    """Configuration class for toolbars."""

    def __init__(self):
        self.menu_path = ""
        self.supported_data_types = []
        self.supported_viewer_types = []
        self.orientation = QtCore.Qt.RightToolBarArea

    def setMenuPath(self, path: str) -> "ToolbarConfig":
        """
        Set the menu path.

        :param path: The path for the action in the menu. Separated by '/'.
        :type path: str
        :return: self
        :rtype: ToolbarConfig
        """
        self.menu_path = path
        return self

    def setSupportedData(self, data_types: List[DataType]) -> "ToolbarConfig":
        """
        Set the list of supported data types.

        :param data_types: List of data types.
        :type data_types: List[DataType]
        :return: self
        :rtype: ToolbarConfig
        """
        self.supported_data_types = data_types
        return self

    def addSupportedData(self, data_type: DataType) -> "ToolbarConfig":
        """
        Add data type to the supported data types.

        :param data_type: The data type to add.
        :type data_type: DataType
        :return: self
        :rtype: ToolbarConfig
        """
        self.supported_data_types.append(data_type)
        return self

    def setSupportedViewer(self, viewer_types: List[ViewerType]) -> "ToolbarConfig":
        """
        Set the list of supported viewer types.

        :param viewer_types: List of viewer types.
        :type viewer_types: List[ViewerType]
        :return: self
        :rtype: ToolbarConfig
        """
        self.supported_data_types = viewer_types
        return self

    def addSupportedViewer(self, viewer_type: ViewerType) -> "ToolbarConfig":
        """
        Add viewer type to the supported viewer types.

        :param viewer_type: The viewer type to add.
        :type viewer_type: ViewerType
        :return: self
        :rtype: ToolbarConfig
        """
        self.supported_viewer_types.append(viewer_type)
        return self

    def setOrientation(self, orientation: QtCore.Qt.ToolBarArea) -> "ToolbarConfig":
        """
        Set the alignment in the main window.

        :param orientation: The Qt dock position
        :type orientation: ToolBarArea
        :return: self
        :rtype: ItemConfig
        """
        self.orientation = orientation
        return self


class ViewerConfig:
    """Configuration class for viewers."""

    def __init__(self):
        self.menu_path = ""
        self.multi_file = False
        self.file_types = FileType.FITS.value
        self.required_pkg = []

    def setMenuPath(self, path: str) -> "ViewerConfig":
        """
        Set the menu path.

        :param path: The path for the action in the menu. Separated by '/'.
        :type path: str
        :return: self
        :rtype: ViewerConfig
        """
        self.menu_path = path
        return self

    def setMultiFile(self, value: str) -> "ViewerConfig":
        """
        Set the open method of the viewer.

        :param value: True for selection of multiple files to create a single viewer. False if the viewer is associated with a single file.
        :type value: bool
        :return: self
        :rtype: ViewerConfig
        """
        self.multi_file = value
        return self

    def setFileType(self, value: Dict[str, List[str]]) -> "ViewerConfig":
        """
        Set the supported file types. Use FileType for predefined types.

        :param value: Dictionary of the supported files. Use {'TYPE NAME' : ['ext1', 'ext2']}
        :type value: Dict[str, List[str]]
        :return: self
        :rtype: ViewerConfig
        """
        self.file_types = value
        return self

    def addRequiredPackage(self, package: str) -> "ViewerConfig":
        """
        Add required python packages for this viewer. The user will be asked to install these packages when the viewer opens.

        :param package: The name of the python module.
        :type package: str
        :return: self
        :rtype: ViewerConfig
        """
        self.required_pkg.append(package)
        return self


class DataModel(ABC):
    """Base class for viewer controller models."""
    path = None


class Viewer(QtWidgets.QWidget):
    """Base class for the displayed widget."""
    rendered = Event()

    @abstractmethod
    def updateModel(self, model: DataModel) -> None:
        """
        Triggered function on data refresh.

        :param model: the data to visualize
        :type model: DataModel
        """
        raise NotImplementedError


class Controller(ABC):
    """Base class for registering controllers."""

    @classproperty
    def name(cls) -> str:
        """Unique identifier for registering the controller."""
        return cls.__name__


class ViewerController(ABC):
    """Base class for viewer controllers."""
    _v_id: int = None

    def __init__(self):
        self._v_id = generateVId()

    @classmethod
    @abstractmethod
    def fromFile(cls, file: str) -> 'ViewerController':
        """
        Create new ViewerController from file.

        :param file: file path to the data
        :type file: str
        :return: the initialized ViewerController
        :rtype: ViewerController
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def fromModel(cls, model: DataModel) -> 'ViewerController':
        """
        Create new ViewerController from existing model.

        :param model: data model
        :type model: DataModel
        :return: the initialized ViewerController
        :rtype: ViewerController
        """
        raise NotImplementedError

    @classproperty
    @abstractmethod
    def viewer_config(self) -> ViewerConfig:
        """
        Create the Configuration.
        Responsible for the representation in the application.

        :return: the viewer configuration
        :rtype: ViewerConfig
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def model(self) -> DataModel:
        """
        Returns the central data model of the viewer controller.

        :return: The data model of the viewer controller.
        :rtype: DataModel
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def view(self) -> Viewer:
        """
        Returns the GUI component of the viewer controller.

        :return: The GUI viewer of the controller.
        :rtype: Viewer
        """

        raise NotImplementedError

    @abstractmethod
    def updateModel(self, model):
        """
        Triggered action on data change. Refresh internal data model.
        Use ContentController to trigger this action.

        :param model: The new data model.
        :type model: DataModel
        """
        raise NotImplementedError

    @abstractmethod
    def getTitle(self) -> str:
        """
        Generate title depending on the data model.

        :return: The title of the viewer.
        """
        raise NotImplementedError

    @property
    def v_id(self) -> int:
        """Unique identifier of the viewer controller"""
        return self._v_id

    @property
    @abstractmethod
    def data_type(self) -> str:
        """The data type of the viewer controller"""
        raise NotImplementedError

    @property
    @abstractmethod
    def viewer_type(self) -> str:
        """The viewer type of the viewer controller"""
        raise NotImplementedError

    def close(self):
        """Closes the view of the controller."""
        self.view.deleteLater()


class ActionController(Controller):
    """Base class for action items."""

    @property
    @abstractmethod
    def item_config(self) -> ItemConfig:
        """
        Create the Configuration.
        Responsible for the representation in the application.

        :return: the menu item configuration
        :rtype: ItemConfig
        """
        raise NotImplementedError

    @abstractmethod
    def onAction(self):
        """Triggered action on selection of the menu item."""
        raise NotImplementedError


class DialogController(Controller):
    """Base class for dialog items."""
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
        """
        Create the Configuration.
        Responsible for the representation in the application.

        :return: the menu item configuration
        :rtype: ItemConfig
        """
        raise NotImplementedError

    @abstractmethod
    def setupContent(self, content_widget):
        """
        Internal basic UI setup function. Use the UI setup file here.

        :param content_widget: The Qt parent widget.
        :type: QWidget
        """
        raise NotImplementedError

    @abstractmethod
    def onDataChanged(self, viewer_ctrl: ViewerController):
        """
        Triggered when a new viewer is selected. Only supported data/viewer types need to be handled.

        :param viewer_ctrl: The new viewer controller.
        :type viewer_ctrl: ViewerController
        """
        raise NotImplementedError

    @abstractmethod
    def modifyData(self, data_model: DataModel) -> DataModel:
        """
        Triggered action on dialog accept. Execute action on data model.

        :param data_model: The data model to modify.
        :type data_model: DataModel
        :return: The modified data model.
        :rtype: DataModel
        """
        raise NotImplementedError

    @property
    def view(self) -> QtWidgets.QDialog:
        """
        Returns the dialog view.

        :return: The dialog widget.
        :rtype: QDialog
        """
        viewer_ctrl = self.content_ctrl.getViewerController()
        self.onDataChanged(viewer_ctrl)
        return self._dlg_view

    def _onOk(self):
        """Triggered ok action"""
        viewer_ctrl = self.content_ctrl.getViewerController()
        model = self.modifyData(copy.deepcopy(viewer_ctrl.model))
        self.content_ctrl.setDataModel(model)

    def _onCancel(self):
        """Triggered cancel action"""
        pass


class ToolController(Controller):
    """Base class for tool items."""

    @property
    @abstractmethod
    def item_config(self) -> ItemConfig:
        """
        Create the Configuration.
        Responsible for the representation in the application.

        :return: the menu item configuration
        :rtype: ItemConfig
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def view(self) -> QWidget:
        """
        Create the UI component of the tool controller.

        :return: The central widget of the tool.
        :rtype: QWidget
        """
        raise NotImplementedError
