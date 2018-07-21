from PyQt5.QtWidgets import QWidget

from solarviewer.config.base import ItemConfig, DataModel, ViewerController, DataType, ViewerType, DialogController
from solarviewer.ui.spectra_settings import Ui_SpectraSettings
from solarviewer.viewer.spectra import CallistoModel


class SpectraSettingsController(DialogController):
    item_config = ItemConfig().setMenuPath("View/Spectra Settings").setTitle("Spectrogram Settings").addSupportedData(
        DataType.SPECTROGRAM).addSupportedViewer(ViewerType.MPL)

    def setupContent(self, content_widget: QWidget):
        self._ui = Ui_SpectraSettings()
        self._ui.setupUi(content_widget)

    def onDataChanged(self, viewer_ctrl: ViewerController):
        model: CallistoModel = viewer_ctrl.model

        self._ui.vmin_check.setChecked(model.vmin is not None)
        if model.vmin:
            self._ui.vmin_spin.setValue(model.vmin)
        self._ui.vmax_check.setChecked(model.vmax is not None)
        if model.vmax:
            self._ui.vmax_spin.setValue(model.vmax)
        self._ui.substract_background_check.setChecked(model.substract_background)
        self._ui.linear_check.setChecked(model.linear)
        self._ui.color_bar_check.setChecked(model.colorbar)

    def modifyData(self, data_model: CallistoModel) -> DataModel:
        data_model.vmin = self._ui.vmin_spin.value() if self._ui.vmin_check.isChecked() else None
        data_model.vmax = self._ui.vmax_spin.value() if self._ui.vmax_check.isChecked() else None
        data_model.substract_background = self._ui.substract_background_check.isChecked()
        data_model.linear = self._ui.linear_check.isChecked()
        data_model.colorbar = self._ui.color_bar_check.isChecked()

        return data_model
