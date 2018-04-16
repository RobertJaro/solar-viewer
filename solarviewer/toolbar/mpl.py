from qtpy import QtWidgets, QtCore, QtGui

from solarviewer.config.base import ItemConfig, ToolbarConfig, ViewerController, ViewerType, DataType
from solarviewer.config.impl import ToolbarController


class MplToolbarController(ToolbarController):

    def __init__(self):
        self.toolbar = None
        ToolbarController.__init__(self)

    @property
    def item_config(self) -> ItemConfig:
        return ToolbarConfig().setMenuPath("View\\Toolbar\\Default").addSupportedViewer(
            ViewerType.MPL).addSupportedData(DataType.ANY)

    def setup(self, toolbar_widget: QtWidgets.QToolBar):
        toolbar_widget.setOrientation(QtCore.Qt.Vertical)

        pan_icon = QtGui.QIcon()
        pan_icon.addPixmap(QtGui.QPixmap(":/image/pan.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        pan = toolbar_widget.addAction(pan_icon, "Pan")
        pan.setCheckable(True)

        zoom_icon = QtGui.QIcon()
        zoom_icon.addPixmap(QtGui.QPixmap(":/image/zoom.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        zoom = toolbar_widget.addAction(zoom_icon, "Zoom")
        zoom.setCheckable(True)

        reset_icon = QtGui.QIcon()
        reset_icon.addPixmap(QtGui.QPixmap(":/image/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        reset = toolbar_widget.addAction(reset_icon, "Reset")

        def f(checked, a):
            if checked:
                a.setChecked(False)

        pan.triggered.connect(lambda checked, a=zoom: f(checked, a))
        zoom.triggered.connect(lambda checked, a=pan: f(checked, a))
        pan.triggered.connect(self._onPan)
        zoom.triggered.connect(self._onZoom)
        reset.triggered.connect(self._onReset)

        self.pan_action = pan
        self.zoom_action = zoom

    def manageViewerController(self, viewer_ctrl: ViewerController):
        self.clearViewerController()
        self.toolbar = viewer_ctrl.view.toolbar
        if self.pan_action.isChecked():
            self.toolbar.pan()
        if self.zoom_action.isChecked():
            self.toolbar.zoom()

    def clearViewerController(self):
        if not self.toolbar:
            return
        if self.pan_action.isChecked():
            self.toolbar.pan()
        if self.zoom_action.isChecked():
            self.toolbar.zoom()
        self.toolbar = None

    def _onPan(self):
        self.toolbar.pan()

    def _onZoom(self):
        self.toolbar.zoom()

    def _onReset(self):
        self.toolbar.home()
