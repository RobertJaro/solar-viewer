from PyQt5.QtWidgets import QAction
from qtpy import QtWidgets, QtCore, QtGui

from solarviewer.app.connect import ViewerLock, ViewerConnectionController
from solarviewer.config.base import ItemConfig, ToolbarConfig, ViewerController, ViewerType, DataType
from solarviewer.config.impl import ToolbarController
from solarviewer.config.ioc import RequiredFeature


class MplToolbarController(ToolbarController):
    connection_ctrl: ViewerConnectionController = RequiredFeature(ViewerConnectionController.name)

    def __init__(self):
        ToolbarController.__init__(self)

    @property
    def item_config(self) -> ItemConfig:
        return ToolbarConfig().setMenuPath("View/Toolbar/Default").addSupportedViewer(
            ViewerType.MPL).addSupportedData(DataType.ANY)

    def setup(self, toolbar_widget: QtWidgets.QToolBar):
        toolbar_widget.setOrientation(QtCore.Qt.Vertical)

        pan_icon = QtGui.QIcon(":/image/pan.png")
        pan = toolbar_widget.addAction(pan_icon, "Pan")
        pan.setCheckable(True)

        zoom_icon = QtGui.QIcon(":/image/zoom.png")
        zoom = toolbar_widget.addAction(zoom_icon, "Zoom")
        zoom.setCheckable(True)

        reset_icon = QtGui.QIcon(":/image/home.png")
        reset = toolbar_widget.addAction(reset_icon, "Reset")

        def f(checked, a):
            if checked:
                a.setChecked(False)

        pan.triggered.connect(self._onPan)
        zoom.triggered.connect(self._onZoom)
        reset.triggered.connect(self._onReset)

        self.pan_action = pan
        self.zoom_action = zoom

    def onClose(self):
        if self.pan_action.isChecked() or self.zoom_action.isChecked():
            self.connection_ctrl.remove_lock()

    def _onPan(self):
        if not self.pan_action.isChecked():
            self.connection_ctrl.remove_lock()
            return
        pan_lock = _PanLock(self.item_config, self.pan_action)
        self.connection_ctrl.add_lock(pan_lock)

    def _onZoom(self):
        if not self.zoom_action.isChecked():
            self.connection_ctrl.remove_lock()
            return
        zoom_lock = _ZoomLock(self.item_config, self.zoom_action)
        self.connection_ctrl.add_lock(zoom_lock)

    def _onReset(self):
        view = self.content_ctrl.getViewer()
        view.toolbar.home()


class _PanLock(ViewerLock):
    def __init__(self, config, pan: QAction):
        ViewerLock.__init__(self, config.supported_viewer_types, config.supported_data_types)
        self.pan = pan

    def release(self):
        self.pan.setChecked(False)

    def connect(self, viewer_ctrl: ViewerController):
        toolbar = viewer_ctrl.view.toolbar
        toolbar.pan()

    def disconnect(self, viewer_ctrl: ViewerController):
        toolbar = viewer_ctrl.view.toolbar
        toolbar.pan()


class _ZoomLock(ViewerLock):
    def __init__(self, config, zoom: QAction):
        ViewerLock.__init__(self, config.supported_viewer_types, config.supported_data_types)
        self.zoom = zoom

    def release(self):
        self.zoom.setChecked(False)

    def connect(self, viewer_ctrl: ViewerController):
        toolbar = viewer_ctrl.view.toolbar
        toolbar.zoom()

    def disconnect(self, viewer_ctrl: ViewerController):
        toolbar = viewer_ctrl.view.toolbar
        toolbar.zoom()
