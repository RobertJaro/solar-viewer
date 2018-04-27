import os
import pickle

import matplotlib
from PyQt5.QtWidgets import QFileDialog
from qtpy import QtWidgets
from sunpy.map import GenericMap

from solarviewer.app.content import ContentController
from solarviewer.app.util import saveFits
from solarviewer.config.base import ActionController, ItemConfig, DataType, ViewerType
from solarviewer.config.ioc import RequiredFeature
from solarviewer.ui.save_image import Ui_SaveImage


class ProjectSaveWrapper:
    def __init__(self, viewer_ctrl_type, model):
        self.viewer_ctrl_type = viewer_ctrl_type
        self.model = model


class SaveProjectAction(ActionController):
    content_ctrl: ContentController = RequiredFeature(ContentController.name)

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setMenuPath("File/Save").addSupportedData(DataType.ANY).addSupportedViewer(ViewerType.ANY)

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
        return ItemConfig().setMenuPath("File/Save As..").addSupportedData(DataType.ANY).addSupportedViewer(
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
        return ItemConfig().setMenuPath("File/Open SV Project")

    def onAction(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(filter="Solar Viewer Project (*.svp)")
        if not file:
            return

        bin_file = open(file, mode="rb")
        wrapper = pickle.load(bin_file)
        ctrl = wrapper.viewer_ctrl_type.fromModel(wrapper.model)
        self.content_ctrl.addViewerCtrl(ctrl)
        bin_file.close()


class SaveFitsAction(ActionController):
    content_ctrl: ContentController = RequiredFeature(ContentController.name)

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setMenuPath("File/Export/FITS").addSupportedData(DataType.MAP).addSupportedViewer(
            ViewerType.ANY)

    def onAction(self):
        map: GenericMap = self.content_ctrl.getDataModel().map
        saveFits(map)


class SaveImageController(ActionController):
    content_ctrl: ContentController = RequiredFeature(ContentController.name)

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setMenuPath("File/Export/Image").addSupportedData(DataType.ANY).addSupportedViewer(
            ViewerType.MPL)

    def onAction(self):
        ui = Ui_SaveImage()
        dlg = QtWidgets.QDialog()
        ui.setupUi(dlg)
        ui.dpi_spin.setEnabled(False)

        view = self.content_ctrl.getViewerController().view
        figure = view.figure
        canvas = view.canvas

        filters, selectedFilter = self.getFilter(canvas)

        def selectFile():
            path = \
                QFileDialog.getSaveFileName(directory=ui.file_path.text(), filter=filters,
                                            initialFilter=selectedFilter)[0]
            if path:
                ui.file_path.setText(path)

        ui.file_select.clicked.connect(selectFile)

        startpath = os.path.expanduser(
            matplotlib.rcParams['savefig.directory'])
        start = os.path.join(startpath, canvas.get_default_filename())
        ui.file_path.setText(start)

        if not dlg.exec_():
            return

        path = ui.file_path.text()
        dpi = ui.dpi_spin.value() if ui.dpi_check.isChecked() else None

        figure.savefig(path, dpi=dpi, transparent=ui.transparent_check.isChecked())

    def getFilter(self, canvas):
        filetypes = canvas.get_supported_filetypes_grouped()
        sorted_filetypes = [(k, v) for k, v in filetypes.items()]
        sorted_filetypes.sort()
        default_filetype = canvas.get_default_filetype()
        filters = []
        selectedFilter = None
        for name, exts in sorted_filetypes:
            exts_list = " ".join(['*.%s' % ext for ext in exts])
            filter = '%s (%s)' % (name, exts_list)
            if default_filetype in exts:
                selectedFilter = filter
            filters.append(filter)
        filters = ';;'.join(filters)
        return filters, selectedFilter
