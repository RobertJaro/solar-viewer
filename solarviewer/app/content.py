import time
from threading import Thread
from typing import Callable

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTabWidget, QWidget
from qtpy import QtWidgets

from solarviewer.config.base import ViewerController, Controller, DataModel


class ContentModel:
    def __init__(self):
        self._viewers = {}

    def addViewerCtrl(self, viewer):
        self._viewers[viewer.v_id] = viewer

    def setData(self, v_id, model):
        self._viewers[v_id].setModel(model)

    def getViewerCtrl(self, v_id) -> ViewerController:
        return self._viewers.get(v_id, None)

    def getViewerCtrls(self):
        return self._viewers


class ContentController(Controller):
    """Main Controller for content storage and representation"""
    sub_id = 0

    def __init__(self):
        self._model = ContentModel()

        self._viewer_changed_subscribers = {}
        self._viewer_added_subscribers = {}
        self._viewer_closed_subscribers = {}
        self._data_changed_subscribers = {}

        self._view = QTabWidget()
        self._view.setTabsClosable(True)
        self._view.setMovable(True)
        self._view.setObjectName("tabWidget")

        self._view.currentChanged.connect(self._onViewerChanged)
        self._view.tabCloseRequested.connect(self._onCloseTab)

    @property
    def view(self) -> QTabWidget:
        return self._view

    def getViewerController(self, v_id=-1) -> ViewerController:
        """Returns data model of viewer with id=v_id. If id is -1 the currently viewed data model will be returned."""
        if v_id == -1:
            v_id = self.getCurrentId()
        if v_id == -1:  # No tab open
            return None
        viewer_ctrl = self._model.getViewerCtrl(v_id)
        return viewer_ctrl

    def getDataModel(self, v_id=-1) -> DataModel:
        """Returns data model of viewer with id=v_id. If id is -1 the currently viewed data model will be returned."""
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
        wrapper = self._view.currentWidget()
        return wrapper.v_id if wrapper is not None else -1

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

    def subscribeDataChange(self, v_id, action):
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

    def addViewerCtrl(self, viewer_ctrl):
        self._model.addViewerCtrl(viewer_ctrl)
        v_id = viewer_ctrl.v_id
        viewer = viewer_ctrl.view
        wrapper = QWidget()
        wrapper.v_id = v_id
        layout = QtWidgets.QHBoxLayout(wrapper)
        layout.addWidget(viewer)
        index = self._view.addTab(wrapper, viewer_ctrl.getTitle())
        self._view.setCurrentIndex(index)
        self._onViewerAdded(viewer_ctrl)

    def _onViewerChanged(self, *args):
        v = self.getViewerController()
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

        thread = _RenderDelayThread(viewer_controller)
        thread.finished.connect(notify)
        thread.start()

    def _onCloseTab(self, index):
        v_id = self._view.widget(index).v_id
        ctrl = self._model.getViewerCtrl(v_id)
        self._onViewerClosed(ctrl)
        ctrl.close()
        self._view.removeTab(index)
        if self._view.count() == 0:
            self._onViewerChanged()

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


class _RenderDelayThread(QtCore.QObject, Thread):
    finished = pyqtSignal()

    def __init__(self, viewer_ctrl):
        QtCore.QObject.__init__(self)
        Thread.__init__(self)
        self.viewer_ctrl = viewer_ctrl

    def run(self):
        while self.viewer_ctrl is not None and not self.viewer_ctrl.view.rendered:
            time.sleep(0.001)
        self.finished.emit()
