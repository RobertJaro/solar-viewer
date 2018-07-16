import sys
import unittest

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication
from mock import Mock, mock

from solarviewer.app.connect import ViewerConnectionController
from solarviewer.app.content import ContentController
from solarviewer.config.base import ItemConfig, DataType, ViewerType
from solarviewer.config.impl import DataToolController, DataActionController, ToolbarController, ViewerToolController
from solarviewer.config.ioc import features


class ContentCtrlMock:
    def subscribeViewerChanged(self, func):
        return 1

    def subscribeDataChanged(self, v_id, func):
        return 22

    unsubscribe = Mock()
    getViewerController = Mock()
    getDataModel = Mock()


class ConnectionCtrlMock:
    def subscribe(self, func):
        return 30

    unsubscribe = Mock()


class ViewerMock:
    v_id = 123
    data_type = DataType.MAP
    viewer_type = ViewerType.MPL


class TestDataToolController(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)
        self.content_ctrl_mock = ContentCtrlMock()
        features.allowReplace = True
        features.Provide(ContentController.name, self.content_ctrl_mock)

        class TestDataTool(DataToolController):
            setupContent = Mock()
            onDataChanged = Mock()
            modifyData = Mock()

            @property
            def item_config(self) -> ItemConfig:
                return ItemConfig().addSupportedViewer(ViewerType.MPL).addSupportedData(DataType.MAP)

        self.tool = TestDataTool()

    def test_apply(self):
        self.tool.setupContent.assert_called_once()
        self.tool.view
        viewer_ctrl = ViewerMock()
        self.tool._onTabChanged(viewer_ctrl)
        self.tool.onDataChanged.assert_called_once()

        apply_button = self.tool._tool_ui.button_box.button(QtWidgets.QDialogButtonBox.Apply)
        QTest.mouseClick(apply_button, QtCore.Qt.LeftButton)
        self.tool.modifyData.assert_called_once()

    def test_close(self):
        self.tool.view

        self.tool._tool_view.closeEvent()
        self.content_ctrl_mock.unsubscribe.assert_has_calls([mock.call(1), mock.call(22)])

    def test_tab_changed(self):
        view = self.tool.view

        # Supported
        viewer_ctrl = ViewerMock()
        self.tool._onTabChanged(viewer_ctrl)
        self.assertTrue(view.isEnabled())

        # Unsupported Data Type
        viewer_ctrl = ViewerMock()
        viewer_ctrl.data_type = DataType.PLAIN_2D
        self.tool._onTabChanged(viewer_ctrl)
        self.assertFalse(view.isEnabled())

        # Unsupported Viewer Type
        viewer_ctrl = ViewerMock()
        viewer_ctrl.viewer_type = ViewerType.GINGA
        self.tool._onTabChanged(viewer_ctrl)
        self.assertFalse(view.isEnabled())

        # None
        self.tool._onTabChanged(None)
        self.assertFalse(view.isEnabled())


class TestDataActionController(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.content_ctrl_mock = ContentCtrlMock()
        features.allowReplace = True
        features.Provide(ContentController.name, self.content_ctrl_mock)

        class TestDataAction(DataActionController):
            modifyData = Mock()

            @property
            def item_config(self) -> ItemConfig:
                return ItemConfig()

        self.action = TestDataAction()

    def test_action(self):
        self.action.onAction()
        self.action.modifyData.assert_called_once()


class TestToolbarController(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.content_ctrl_mock = ContentCtrlMock()
        features.allowReplace = True
        features.Provide(ContentController.name, self.content_ctrl_mock)

        class TestToolbar(ToolbarController):
            setup = Mock()
            onClose = Mock()

            @property
            def item_config(self) -> ItemConfig:
                return ItemConfig()

        self.toolbar = TestToolbar()

    def test_change(self):
        view = self.toolbar.view
        self.toolbar.setup.assert_called_once()

        self.toolbar._onTabChanged(ViewerMock())
        self.assertTrue(view.isEnabled())

        self.toolbar._onTabChanged(None)
        self.assertFalse(view.isEnabled())

    def test_close(self):
        self.toolbar._onClose()
        self.toolbar.onClose.assert_called_once()


class TestViewerToolController(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.content_ctrl_mock = ContentCtrlMock()
        self.connection_ctrl_mock = ConnectionCtrlMock()
        features.allowReplace = True
        features.Provide(ContentController.name, self.content_ctrl_mock)
        features.Provide(ViewerConnectionController.name, self.connection_ctrl_mock)

        class TestViewerTool(ViewerToolController):
            connect = Mock()
            disconnect = Mock()
            setupContent = Mock()

            @property
            def item_config(self) -> ItemConfig:
                return ItemConfig()

        self.tool = TestViewerTool()

    def test_connect_close(self):
        view = self.tool.view
        self.tool.setupContent.assert_called_once()

        view.closeEvent()
        self.connection_ctrl_mock.unsubscribe.assert_called_once_with(30)
