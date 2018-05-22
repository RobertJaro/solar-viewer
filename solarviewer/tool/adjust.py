import numpy as np
from PyQt5.QtWidgets import QWidget

from solarviewer.config.base import ItemConfig, ViewerType, DataType, DataModel
from solarviewer.config.impl import DataToolController
from solarviewer.ui.adjust import Ui_AdjustData
from solarviewer.viewer.map import MapModel


class ValueAdjustmentController(DataToolController):

    def setupContent(self, content_widget: QWidget):
        self._ui = Ui_AdjustData()
        self._ui.setupUi(content_widget)

    def onDataChanged(self, viewer_ctrl):
        model: MapModel = viewer_ctrl.model
        norm_vmax, norm_vmin, vmax, vmin = self._getRange(model)
        self._ui.range_max_spin.setRange(vmin, vmax)
        self._ui.range_max_spin.setValue(norm_vmax)
        self._ui.range_min_spin.setRange(vmin, vmax)
        self._ui.range_min_spin.setValue(norm_vmin)
        self._ui.clip_spin.setRange(vmin, vmax)

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setTitle("Value Adjustment").setMenuPath("Tools/Adjust Data").addSupportedData(
            DataType.MAP).addSupportedViewer(ViewerType.ANY)

    def modifyData(self, data_model: DataModel) -> DataModel:
        d = data_model.data
        if self._ui.clip_radio.isChecked():
            limit = self._ui.clip_spin.value()
            data_model.setData(d.clip(limit))
        if self._ui.offset_radio.isChecked():
            min_value = np.nanmin(d)
            offset = self._ui.offset_spin.value()
            data_model.setData(d - min_value + offset)
            data_model.norm.vmin += offset - min_value
            data_model.norm.vmax += offset - min_value
        if self._ui.range_radio.isChecked():
            vmin = self._ui.range_min_spin.value()
            vmax = self._ui.range_max_spin.value()
            data_model.setData(np.clip(d, vmin, vmax))

        self._adjustNorm(data_model)
        return data_model

    def _adjustNorm(self, data_model):
        norm_vmax, norm_vmin, vmax, vmin = self._getRange(data_model)
        if norm_vmax > vmax:
            norm_vmax = vmax
        if norm_vmin < vmin:
            norm_vmin = vmin
        data_model.norm.vmin = norm_vmin
        data_model.norm.vmax = norm_vmax

    def _getRange(self, model):
        norm = model.norm
        vmin = np.nanmin(model.data)
        vmax = np.nanmax(model.data)
        norm_vmin = norm.vmin if norm.vmin != None and norm.vmin >= vmin else vmin
        norm_vmax = norm.vmax if norm.vmax != None and norm.vmax <= vmax else vmax
        return norm_vmax, norm_vmin, vmax, vmin
