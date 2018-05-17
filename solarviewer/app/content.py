from typing import Callable, List, Dict

from PyQt5.QtWidgets import QTabWidget
from qtpy import QtWidgets, QtCore

from solarviewer.config.base import ViewerController, Controller, DataModel, Viewer
from solarviewer.util import executeWaitTask


class ContentModel:
    def __init__(self):
        self._viewers = {}
        self._tabs = {}
        self._active_viewer = None

    def getActiveViewer(self) -> ViewerController:
        return self._active_viewer

    def setActiveViewer(self, viewer: ViewerController):
        self._active_viewer = viewer

    def addViewerCtrl(self, viewer: ViewerController):
        self._viewers[viewer.v_id] = viewer

    def setData(self, v_id: int, model: DataModel):
        self._viewers[v_id].setModel(model)

    def getViewerCtrl(self, v_id: int) -> ViewerController:
        return self._viewers.get(v_id, None)

    def getViewerCtrls(self) -> List[ViewerController]:
        return self._viewers

    def addTab(self, v_id: int, dock: QtWidgets.QDockWidget):
        self._tabs[v_id] = dock

    def getTabs(self) -> Dict[int, QtWidgets.QDockWidget]:
        return self._tabs

    def getActiveTab(self) -> QtWidgets.QDockWidget:
        if self._active_viewer is None:
            return None
        return self._tabs[self._active_viewer.v_id]

    def remove(self, v_id):
        ctrl = self._viewers.pop(v_id)
        tab = self._tabs.pop(v_id)
        return ctrl, tab

    def count(self):
        return len(self._viewers.keys())

    def isActive(self, v_id):
        if self._active_viewer is None:
            return False
        return self._active_viewer.v_id == v_id


