from PyQt5.QtWidgets import QWidget
from qtpy import QtWidgets

from solarviewer.config.base import ItemConfig, DataModel, DataType, ViewerType
from solarviewer.config.impl import DataToolController
from solarviewer.ui.composite_form import Ui_CompositeForm
from solarviewer.viewer.composite import CompositeMapModel


class CompositeSettingsController(DataToolController):

    def __init__(self):
        DataToolController.__init__(self)
        self.settings_forms = {}

    def setupContent(self, content_widget: QWidget):
        layout = QtWidgets.QVBoxLayout()
        content_widget.setLayout(layout)

        self.tool_box = QtWidgets.QToolBox()
        layout.addWidget(self.tool_box)
        layout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

    def onDataChanged(self, viewer_ctrl):
        # remove old
        for i in range(self.tool_box.count()):
            self.tool_box.removeItem(0)
        self.settings_forms.clear()

        # add new
        model: CompositeMapModel = viewer_ctrl.model
        for c_id, (m, settings) in model.maps.items():
            view, ui = self._createSettingsForm(settings)
            self.settings_forms[c_id] = ui
            self.tool_box.addItem(view, m.name)

    def modifyData(self, data_model: CompositeMapModel) -> DataModel:
        for c_id, ui in self.settings_forms.items():
            _, settings = data_model.maps[c_id]
            settings["zorder"] = ui.order.value()
            settings["alpha"] = ui.alpha_spin.value()
            if ui.levels_check.isChecked():
                strings = ui.levels_list.text().split(" ")
                levels = sorted([int(s) for s in set(strings) if s != ""])
                settings["levels"] = levels
            else:
                settings["levels"] = False

        return data_model

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setTitle("Composite Map Settings").setMenuPath(
            "View/Composite Map/Settings").addSupportedData(DataType.MAP_COMPOSITE).addSupportedViewer(ViewerType.ANY)

    def _createSettingsForm(self, settings):
        setting = QtWidgets.QWidget()
        ui = Ui_CompositeForm()
        ui.setupUi(setting)

        ui.order.setValue(settings["zorder"])
        ui.alpha_spin.setValue(settings["alpha"])
        if settings["levels"]:
            ui.levels_check.setChecked(True)
            ui.levels_list.setText(" ".join(map(str, settings["levels"])))
        else:
            ui.levels_check.setChecked(False)
            ui.levels_list.setText("10 20 30 40 50 60 70 80 90")

        return setting, ui
