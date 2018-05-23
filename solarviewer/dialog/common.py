from astropy import units as u

from solarviewer.config.base import DialogController, ItemConfig, ViewerType, DataType, DataModel, ViewerController
from solarviewer.ui.rotate import Ui_Rotate
from solarviewer.viewer.map import MapModel


class RotateController(DialogController):
    def __init__(self):
        DialogController.__init__(self)

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setTitle("Rotate").setMenuPath("Edit/Rotate").addSupportedViewer(
            ViewerType.ANY).addSupportedData(DataType.MAP)

    def setupContent(self, content_widget):
        self._ui = Ui_Rotate()
        self._ui.setupUi(content_widget)

    def onDataChanged(self, viewer_ctrl: ViewerController):
        pass

    def modifyData(self, data_model: MapModel) -> DataModel:
        rotated_map = data_model.map.rotate(angle=self._ui.angle_spin.value() * u.deg)
        data_model.map = rotated_map
        return data_model
