import copy

from qtpy import QtGui

from solarviewer.app.content import ContentController
from solarviewer.config.base import ItemConfig, Controller, ActionController, DataType, ViewerType
from solarviewer.config.ioc import RequiredFeature


class HistoryController(Controller):
    viewers = {}
    skip_next_change = False
    content_ctrl: ContentController = RequiredFeature(ContentController.name)

    def __init__(self):
        self.content_ctrl.subscribeViewerAdded(self.onViewerAdded)

    def undo(self, id):
        history = self.viewers[id]
        if len(history) <= 1:
            return None
        del history[-1]
        # change event will be triggered by undo
        self.skip_next_change = True
        self.content_ctrl.setDataModel(copy.deepcopy(history[-1]), id)

    def onViewerAdded(self, viewer_ctrl):
        self.viewers[viewer_ctrl.v_id] = [viewer_ctrl.model]
        self.content_ctrl.subscribeDataChange(viewer_ctrl.v_id, self.onDataChanged)

    def onDataChanged(self, viewer_ctrl):
        if self.skip_next_change:
            self.skip_next_change = False
            return
        history = self.viewers[viewer_ctrl.v_id]
        if (len(history) > 10):
            del history[0]
        history.append(viewer_ctrl.model)


class UndoAction(ActionController):
    history = RequiredFeature(HistoryController.name)
    content_ctrl: ContentController = RequiredFeature(ContentController.name)

    def __init__(self):
        ActionController.__init__(self)

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setTitle("History").setMenuPath("Edit\\Undo").addSupportedData(
            DataType.ANY).addSupportedViewer(ViewerType.ANY).setShortcut(QtGui.QKeySequence("Ctrl+Z"))

    def onAction(self):
        id = self.content_ctrl.getCurrentId()
        self.history.undo(id)
