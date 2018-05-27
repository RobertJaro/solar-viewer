import astropy.units as u
import numpy as np
from sunpy.map import Map

from solarviewer.config.base import DialogController, DataModel, ViewerController, ItemConfig, DataType, ViewerType
from solarviewer.ui.plot_settings import Ui_PlotSettings


class PlotSettingsController(DialogController):

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().addSupportedData(DataType.MAP).addSupportedViewer(ViewerType.MPL).setMenuPath(
            "View/Plot Settings").setTitle("Plot Settings")

    def setupContent(self, content_widget):
        self._ui = Ui_PlotSettings()
        self._ui.setupUi(content_widget)

    def onDataChanged(self, viewer_ctrl: ViewerController):
        plot_settings = viewer_ctrl.model.plot_preferences
        self._ui.color_bar.setChecked(plot_settings["show_colorbar"])
        self._ui.limb.setChecked(plot_settings["show_limb"])
        self._ui.grid.setChecked(plot_settings["draw_grid"])
        self._ui.mask.setChecked(plot_settings["mask"])
        if plot_settings["contours"]:
            self._ui.contours.setChecked(True)
            self._ui.contours_list.setText(" ".join(map(str, plot_settings["contours"])))
        else:
            self._ui.contours.setChecked(False)
            self._ui.contours_list.setText("10 20 30 40 50 60 70 80 90 ")

    def modifyData(self, data_model: DataModel) -> DataModel:
        plot_settings = data_model.plot_preferences
        plot_settings["show_colorbar"] = self._ui.color_bar.isChecked()
        plot_settings["show_limb"] = self._ui.limb.isChecked()
        plot_settings["draw_grid"] = self._ui.grid.isChecked()
        plot_settings["mask"] = self._ui.mask.isChecked()

        if self._ui.mask.isChecked():
            s_map = data_model.map
            data_model.map = Map(s_map.data, s_map.meta, mask=self._createMask(s_map))
        else:
            s_map = data_model.map
            data_model.map = Map(s_map.data, s_map.meta)

        if self._ui.contours.isChecked():
            strings = self._ui.contours_list.text().split(" ")
            levels = [int(s) for s in set(strings) if s != ""]
            plot_settings["contours"] = levels
        else:
            plot_settings["contours"] = False
        return data_model

    def _createMask(self, s_map):
        x, y = np.meshgrid(*[np.arange(v.value) for v in s_map.dimensions]) * u.pixel
        hpc_coords = s_map.pixel_to_data(x, y)
        r = np.sqrt(hpc_coords.Tx ** 2 + hpc_coords.Ty ** 2) / s_map.rsun_obs
        mask = np.ma.masked_less_equal(r, 1)
        palette = s_map.plot_settings['cmap']
        palette.set_bad('black')
        return mask.mask
