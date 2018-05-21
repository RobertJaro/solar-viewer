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
        if self._ui.contours.isChecked():
            strings = self._ui.contours_list.text().split(" ")
            levels = [int(s) for s in set(strings) if s != ""]
            plot_settings["contours"] = levels
        else:
            plot_settings["contours"] = False
        return data_model
