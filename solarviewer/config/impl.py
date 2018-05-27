import copy
from abc import abstractmethod

from PyQt5.QtWidgets import QWidget, QDialogButtonBox
from qtpy import QtWidgets

from solarviewer.app.connect import ViewerConnectionController, ConnectionMixin
from solarviewer.app.content import ContentController
from solarviewer.app.util import supported
from solarviewer.config import content_ctrl_name
from solarviewer.config.base import ViewerController, DataModel, ActionController, ToolController, Controller, \
    ToolbarConfig
from solarviewer.config.ioc import RequiredFeature
from solarviewer.ui.data_tool import Ui_DataTool
from solarviewer.ui.viewer_tool import Ui_ViewerTool
from solarviewer.util import executeTask, executeLongRunningTask


class DataToolController(ToolController):
    """Base class for tool items with relation to the currently viewed data"""
    content_ctrl: ContentController = RequiredFeature(content_ctrl_name)

    def __init__(self):
        ToolController.__init__(self)

        self._tool_view = QWidget()
        self._tool_ui = Ui_DataTool()
        self._tool_ui.setupUi(self._tool_view)

        self._sub_id = None
        self._tab_sub_id = None
        self._v_id = None

        self.setupContent(self._tool_ui.content)
        self._tool_ui.content.resizeEvent = lambda evt: self._tool_ui.scrollArea.setMinimumWidth(
            self._tool_ui.content.sizeHint().width() + self._tool_ui.scrollArea.verticalScrollBar().sizeHint().width())

        apply_btn = self._tool_ui.button_box.button(QDialogButtonBox.Apply)
        apply_btn.clicked.connect(self._onApply)

    @abstractmethod
    def setupContent(self, content_widget: QWidget):
        raise NotImplementedError

    @abstractmethod
    def onDataChanged(self, viewer_ctrl):
        """Triggered action for data changes (switched tab, modified data)"""
        raise NotImplementedError

    @abstractmethod
    def modifyData(self, data_model: DataModel) -> DataModel:
        """
        Triggered apply action.
        :param data_model: The selected data model
        :return: The modified data model
        """
        raise NotImplementedError

    @property
    def view(self) -> QtWidgets:
        viewer_ctrl = self.content_ctrl.getViewerController()
        self._onTabChanged(viewer_ctrl)

        self._tab_sub_id = self.content_ctrl.subscribeViewerChanged(self._onTabChanged)
        self._tool_view.closeEvent = self._onClose
        return self._tool_view

    def _onApply(self):
        if not self._v_id:
            return
        self._tool_ui.message_box.hide()
        self._tool_ui.button_box.setEnabled(False)
        data_model = self.content_ctrl.getDataModel(self._v_id)
        executeTask(self._apply, [data_model], self._onResult)

    def _apply(self, data_model):
        try:
            data_copy = copy.deepcopy(data_model)
            result = self.modifyData(data_copy)
            return result if result else data_copy
        except Exception as ex:
            return ex

    def _onResult(self, result):
        self._tool_ui.button_box.setEnabled(True)
        if isinstance(result, Exception):
            self._tool_ui.message_box.showMessage(str(result))
            return
        self.content_ctrl.setDataModel(result)

    def _onTabChanged(self, viewer_ctrl: ViewerController):
        if self._sub_id is not None:
            self.content_ctrl.unsubscribe(self._sub_id)

        if viewer_ctrl is None:
            self._sub_id = None
            self._v_id = None
        else:
            self._sub_id = self.content_ctrl.subscribeDataChanged(viewer_ctrl.v_id, self._handleDataChanged)
            self._v_id = viewer_ctrl.v_id

        self._handleDataChanged(viewer_ctrl)

    def _onClose(self, *args):
        self.content_ctrl.unsubscribe(self._tab_sub_id)
        if self._sub_id:
            self.content_ctrl.unsubscribe(self._sub_id)

    def _handleDataChanged(self, viewer_ctrl):
        if viewer_ctrl is None or not supported(viewer_ctrl.data_type, viewer_ctrl.viewer_type,
                                                self.item_config.supported_data_types,
                                                self.item_config.supported_viewer_types):
            self._tool_view.setEnabled(False)
        else:
            self._tool_view.setEnabled(True)
            self.onDataChanged(viewer_ctrl)


