from threading import Thread

from PyQt5.QtCore import QDateTime, pyqtSignal
from qtpy import QtWidgets, QtCore
from sunpy.net import hek
from sunpy.net.hek2vso import hek2vso

from solarviewer.config.base import ToolController, ItemConfig
from solarviewer.config.ioc import RequiredFeature
from solarviewer.tool.download_result import DownloadResultController
from solarviewer.ui.download_event import Ui_DownloadEvent


class EventController(ToolController):  #

    result_ctrl: DownloadResultController = RequiredFeature(DownloadResultController.name)

    def __init__(self):
        self.query_id = 0

        ToolController.__init__(self)
        self._view = QtWidgets.QWidget()
        self._ui = Ui_DownloadEvent()
        self._ui.setupUi(self._view)
        self._ui.message_box.hide()
        self.table = self._ui.table

        self._ui.event_type.addItems([c().item.upper() for c in hek.attrs.EventType.__subclasses__()])

        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        now = QDateTime.currentDateTimeUtc()
        self._ui.from_date.setDateTime(now.addSecs(-2 * 60 * 60))
        self._ui.to_date.setDateTime(now.addSecs(-1.50 * 60 * 60))

        self._ui.search_button.clicked.connect(self._onSearch)
        self._ui.query_button.clicked.connect(self._onQuery)

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setTitle("Event Download Tool").setMenuPath("File/HEK")

    @property
    def view(self) -> QtWidgets:
        return self._view

    def _onSearch(self):
        self._ui.message_box.hide()
        try:
            self._ui.search_button.setEnabled(False)
            self._ui.search_button.setText("Loading...")

            self.table.setRowCount(0)

            start = self._ui.from_date.dateTime().toString(QtCore.Qt.ISODate)
            end = self._ui.to_date.dateTime().toString(QtCore.Qt.ISODate)
            event = self._ui.event_type.currentText()
            attrs = [hek.attrs.Time(start=start, end=end), hek.attrs.EventType(event)]
            thread = _SearchThread(attrs)
            thread.finished.connect(self._onSearchResult)
            thread.start()
        except Exception as ex:
            self._ui.message_label.setText("Invalid Query: " + str(ex))
            self._ui.message_box.show()

    def _onQuery(self):
        indexes = self.table.selectedIndexes()
        if len(indexes) == 0:
            return

        vso_query = hek2vso.translate_results_to_query(self.query[indexes[0].row()])
        self.result_ctrl.query(vso_query[0])

    def _onSearchResult(self, query):
        self.query = query
        self.table.setRowCount(len(query))
        for index, item in enumerate(query):
            location = self._createLocation(item)
            self.table.setItem(index, 0, QtWidgets.QTableWidgetItem(item["event_type"]))
            self.table.setItem(index, 1, QtWidgets.QTableWidgetItem(item["event_starttime"]))
            self.table.setItem(index, 2, QtWidgets.QTableWidgetItem(item["event_endtime"]))
            self.table.setItem(index, 3, QtWidgets.QTableWidgetItem(location))
            self.table.setItem(index, 4, QtWidgets.QTableWidgetItem(item["obs_observatory"]))
            self.table.setItem(index, 5, QtWidgets.QTableWidgetItem(item["obs_instrument"]))
            self.table.setItem(index, 6, QtWidgets.QTableWidgetItem(item["obs_channelid"]))
            self.table.setItem(index, 7, QtWidgets.QTableWidgetItem(item["frm_name"]))
        self._ui.search_button.setEnabled(True)
        self._ui.search_button.setText("Search")

    def _createLocation(self, item):
        event_coordunit = item["event_coordunit"]
        if not event_coordunit:
            return ""
        location = "( "
        if item["event_coord1"] is not None:
            location += str(item["event_coord1"])
        if item["event_coord2"] is not None:
            location += ", " + str(item["event_coord2"])
        if item["event_coord3"] is not None:
            location += ", " + str(item["event_coord3"])
        location += " ) " + event_coordunit
        return location


class _SearchThread(QtCore.QObject, Thread):
    finished = pyqtSignal(object)

    def __init__(self, attrs):
        self.attrs = attrs
        self.client = hek.HEKClient()

        QtCore.QObject.__init__(self)
        Thread.__init__(self)

    def run(self):
        query = self.client.search(*self.attrs)
        self.finished.emit(query)
