import pickle

from qtpy import QtWidgets
from sunpy.map import GenericMap

from solarviewer.app.content import ContentController
from solarviewer.app.util import saveFits
from solarviewer.config.base import ActionController, ItemConfig, DataType, ViewerType
from solarviewer.config.ioc import RequiredFeature


class ProjectSaveWrapper:
    def __init__(self, viewer_ctrl_type, model):
        self.viewer_ctrl_type = viewer_ctrl_type
        self.model = model


class SaveProjectAction(ActionController):
    content_ctrl: ContentController = RequiredFeature(ContentController.name)

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setMenuPath("File\\Save").addSupportedData(DataType.ANY).addSupportedViewer(ViewerType.ANY)

    def onAction(self):
        ctrl = self.content_ctrl.getViewerController()
        model = ctrl.model

        if model.path:
            file = model.path
        else:
            file, _ = QtWidgets.QFileDialog.getSaveFileName(filter="Solar Viewer Project (*.svp)")
            if not file:
                return
            model.path = file

        wrapper = ProjectSaveWrapper(type(ctrl), model)
        # write to file
        bin_file = open(file, mode="wb")
        pickle.dump(wrapper, bin_file)
        bin_file.close()


class SaveAsProjectAction(ActionController):
    content_ctrl: ContentController = RequiredFeature(ContentController.name)

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setMenuPath("File\\Save As..").addSupportedData(DataType.ANY).addSupportedViewer(
            ViewerType.ANY)

    def onAction(self):
        ctrl = self.content_ctrl.getViewerController()
        model = ctrl.model

        file, _ = QtWidgets.QFileDialog.getSaveFileName(directory=model.path, filter="Solar Viewer Project (*.svp)")
        if not file:
            return
        model.path = file
        wrapper = ProjectSaveWrapper(type(ctrl), model)

        # write to file
        bin_file = open(file, mode="wb")
        pickle.dump(wrapper, bin_file)
        bin_file.close()


class OpenProjectAction(ActionController):
    content_ctrl: ContentController = RequiredFeature(ContentController.name)

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setMenuPath("File\\Open SV Project")

    def onAction(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(filter="Solar Viewer Project (*.svp)")
        if not file:
            return

        bin_file = open(file, mode="rb")
        wrapper = pickle.load(bin_file)
        ctrl = wrapper.viewer_ctrl_type.fromModel(wrapper.model)
        self.content_ctrl.addViewerCtrl(ctrl)


class SaveFitsAction(ActionController):
    content_ctrl: ContentController = RequiredFeature(ContentController.name)

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setMenuPath("File\\Export\\FITS").addSupportedData(DataType.MAP).addSupportedViewer(
            ViewerType.ANY)

    def onAction(self):
        map: GenericMap = self.content_ctrl.getDataModel().map
        saveFits(map)
