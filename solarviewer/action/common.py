import copy

import numpy as np
from qtpy import QtWidgets

from solarviewer.app.content import ContentController
from solarviewer.config.base import ItemConfig, ViewerType, DataType, ActionController
from solarviewer.config.ioc import RequiredFeature
from solarviewer.util import executeLongRunningTask


class CutController(ActionController):
    content_ctrl: ContentController = RequiredFeature(ContentController.name)

    def onAction(self):
        viewer_ctrl = self.content_ctrl.getViewerController()
        call_after = lambda result: self.content_ctrl.setDataModel(result)
        executeLongRunningTask(self._action, [viewer_ctrl], "Executing Action", call_after)

    def _action(self, viewer_ctrl):
        submap = viewer_ctrl.getZoomedMap()
        data_copy = copy.deepcopy(viewer_ctrl.model)
        data_copy.map = submap
        return data_copy

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setMenuPath("Edit/Crop To Current View").addSupportedViewer(
            ViewerType.MPL).addSupportedData(DataType.MAP)


class SNRController(ActionController):
    content_ctrl: ContentController = RequiredFeature(ContentController.name)

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setMenuPath("Help/Calculate SNR").addSupportedViewer(
            ViewerType.MPL).addSupportedData(DataType.MAP)

    def onAction(self):
        data = self.content_ctrl.getViewerController().getZoomedData()
        snr = np.mean(data) / np.std(data)
        message = "Estimated SNR: {0:.7}".format(float(snr))
        QtWidgets.QMessageBox.information(None, "SNR", message)
