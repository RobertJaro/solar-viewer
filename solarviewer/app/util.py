from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QShortcut

from solarviewer.app.content import ContentController
from solarviewer.config.base import FileType, ViewerController, Controller
from solarviewer.config.ioc import RequiredFeature


class ActionManager:
    content_ctrl: ContentController = RequiredFeature(ContentController.name)

    def __init__(self, action: QtWidgets.QAction):
        self.action = action
        action.triggered.connect(self._onTriggered)
        action.setEnabled(False)

        self.controllers = {}
        self._active_ctrl = None
        self._shortcut = False
        self.content_ctrl.subscribeViewerChanged(self._checkActionSupported)

    def register(self, ctrl: Controller, action, parent):
        self.controllers[ctrl] = action
        self._checkActionSupported(self.content_ctrl.getViewerController())
        self._registerShortcut(ctrl, parent)

    def _registerShortcut(self, ctrl, parent):
        if self._shortcut is not False:
            assert ctrl.item_config.shortcut is self._shortcut, \
                "invalid configuration. different shortcuts for same action encountered."
            return
        if not ctrl.item_config.shortcut:
            self._shortcut = None
        else:
            QShortcut(ctrl.item_config.shortcut, parent,
                      lambda: self.action.trigger() if self.action.isEnabled() else None)

    def _checkActionSupported(self, vc: ViewerController):
        dt = vc.data_type if vc else None
        vt = vc.viewer_type if vc else None

        enabled = False
        for c in self.controllers.keys():
            if supported(dt, vt, c.item_config.supported_data_types, c.item_config.supported_viewer_types):
                enabled = True
                self._active_ctrl = c
                break

        self.action.setEnabled(enabled)

    def _onTriggered(self, checked):
        self.controllers[self._active_ctrl]()


class InitUtil:

    @staticmethod
    def getAction(tree, parent, checkable=False) -> QtWidgets.QAction:
        for i, name in enumerate(tree):
            if i == len(tree) - 1:
                action = InitUtil._getAction(name, parent, checkable)
                return action
            else:
                parent = InitUtil._getSubMenu(name, parent)

    @staticmethod
    def createActionManager(tree, parent) -> ActionManager:
        action = InitUtil.getAction(tree, parent)
        return ActionManager(action)

    @staticmethod
    def _getSubMenu(name, parent):
        for c in parent.children():
            if isinstance(c, QtWidgets.QMenu) and c.title() == name:
                return c
        return parent.addMenu(name)

    @staticmethod
    def _getAction(name, parent, checkable):
        for a in parent.actions():
            if a.text() == name:
                return a
        a = QtWidgets.QAction(name, parent)
        a.setCheckable(checkable)
        parent.addAction(a)
        return a


def supported(data_type, viewer_type, supported_types, supported_viewers):
    from solarviewer.config.base import DataType, ViewerType
    if len(supported_viewers) == 0:
        return True
    if data_type is None or viewer_type is None:
        return False
    types = [str(t) for t in supported_types]
    viewers = [str(t) for t in supported_viewers]

    return (str(DataType.ANY) in types or str(data_type) in types) and (
            str(ViewerType.ANY) in viewers or str(viewer_type) in viewers)


def saveFits(s_map):
    f = getattr(s_map, "path", None)
    name, _ = QtWidgets.QFileDialog.getSaveFileName(directory=f, filter=getExtensionString(FileType.FITS.value))
    if name:
        s_map.save(name, overwrite=True)


def getExtensionString(file_types):
    files = []
    for f, t in file_types.items():
        types = " ".join(["*." + str(type) + "" for type in t])
        type = f + " (" + types + ")"
        files.append(type)
    return " ".join(files)
