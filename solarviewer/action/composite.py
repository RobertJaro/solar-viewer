from PyQt5.QtGui import QStandardItemModel, QStandardItem
from qtpy import QtWidgets, QtCore
from sunpy.image.coalignment import mapcube_coalign_by_match_template
from sunpy.map import Map
from sunpy.physics.solar_rotation import mapcube_solar_derotate

from solarviewer.app.content import ContentController
from solarviewer.config.base import ItemConfig, ActionController, DataType, DataModel, ViewerType
from solarviewer.config.impl import DataActionController
from solarviewer.config.ioc import RequiredFeature
from solarviewer.ui.open_composite import Ui_OpenComposite
from solarviewer.viewer.composite import CompositeMapModel, CompositeMapViewerController


class DerotateController(DataActionController):

    def modifyData(self, data_model: CompositeMapModel) -> DataModel:
        mc = Map(data_model.getMaps(), cube=True)
        derotated = mapcube_solar_derotate(mc)
        data_model.updateMaps(derotated.maps)
        return data_model

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setMenuPath("Edit/Composite Map/Derotate").addSupportedViewer(
            ViewerType.ANY).addSupportedData(DataType.MAP_COMPOSITE)


class CoalignController(DataActionController):

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setMenuPath("Edit/Composite Map/Coalign").addSupportedViewer(
            ViewerType.ANY).addSupportedData(DataType.MAP_COMPOSITE)

    def modifyData(self, data_model: CompositeMapModel) -> DataModel:
        mc = Map(data_model.getMaps(), cube=True)
        coaligned = mapcube_coalign_by_match_template(mc)
        data_model.updateMaps(coaligned.maps)
        return data_model


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
        viewer_ctrls = self.content_ctrl.getViewerControllers(DataType.MAP)
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

        model = self._createModel(map_models)
        ctrl = CompositeMapViewerController.fromModel(model)
        self.content_ctrl.addViewerController(ctrl)

    def _createModel(self, models):
        # preserve plot settings
        for i, model in enumerate(models):
            settings = {"cmap": model.cmap, "norm": model.norm, "interpolation": model.interpolation,
                        "origin": model.origin}
            model.map.plot_settings = settings

        comp_model = CompositeMapModel([model.map for model in models])
        return comp_model

    def _getSelectedDataModels(self, model):
        checked_ids = []
        for index in range(model.rowCount()):
            if model.item(index).checkState() == QtCore.Qt.Checked:
                checked_ids.append(model.item(index).v_id)
        models = [self.content_ctrl.getDataModel(v_id) for v_id in checked_ids]
        return models
