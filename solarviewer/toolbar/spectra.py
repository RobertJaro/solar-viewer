import copy

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QDateTime
from radiospectra.sources import CallistoSpectrogram

from solarviewer.app.content import ContentController
from solarviewer.config.base import ToolbarConfig, ViewerType, DataType
from solarviewer.config.impl import ToolbarController
from solarviewer.config.ioc import RequiredFeature
from solarviewer.ui.time_range import Ui_TimeRange
from solarviewer.util import executeLongRunningTask
from solarviewer.viewer.spectra import CallistoModel


class SpectraToolbarController(ToolbarController):
    item_config = ToolbarConfig().addSupportedViewer(ViewerType.ANY).addSupportedData(DataType.SPECTROGRAM).setMenuPath(
        "View/Toolbar/Spectra").setOrientation(QtCore.Qt.TopToolBarArea)

    content_ctrl: ContentController = RequiredFeature(ContentController.name)

    def setup(self, toolbar_widget: QtWidgets.QToolBar):
        left_icon = QtGui.QIcon(":/image/double_left.png")
        right_icon = QtGui.QIcon(":/image/double_right.png")
        range_icon = QtGui.QIcon(":/image/range.png")
        add_icon = QtGui.QIcon(":/image/add.png")

        extend_start = toolbar_widget.addAction(left_icon, "Extend Start")
        extend_end = toolbar_widget.addAction(right_icon, "Extend End")
        range = toolbar_widget.addAction(range_icon, "Set Range")
        add = toolbar_widget.addAction(add_icon, "Add File")

        extend_start.triggered.connect(self.onExtendStart)
        extend_end.triggered.connect(self.onExtendEnd)
        range.triggered.connect(self.onSetRange)
        add.triggered.connect(self.onAddFile)

    def onExtendStart(self):
        v_id = self.content_ctrl.getViewerController().v_id
        executeLongRunningTask(self._extendAction, [-15], "Downloading", self.content_ctrl.setDataModel, [v_id])

    def onExtendEnd(self):
        v_id = self.content_ctrl.getViewerController().v_id
        executeLongRunningTask(self._extendAction, [15], "Downloading", self.content_ctrl.setDataModel, [v_id])

    def onSetRange(self):
        v_id = self.content_ctrl.getViewerController().v_id
        model: CallistoModel = self.content_ctrl.getDataModel()
        dlg = _RangeDialog(model.spectrogram.start, model.spectrogram.end)
        if dlg.exec_():
            model_c = copy.deepcopy(model)
            model_c.spectrogram = model.spectrogram.in_interval(dlg.getStartTime(), dlg.getEndTime())
            self.content_ctrl.setDataModel(model_c, v_id)

    def onAddFile(self):
        v_id = self.content_ctrl.getViewerController().v_id
        paths, _ = QtWidgets.QFileDialog.getOpenFileNames(None, caption="Select Extend File",
                                                          filter="FITS files (*.fits; *.fit; *.fts)")
        if paths:
            model: CallistoModel = copy.deepcopy(self.content_ctrl.getDataModel())
            spectra = [CallistoSpectrogram.read(p) for p in paths]
            spectra.append(model.spectrogram)
            model.spectrogram = CallistoSpectrogram.join_many(spectra)
            self.content_ctrl.setDataModel(model, v_id)

    def _extendAction(self, minutes):
        model: CallistoModel = copy.deepcopy(self.content_ctrl.getDataModel())
        model.spectrogram = model.spectrogram.extend(minutes)
        return model

    def onClose(self):
        pass


class _RangeDialog(QtWidgets.QDialog):
    def __init__(self, start, end):
        QtWidgets.QDialog.__init__(self)

        layout = QtWidgets.QVBoxLayout(self)
        range_widget = QtWidgets.QWidget(self)
        self._ui = Ui_TimeRange()
        self._ui.setupUi(range_widget)
        layout.addWidget(range_widget)

        button_box = QtWidgets.QDialogButtonBox(self)
        button_box.setOrientation(QtCore.Qt.Horizontal)
        button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        layout.addWidget(button_box)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        self._ui.from_time.setDateTime(QDateTime(start))
        self._ui.to_time.setDateTime(QDateTime(end))

    def getStartTime(self):
        return self._ui.from_time.dateTime().toPyDateTime()

    def getEndTime(self):
        return self._ui.to_time.dateTime().toPyDateTime()
