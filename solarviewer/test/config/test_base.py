import sys
import unittest
from unittest.mock import Mock

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from qtpy import QtWidgets
from qtpy.QtTest import QTest

from solarviewer.app.content import ContentController
from solarviewer.config.base import ItemConfig, DataType, ViewerType, ToolbarConfig, ViewerConfig, DialogController
from solarviewer.config.ioc import features


class TestConfig(unittest.TestCase):

    def test_item_config(self):
        config = ItemConfig()
        config.setMenuPath("PATH")
        config.setTitle("TITLE")
        config.addSupportedData(DataType.ANY)
        config.addSupportedViewer(ViewerType.ANY)
        config.setShortcut("SHORTCUT")
        config.setOrientation(QtCore.Qt.RightDockWidgetArea)

        self.assertEquals(config.menu_path, "PATH")
        self.assertEquals(config.title, "TITLE")
        self.assertEquals(config.supported_data_types, [DataType.ANY])
        self.assertEquals(config.supported_viewer_types, [ViewerType.ANY])
        self.assertEquals(config.shortcut, "SHORTCUT")
        self.assertEquals(config.orientation, QtCore.Qt.RightDockWidgetArea)

    def test_toolbar_config(self):
        config = ToolbarConfig()
        config.setMenuPath("PATH")
        config.addSupportedData(DataType.ANY)
        config.addSupportedViewer(ViewerType.ANY)

        self.assertEquals(config.menu_path, "PATH")
        self.assertEquals(config.supported_data_types, [DataType.ANY])
        self.assertEquals(config.supported_viewer_types, [ViewerType.ANY])

    def test_toolbar_config(self):
        config = ViewerConfig()
        config.setMenuPath("PATH")
        config.setMultiFile(True)
        config.setFileType(["FILE", ["file"]])
        config.addRequiredPackage("PKG")

        self.assertEquals(config.menu_path, "PATH")
        self.assertEquals(config.multi_file, True)
        self.assertEquals(config.file_types, ["FILE", ["file"]])
        self.assertEquals(config.required_pkg, ["PKG"])


class TestDialogController(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)
        features.allowReplace = True
        features.Provide(ContentController.name, Mock())

        class TestDlg(DialogController):
            setupContent = Mock()
            onDataChanged = Mock()
            modifyData = Mock()

            @property
            def item_config(self) -> ItemConfig:
                return ItemConfig()

        self.dlg = TestDlg()

    def test_ok(self):
        self.dlg.setupContent.assert_called_once()

        self.dlg.view
        self.dlg.onDataChanged.assert_called_once()

        ok_button = self.dlg._dlg_ui.button_box.button(QtWidgets.QDialogButtonBox.Ok)
        QTest.mouseClick(ok_button, QtCore.Qt.LeftButton)
        self.dlg.modifyData.assert_called_once()
