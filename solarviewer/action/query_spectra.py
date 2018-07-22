from PyQt5 import QtCore
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QDialog
from radiospectra.sources import CallistoSpectrogram

from solarviewer.app.content import ContentController
from solarviewer.config.base import ActionController, ItemConfig
from solarviewer.config.ioc import RequiredFeature
from solarviewer.ui.query_callisto import Ui_QueryCallisto
from solarviewer.util import executeLongRunningTask
from solarviewer.viewer.spectra import CallistoViewerController


class QueryCallistoActionController(ActionController):
    item_config = ItemConfig().setMenuPath("File/Open Spectrogram/Callisto/Query")
    content_ctrl: ContentController = RequiredFeature(ContentController.name)

    def onAction(self):
        dlg = QDialog()
        ui = Ui_QueryCallisto()
        ui.setupUi(dlg)

        now = QDateTime.currentDateTimeUtc()
        ui.start_time.setDateTime(now.addSecs(-2 * 60 * 60))
        ui.end_time.setDateTime(now.addSecs(-1.50 * 60 * 60))

        if dlg.exec_():
            start_time = ui.start_time.dateTime().toString(QtCore.Qt.ISODate).replace("T", " ")
            end_time = ui.end_time.dateTime().toString(QtCore.Qt.ISODate).replace("T", " ")

            executeLongRunningTask(CallistoSpectrogram.from_range, [ui.instrument.currentText(), start_time, end_time],
                                   "Downloading", self._openSpectrogram)

    def _openSpectrogram(self, spectrogram):
        viewer_ctrl = CallistoViewerController.fromSpectrogram(spectrogram)
        self.content_ctrl.addViewerController(viewer_ctrl)
