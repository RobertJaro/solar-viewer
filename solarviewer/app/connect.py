from abc import abstractmethod, ABC

from solarviewer.app.content import ContentController
from solarviewer.app.util import supported
from solarviewer.config.base import Controller, ViewerController
from solarviewer.config.ioc import RequiredFeature


class ConnectionMixin(ABC):

    @abstractmethod
    def connect(self, viewer_ctrl: ViewerController):
        raise NotImplementedError

    @abstractmethod
    def disconnect(self, viewer_ctrl: ViewerController):
        raise NotImplementedError

    @abstractmethod
    def supports(self, viewer_ctrl: ViewerController) -> bool:
        raise NotImplementedError

    @abstractmethod
    def enabled(self, value: bool):
        raise NotImplementedError


class ViewerLock(ABC):

    def __init__(self, supported_viewer_types, supported_data_types):
        self.supported_data_types = supported_data_types
        self.supported_viewer_types = supported_viewer_types

    @abstractmethod
    def release(self):
        raise NotImplementedError

    @abstractmethod
    def connect(self, viewer_ctrl: ViewerController):
        raise NotImplementedError

    @abstractmethod
    def disconnect(self, viewer_ctrl: ViewerController):
        raise NotImplementedError

    def supports(self, viewer_ctrl: ViewerController) -> bool:
        return viewer_ctrl is not None and supported(viewer_ctrl.data_type, viewer_ctrl.viewer_type,
                                                     self.supported_data_types,
                                                     self.supported_viewer_types)


class ViewerConnectionController(Controller):
    content_ctrl: ContentController = RequiredFeature(ContentController.name)

    def __init__(self):
        self.subscribers = {}
        self.connections = {}

        self.sub_vc_id = None
        self.sub_id = 0

        self.lock: ViewerLock = None
        self.active_id = -1
        self.active_sub: ConnectionMixin = None

        self.content_ctrl.subscribeViewerChanged(self._connect)

    def subscribe(self, sub: ConnectionMixin):
        self.sub_id += 1
        self.subscribers[self.sub_id] = sub

        if self.lock:
            self.lock.release()
            self.lock = None
        self._connect(self.content_ctrl.getViewerController())

        return self.sub_id

    def unsubscribe(self, s_id):
        self.subscribers.pop(s_id)
        self._connect(self.content_ctrl.getViewerController(self.active_id))

    def add_lock(self, lock: ViewerLock):
        if self.lock:
            self.lock.release()
        self.lock = lock
        self._connect(self.content_ctrl.getViewerController())
        return self.lock

    def remove_lock(self):
        if self.lock:
            self.lock.release()
        self.lock = None
        self._connect(self.content_ctrl.getViewerController())

    def _connect(self, viewer_ctrl: ViewerController):
        self._disconnectActive()
        self.active_id = viewer_ctrl.v_id if viewer_ctrl else -1
        if self.active_id != -1:
            self.active_sub = self._getFirstSupported(viewer_ctrl)
            if self.active_sub:
                self.active_sub.connect(viewer_ctrl)
        self._setEnabled()

    def _setEnabled(self):
        for sub in self.subscribers.values():
            sub.enabled(sub is self.active_sub)

    def _disconnectActive(self):
        if self.active_sub is None:
            return
        self.active_sub.disconnect(self.content_ctrl.getViewerController(self.active_id))
        self.active_sub = None

    def _getFirstSupported(self, viewer_ctrl):
        if self.lock and self.lock.supports(viewer_ctrl):
            return self.lock
        for sub in reversed(list(self.subscribers.values())):
            if sub.supports(viewer_ctrl):
                return sub
        return None