class DataActionController(ActionController):
    """Base class for actions related to the currently viewed data"""
    content_ctrl = RequiredFeature(ContentController.name)

    def onAction(self):
        data_model = self.content_ctrl.getDataModel()
        call_after = lambda result: self.content_ctrl.setDataModel(result)
        executeLongRunningTask(self._action, [data_model], "Action in Progress", call_after)

    def _action(self, data_model):
        data_copy = copy.deepcopy(data_model)
        modified = self.modifyData(data_copy)
        return modified

    @abstractmethod
    def modifyData(self, data_model: DataModel) -> DataModel:
        raise NotImplementedError


class ToolbarController(Controller):
    """Base class for toolbars"""
    content_ctrl: ContentController = RequiredFeature(content_ctrl_name)

    def __init__(self):
        self._sub_id = None
        self._tab_sub_id = None

    @property
    @abstractmethod
    def item_config(self) -> ToolbarConfig:
        raise NotImplementedError

    @abstractmethod
    def setup(self, toolbar_widget: QtWidgets.QToolBar):
        raise NotImplementedError

    @abstractmethod
    def onClose(self):
        pass

    def supports(self, viewer_ctrl: ViewerController) -> bool:
        return viewer_ctrl is not None and supported(viewer_ctrl.data_type, viewer_ctrl.viewer_type,
                                                     self.item_config.supported_data_types,
                                                     self.item_config.supported_viewer_types)

    @property
    def view(self) -> QtWidgets.QToolBar:
        self._toolbar_view = QtWidgets.QToolBar()
        self.setup(self._toolbar_view)

        viewer_ctrl = self.content_ctrl.getViewerController()
        self._onTabChanged(viewer_ctrl)

        self._tab_sub_id = self.content_ctrl.subscribeViewerChanged(self._onTabChanged)
        self._toolbar_view.closeEvent = self._onClose
        return self._toolbar_view

    def _onTabChanged(self, viewer_ctrl: ViewerController):
        if self._sub_id is not None:
            self.content_ctrl.unsubscribe(self._sub_id)

        if viewer_ctrl is None:
            self._sub_id = None
        else:
            self._sub_id = self.content_ctrl.subscribeDataChanged(viewer_ctrl.v_id, self._onDataChanged)

        self._onDataChanged(viewer_ctrl)

    def _onClose(self, *args):
        self.onClose()
        self.content_ctrl.unsubscribe(self._tab_sub_id)
        if self._sub_id:
            self.content_ctrl.unsubscribe(self._sub_id)

    def _onDataChanged(self, viewer_ctrl):
        if viewer_ctrl is None or not supported(viewer_ctrl.data_type, viewer_ctrl.viewer_type,
                                                self.item_config.supported_data_types,
                                                self.item_config.supported_viewer_types):
            self._toolbar_view.setEnabled(False)
        else:
            self._toolbar_view.setEnabled(True)


class ViewerToolController(ToolController, ConnectionMixin):
    """Base class for viewer aware tool controllers"""
    connection_ctrl: ViewerConnectionController = RequiredFeature(ViewerConnectionController.name)

    def __init__(self):
        ToolController.__init__(self)

        self._tool_view = QWidget()
        self._tool_ui = Ui_ViewerTool()
        self._tool_ui.setupUi(self._tool_view)

        self._sub_id = None

        self.setupContent(self._tool_ui.content)
        self._tool_ui.content.resizeEvent = lambda evt: self._tool_ui.scrollArea.setMinimumWidth(
            self._tool_ui.content.sizeHint().width() + self._tool_ui.scrollArea.verticalScrollBar().sizeHint().width())

    def supports(self, viewer_ctrl: ViewerController) -> bool:
        return viewer_ctrl is not None and supported(viewer_ctrl.data_type, viewer_ctrl.viewer_type,
                                                     self.item_config.supported_data_types,
                                                     self.item_config.supported_viewer_types)

    def enabled(self, value: bool):
        self._tool_view.setEnabled(value)

    @abstractmethod
    def setupContent(self, content_widget):
        raise NotImplementedError

    @property
    def view(self) -> QtWidgets.QWidget:
        self._sub_id = self.connection_ctrl.subscribe(self)

        self._tool_view.closeEvent = self._onClose
        return self._tool_view

    def _onClose(self, *args):
        self.connection_ctrl.unsubscribe(self._sub_id)
