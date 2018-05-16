from PyQt5.QtGui import QStandardItemModel, QStandardItem
from qtpy import QtWidgets, QtCore
from sunpy.map import Map

from solarviewer.app.content import ContentController
from solarviewer.config.base import ItemConfig, ActionController
from solarviewer.config.ioc import RequiredFeature
from solarviewer.ui.open_composite import Ui_OpenComposite
from solarviewer.viewer.composite import CompositeMapModel, CompositeMapViewerController
from solarviewer.viewer.map import MapViewerController


class CreateCompositeMapTool(ActionController):
    content_ctrl: ContentController = RequiredFeature(ContentController.name)

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setMenuPath("File/Open SunPy Composite Map/From Active")

    def onAction(self):
        dlg = QtWidgets.QDialog()
        ui = Ui_OpenComposite()
        ui.setupUi(dlg)

        model = QStandardItemModel()
        viewer_ctrls = self.content_ctrl.getViewerControllers(MapViewerController)
        for v in viewer_ctrls:
            item = QStandardItem("{}: {}".format(v.v_id, v.getTitle()))
            item.setCheckable(True)
            item.v_id = v.v_id
            model.appendRow(item)

        ui.list.setModel(model)

        if not dlg.exec_():
            return
        map_models = self._getSelectedDataModels(model)
        if len(map_models) == 0:
            return

        c_map = self._createCompositeMap(map_models)
        model = CompositeMapModel(c_map)
        ctrl = CompositeMapViewerController.fromModel(model)
        self.content_ctrl.addViewerController(ctrl)

    def _createCompositeMap(self, models):
        maps = [m.map for m in models]
        c_map = Map(maps, composite=True)

        for i, model in enumerate(models):
            c_map.set_alpha(i, 0.5)
            settings = {"cmap": model.cmap, "norm": model.norm, "interpolation": model.interpolation,
                        "origin": model.origin}
            c_map.set_plot_settings(i, settings)
        return c_map

    def _getSelectedDataModels(self, model):
        checked_ids = []
        for index in range(model.rowCount()):
            if model.item(index).checkState() == QtCore.Qt.Checked:
                checked_ids.append(model.item(index).v_id)
        models = [self.content_ctrl.getDataModel(v_id) for v_id in checked_ids]
        return models
