from typing import List

from PyQt5.QtWidgets import QShortcut
from qtpy import QtWidgets, QtGui, QtCore

from solarviewer.app.content import ContentController
from solarviewer.app.statusbar import StatusBarController
from solarviewer.app.util import InitUtil, supported
from solarviewer.config import content_ctrl_name, viewers_name
from solarviewer.config.base import ToolController, DialogController, ActionController, ViewerController
from solarviewer.config.impl import ToolbarController
from solarviewer.config.ioc import RequiredFeature, MatchingFeatures, IsInstanceOf
from solarviewer.ui.app import Ui_MainWindow


class AppController(QtWidgets.QMainWindow):
    content_ctrl: ContentController = RequiredFeature(content_ctrl_name)
    status_bar_ctrl: StatusBarController = RequiredFeature(StatusBarController.name)
    viewers = RequiredFeature(viewers_name)
    tool_ctrls: List[ToolController] = MatchingFeatures(IsInstanceOf(ToolController))
    dlg_ctrls: List[DialogController] = MatchingFeatures(IsInstanceOf(DialogController))
    action_ctrls: List[ActionController] = MatchingFeatures(IsInstanceOf(ActionController))
    toolbar_ctrls: List[ToolbarController] = MatchingFeatures(IsInstanceOf(ToolbarController))

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.active_tools = {}
        self.active_toolbars = {}

        self.ui.horizontalLayout.addWidget(self.content_ctrl.view)

        self._initIcon()
        self._initViewers()
        self._initTools()
        self._initDialogs()
        self._initActions()
        self._initToolbars()
        self.setStatusBar(self.status_bar_ctrl.view)

        self.ui.default_toolbar.trigger()
        self.ui.actionQuit.triggered.connect(lambda evt: self.close())

    def openController(self, controller_name: str):
        """
        Opens the controller of the given name in the application
        :param controller_name: the class name of the controller to open (tool, dialog, action or toolbar)
        :return:
        """
        if controller_name in self.active_toolbars or controller_name in self.active_tools:
            return
        for ctrl in self.tool_ctrls:
            if ctrl.name == controller_name:
                self._toggleTool(ctrl)
                return
        for ctrl in self.dlg_ctrls:
            if ctrl.name == controller_name:
                self._openDialog(ctrl)
                return
        for ctrl in self.action_ctrls:
            if ctrl.name == controller_name:
                ctrl.onAction()
                return
        for ctrl in self.toolbar_ctrls:
            if ctrl.name == controller_name:
                self._toggleToolbar(ctrl)
                return

    def _toggleTool(self, ctrl: ToolController, action=None):
        if ctrl.name not in self.active_tools:
            dock = QtWidgets.QDockWidget(ctrl.item_config.title)
            dock.setWidget(ctrl.view)
            if action:
                dock.closeEvent = lambda evt, a=action: a.setChecked(False)
            self.addDockWidget(ctrl.item_config.orientation, dock)
            self.active_tools[ctrl.name] = dock
        else:
            self.active_tools.pop(ctrl.name).close()

    def _toggleToolbar(self, ctrl: ToolbarController):
        if ctrl.name not in self.active_toolbars:
            tool_bar = ctrl.view
            self.addToolBar(QtCore.Qt.RightToolBarArea, tool_bar)
            self.active_toolbars[ctrl.name] = tool_bar
        else:
            self.active_toolbars.pop(ctrl.name).close()

    def _openDialog(self, dlg_ctrl: DialogController):
        dlg = dlg_ctrl.view
        dlg.exec_()

    def _initIcon(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

    def _initViewers(self):
        for v_ctrl in self.viewers:
            tree = v_ctrl.viewer_config.menu_path.split("\\")
            if len(tree) == 1:
                continue
            action = InitUtil.getAction(tree, self.ui.menubar)
            action.triggered.connect(lambda evt, c=v_ctrl: self.content_ctrl.openViewer(c))

    def _initTools(self):
        for ctrl in self.tool_ctrls:
            tree = ctrl.item_config.menu_path.split("\\")
            if len(tree) == 1:
                continue
            action = InitUtil.getAction(tree, self.ui.menubar, True)
            action.triggered.connect(lambda evt, c=ctrl, a=action: self._toggleTool(c, a))
            if ctrl.item_config.shortcut:
                QShortcut(ctrl.item_config.shortcut, self, lambda: action.trigger if action.isEnabled() else None)

    def _initDialogs(self):
        for ctrl in self.dlg_ctrls:
            tree = ctrl.item_config.menu_path.split("\\")
            if len(tree) == 1:
                continue
            action = InitUtil.getAction(tree, self.ui.menubar)
            action.triggered.connect(lambda evt, c=ctrl: self._openDialog(c))
            self._subscribeItemSupportCheck(action, ctrl)
            if ctrl.item_config.shortcut:
                QShortcut(ctrl.item_config.shortcut, self, lambda: action.trigger if action.isEnabled() else None)

    def _initActions(self):
        for ctrl in self.action_ctrls:
            tree = ctrl.item_config.menu_path.split("\\")
            if len(tree) == 1:
                continue
            action = InitUtil.getAction(tree, self.ui.menubar)
            action.triggered.connect(ctrl.onAction)
            self._subscribeItemSupportCheck(action, ctrl)
            if ctrl.item_config.shortcut:
                QShortcut(ctrl.item_config.shortcut, self, lambda: action.trigger if action.isEnabled() else None)

    def _initToolbars(self):
        for ctrl in self.toolbar_ctrls:
            tree = ctrl.item_config.menu_path.split("\\")
            if len(tree) == 1:
                continue
            action = InitUtil.getAction(tree, self.ui.menubar, checkable=True)
            action.triggered.connect(lambda checked, c=ctrl: self._toggleToolbar(c))

    def _subscribeItemSupportCheck(self, action, ctrl):
        def f(vc: ViewerController, a=action, c=ctrl):
            dt = vc.data_type if vc else None
            vt = vc.viewer_type if vc else None
            enabled = supported(dt, vt, c.item_config.supported_data_types, c.item_config.supported_viewer_types)
            a.setEnabled(enabled)

        self.content_ctrl.subscribeTabChange(f)
        f(None)  # initial
