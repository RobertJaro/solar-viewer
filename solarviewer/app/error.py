import datetime
import sys

from PyQt5.QtWidgets import QWidget
from qtpy import QtWidgets, QtCore

from solarviewer.app.app import AppController
from solarviewer.config.base import ToolController, ItemConfig
from solarviewer.config.ioc import RequiredFeature
from solarviewer.ui.error_log import Ui_ErrorLog


class ErrorLogTool(ToolController):
    app_ctrl: AppController = RequiredFeature(AppController.__name__)

    def __init__(self):
        ToolController.__init__(self)

        self._view = QtWidgets.QWidget()
        self._ui = Ui_ErrorLog()
        self._ui.setupUi(self._view)

        self._base_excepthook = sys.excepthook
        sys.excepthook = self._exception_hook

    def _exception_hook(self, exctype, value, traceback):
        # Print the error and traceback to console
        self._base_excepthook(exctype, value, traceback)

        # write to ui
        self._ui.log.append("{}: {}".format(datetime.datetime.now(), value))

        # open tool
        self.app_ctrl.openController(self.name)

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setMenuPath("Help/Error Log").setTitle("Error Log").setOrientation(
            QtCore.Qt.BottomDockWidgetArea)

    @property
    def view(self) -> QWidget:
        return self._view
