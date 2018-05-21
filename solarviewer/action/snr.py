import numpy as np
from qtpy import QtWidgets

from solarviewer.app.content import ContentController
from solarviewer.config.base import ItemConfig, ViewerType, DataType, ActionController
from solarviewer.config.ioc import RequiredFeature


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