class ContentController(Controller):
    """Main Controller for content storage and representation"""
    sub_id = 0

    def __init__(self):
        self._model: ContentModel = ContentModel()

        self._viewer_changed_subscribers = {}
        self._viewer_added_subscribers = {}
        self._viewer_closed_subscribers = {}
        self._data_changed_subscribers = {}

        self._view = QtWidgets.QMainWindow()
        self._view.setTabPosition(QtCore.Qt.AllDockWidgetAreas, QTabWidget.North)
        self._view.setCentralWidget(None)
        self._view.setDockOptions(QtWidgets.QMainWindow.AnimatedDocks |
                                  QtWidgets.QMainWindow.AllowNestedDocks |
                                  QtWidgets.QMainWindow.AllowTabbedDocks |
                                  QtWidgets.QMainWindow.GroupedDragging)
        self._view.tabifiedDockWidgetActivated.connect(lambda x: x.setFocus())
        self._view.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self._view.setStyleSheet("background-color: white;")

    @property
    def view(self) -> QTabWidget:
        return self._view

    def getViewerControllers(self, data_type: str = None) -> List[ViewerController]:
        """
        Returns all viewer controllers with the matching data_type. If none is specified all viewers are returned.
        :return: List[ViewerController]
        """
        if data_type:
            return [v for v in self._model.getViewerCtrls().values() if v.data_type == data_type]
        return self._model.getViewerCtrls().value()

    def getViewerController(self, v_id=-1) -> ViewerController:
        """
        Returns the viewer controller with id=v_id. When no id is provided the active viewer controller is returned.
        :param v_id: the unique identifier
        :return: ViewerController
        """
        if v_id == -1:
            v_id = self.getCurrentId()
        if v_id == -1:  # No tab open
            return None
        viewer_ctrl = self._model.getViewerCtrl(v_id)
        return viewer_ctrl

    def getViewer(self, v_id=-1) -> Viewer:
        """
        Returns the viewer with id=v_id. When no id is provided the active viewer is returned.
        :param v_id: the unique identifier
        :return: Viewer
        """
        viewer_ctrl = self.getViewerController(v_id)
        if viewer_ctrl is None:
            return None
        return viewer_ctrl.view

    def getDataModel(self, v_id=-1) -> DataModel:
        """
        Returns the data model with id=v_id. When no id is provided the active data model is returned.
        :param v_id: the unique identifier
        :return: DataModel
        """
        viewer_ctrl = self.getViewerController(v_id)
        if viewer_ctrl is None:
            return None
        return viewer_ctrl.model

    def setDataModel(self, data_model: DataModel, v_id=-1):
        """Set the data model of viewer with id=v_id. If id is -1 the currently viewed data will be changed."""
        if v_id == -1:
            v_id = self.getCurrentId()
        assert v_id is not -1, "Invalid set data command encountered."
        self._model.getViewerCtrl(v_id).updateModel(data_model)
        self._onDataChanged(v_id)

    def getCurrentId(self):
        viewer = self._model.getActiveViewer()
        return viewer.v_id if viewer is not None else -1

    def subscribeViewerChanged(self, action: Callable) -> int:
        """
        Subscribes action to tab changes
        :param action: Callable function of form action(viewer_controller: ViewerController)
        :return: unique subscription id
        """
        self.sub_id += 1
        self._viewer_changed_subscribers[self.sub_id] = action
        return self.sub_id

    def subscribeViewerAdded(self, action):
        """
        Subscribe action to viewer added
        :param action: Callable function of form action(viewer_controller: ViewerController)
        :return: unique subscription id
        """
        self.sub_id += 1
        self._viewer_added_subscribers[self.sub_id] = action
        return self.sub_id

    def subscribeViewerClosed(self, action):
        """
        Subscribe action to viewer added
        :param action: Callable function of form action(viewer_controller: ViewerController)
        :return: unique subscription id
        """
        self.sub_id += 1
        self._viewer_closed_subscribers[self.sub_id] = action
        return self.sub_id

    def subscribeDataChanged(self, v_id, action):
        """
        Subscribe action to data changes
        :param v_id: the id of the viewer controller
        :param action: Callable function of form action(viewer_controller: ViewerController)
        :return: unique subscription id
        """
        self.sub_id += 1
        v_dict = {}
        if self._data_changed_subscribers.get(v_id, None):
            v_dict = self._data_changed_subscribers[v_id]
        else:
            self._data_changed_subscribers[v_id] = v_dict

        v_dict[self.sub_id] = action
        return self.sub_id

    def addViewerController(self, viewer_ctrl):
        self._model.addViewerCtrl(viewer_ctrl)

        wrapper = QtWidgets.QDockWidget("{}: {}".format(viewer_ctrl.v_id, viewer_ctrl.getTitle()))
        wrapper.setWidget(viewer_ctrl.view)

        wrapper.setFocusPolicy(QtCore.Qt.ClickFocus)
        wrapper.focusInEvent = lambda x, v=viewer_ctrl.v_id, dock=wrapper: self._onViewerChanged(v, dock)
        wrapper.closeEvent = lambda evt, v=viewer_ctrl.v_id: self._onTabClosed(v)
        wrapper.setFeatures(
            QtWidgets.QDockWidget.DockWidgetVerticalTitleBar | QtWidgets.QDockWidget.DockWidgetClosable | QtWidgets.QDockWidget.DockWidgetFloatable | QtWidgets.QDockWidget.DockWidgetMovable)
        wrapper.setMinimumSize(300, 300)

        self._view.addDockWidget(self._getDefaultDockArea(), wrapper)
        self._tabify(wrapper)

        self._model.addTab(viewer_ctrl.v_id, wrapper)
        self._onViewerAdded(viewer_ctrl)
        wrapper.setFocus()  # triggers _onViewerChanged

    def _getDefaultDockArea(self):
        if self._model.getActiveTab():
            return self._view.dockWidgetArea(self._model.getActiveTab())
        return QtCore.Qt.TopDockWidgetArea

    def _tabify(self, dock):
        for d in self._model.getTabs().values():
            if self._view.dockWidgetArea(d) == self._view.dockWidgetArea(dock):
                self._view.tabifyDockWidget(d, dock)
        dock.show()
        dock.raise_()

    def _onViewerChanged(self, v_id, dock: QtWidgets.QDockWidget):
        if self._model.isActive(v_id):
            return
        if self._model.getActiveTab():
            old_dock = self._model.getActiveTab()
            title = old_dock.windowTitle()
            title = title.replace(" <<", "")
            old_dock.setWindowTitle(title)

        v = self._model.getViewerCtrl(v_id)
        self._model.setActiveViewer(v)
        dock.setWindowTitle("{} <<".format(dock.windowTitle()))
        self._notifySubscribers(v, self._viewer_changed_subscribers)

    def _onViewerAdded(self, viewer_controller):
        self._notifySubscribers(viewer_controller, self._viewer_added_subscribers)

    def _onViewerClosed(self, viewer_controller):
        for sub in self._viewer_closed_subscribers.values():
            sub(viewer_controller)
        self._data_changed_subscribers.pop(viewer_controller.v_id)

    def _onDataChanged(self, v_id):
        viewer_ctrl = self.getViewerController(v_id)
        self._notifySubscribers(viewer_ctrl, self._data_changed_subscribers.get(v_id, {}))

    def _notifySubscribers(self, viewer_controller, subscribers):
        def notify(s=subscribers, v=viewer_controller):
            for sub in s.values():
                sub(v)

        if viewer_controller is None:
            notify()
        else:
            executeWaitTask(viewer_controller.view.rendered, notify, [subscribers, viewer_controller])

    def _onTabClosed(self, v_id):
        ctrl, tabs = self._model.remove(v_id)
        ctrl.close()
        self._onViewerClosed(ctrl)

        if self._model.getActiveViewer() is ctrl:
            self._model.setActiveViewer(None)
            if self._model.count() != 0:  # activate another tab
                tab = list(self._model.getTabs().values())[0]
                tab.raise_()
                tab.setFocus()
        if self._model.count() == 0:
            self._notifySubscribers(None, self._viewer_changed_subscribers)

    def unsubscribe(self, sub_id):
        removed = self._viewer_changed_subscribers.pop(sub_id, None)
        if removed is not None:
            return
        removed = self._viewer_closed_subscribers.pop(sub_id, None)
        if removed is not None:
            return
        for d in self._data_changed_subscribers.values():
            removed = d.pop(sub_id, None)
            if removed is not None:
                return
