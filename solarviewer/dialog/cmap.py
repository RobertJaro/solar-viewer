import matplotlib
import sunpy
from matplotlib.colors import Colormap

from solarviewer.config.base import DialogController, ItemConfig, ViewerType, DataType, ViewerController, DataModel
from solarviewer.ui.cmap import Ui_Colormap


class CmapController(DialogController):
    def __init__(self):
        DialogController.__init__(self)

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setTitle("Select Coloramap").setMenuPath("Edit\\Change Colormap").addSupportedViewer(
            ViewerType.MPL).addSupportedData(DataType.MAP).addSupportedData(DataType.PLAIN_2D)

    def setupContent(self, content_widget):
        self._ui = Ui_Colormap()
        self._ui.setupUi(content_widget)

        choices = []
        choices.extend(sunpy.cm.cmlist.values())
        choices.extend(matplotlib.cm.cmap_d.values())
        self.cmaps = {cmap.name: cmap for cmap in choices}
        items = list(self.cmaps.keys())
        items.sort()
        self._ui.cmap_combo.addItems(items)

    def onDataChanged(self, viewer_ctrl: ViewerController):
        cmap_name = None
        if isinstance(viewer_ctrl.model.cmap, Colormap):
            cmap_name = viewer_ctrl.model.cmap.name
        if isinstance(viewer_ctrl.model.cmap, str):
            cmap_name = viewer_ctrl.model.cmap
        if cmap_name is not None:
            self._ui.cmap_combo.setCurrentText(cmap_name)

    def modifyData(self, model: DataModel):
        model.cmap = self.cmaps[self._ui.cmap_combo.currentText()]
        return model
