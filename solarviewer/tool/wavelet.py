import numpy as np
import pywt
from PyQt5.QtWidgets import QWidget
from skimage.restoration import estimate_sigma

from solarviewer.config.base import ItemConfig, DataModel, DataType, ViewerType
from solarviewer.config.impl import DataToolController
from solarviewer.ui.wavelet import Ui_Wavelet


class WaveletController(DataToolController):

    def setupContent(self, content_widget: QWidget):
        self.ui = Ui_Wavelet()
        self.ui.setupUi(content_widget)

        self.ui.level_spin.setMinimum(1)
        families = pywt.families(False)
        self.ui.wavelet_family_combo.addItems(families)
        self.ui.wavelet_combo.addItems(pywt.wavelist(pywt.families()[self.ui.wavelet_family_combo.currentIndex()]))
        self.ui.wavelet_family_combo.currentIndexChanged.connect(self._onFamilyChanged)

    def onDataChanged(self, viewer_ctrl):
        estimated_sigma = estimate_sigma(viewer_ctrl.model.data)
        self.ui.sigma_spin.setValue(estimated_sigma)

    def modifyData(self, data_model: DataModel) -> DataModel:
        noise_sigma = self.ui.sigma_spin.value()
        wavelet = self.ui.wavelet_combo.currentText()
        level = self.ui.level_spin.value()

        wc = pywt.wavedec2(data=data_model.data, wavelet=wavelet, level=level)

        threshold = noise_sigma * np.sqrt(2 * np.log(data_model.data.size))

        nwc = map(lambda x: pywt.threshold(x, threshold), wc)
        data_model.setData(pywt.waverec2(list(nwc), wavelet=wavelet))
        return data_model

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setTitle("Wavelet Filter").setMenuPath("Tools/Wavelet Filter").addSupportedData(
            DataType.MAP).addSupportedData(DataType.PLAIN_2D).addSupportedViewer(ViewerType.ANY)

    def _onFamilyChanged(self, index):
        self.ui.wavelet_combo.clear()
        self.ui.wavelet_combo.addItems(pywt.wavelist(pywt.families()[index]))
