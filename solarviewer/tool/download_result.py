import copy
from threading import Thread

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QTableWidgetItem
from dateutil import parser
from qtpy import QtWidgets, QtCore
from sunpy.database import Database, tables
from sunpy.net import Fido

from solarviewer.app.app import AppController
from solarviewer.app.content import ContentController
from solarviewer.config.base import ToolController, ItemConfig
from solarviewer.config.ioc import RequiredFeature
from solarviewer.ui.download_result import Ui_DownloadResult
from solarviewer.ui.result_tab import Ui_ResultTab
from solarviewer.viewer.map import MapViewerController

columns = [
    ["", lambda item: item.fileid if hasattr(item, "fileid") else None],
    ["Start Time", lambda item: parser.parse(item.time.start).isoformat() if hasattr(item.time, "start") else "None"],
    ["End Time", lambda item: parser.parse(item.time.end).isoformat() if hasattr(item.time, "end") else "None"],
    ["Instrument", lambda item: getattr(item, "instrument", "None")],
    ["Source", lambda item: getattr(item, "source", "None")],
    ["Provider", lambda item: getattr(item, "provider", "None")],
    ["Type", lambda item: getattr(getattr(item, "extent", None), "type", "None")],
    ["Wavelength", lambda item: "{} - {}".format(item.wave.wavemin, item.wave.wavemax)
    if hasattr(item, "wave") and hasattr(item.wave, "wavemin") and hasattr(item.wave, "wavemax") else "None"],
    ["Physical Observable", lambda item: getattr(item, "physobs", "None")]
]


class DownloadResultController(ToolController):
    queries = {}
    app_ctrl: AppController = RequiredFeature(AppController.__name__)
    content_ctrl: ContentController = RequiredFeature(ContentController.name)

    def __init__(self):
        self._view = QtWidgets.QWidget()
        self._ui = Ui_DownloadResult()
        self._ui.setupUi(self._view)

        self._ui.tabs.clear()
        self._ui.tabs.tabCloseRequested.connect(self._onRemoveTab)

        self.database = Database()

        self.tabs = {}
        self.queries = {}
        self.query_id = 0
        self.loading = []
        self.loaded = {entry.fileid: entry.path for entry in list(self.database)}

        self._ui.download_button.clicked.connect(lambda evt: self._onDownloadSelected())
        self._ui.open_button.clicked.connect(lambda evt: self._onOpenSelected())

    def query(self, attrs):
        # open tool if not already opened
        self.app_ctrl.openController(self.name)

        self.query_id += 1

        # add pending tab
        tab = ResultTab(self.query_id)
        self.tabs[self.query_id] = tab
        index = self._ui.tabs.addTab(tab, "Query " + str(self.query_id))
        self._ui.tabs.setCurrentIndex(index)
        # start query
        thread = _QueryThread(*attrs)
        thread.query_finished.connect(lambda query, id=self.query_id: self._onQueryResult(id, query))
        thread.start()
        # register events
        tab.download.connect(lambda f_id, q_id=self.query_id: self.download(q_id, f_id))
        tab.open.connect(lambda f_id: self._onOpen(f_id))

    def _onQueryResult(self, id, query):
        if id not in self.tabs:
            return
        query_model = self._convertQuery(query)
        self.tabs[id].loadQuery(query_model)
        self.tabs[id].setLoading(self.loading)
        self.tabs[id].setLoaded(self.loaded.keys())
        self.queries[id] = query

    def download(self, q_id, f_id):
        req = copy.copy(self.queries[q_id])
        req._list = [copy.copy(r) for r in req]
        for resp in req:
            resp[:] = [item for item in resp if item.fileid == f_id]

        self._addLoading([f_id])
        thread = _DownloadThread(req)
        thread.download_finished.connect(lambda path, f=f_id, r=req: self._onDownloadResult(f_id, path[0], req))
        thread.start()

    def _onDownloadResult(self, f_id, path, request):
        entry = list(tables.entries_from_fido_search_result(request, self.database.default_waveunit))[0]
        entry.path = path
        self.database.add(entry)
        self.database.commit()
        self._addLoaded({f_id: path})

    def _onOpen(self, f_id):
        viewer = MapViewerController.fromFile(self.loaded[f_id])
        self.content_ctrl.addViewerController(viewer)

    def _onRemoveTab(self, index):
        tab = self._ui.tabs.widget(index)
        self._ui.tabs.removeTab(index)
        self.tabs.pop(tab.q_id)

    def _onDownloadSelected(self):
        tab = self._ui.tabs.currentWidget()
        f_ids = tab.getSelectedFIds()
        for f_id in f_ids:
            if f_id in self.loading or f_id in self.loaded:
                continue
            self.download(tab.q_id, f_id)

    def _onOpenSelected(self):
        tab = self._ui.tabs.currentWidget()
        f_ids = tab.getSelectedFIds()
        for f_id in f_ids:
            if f_id not in self.loaded:
                continue
            self._onOpen(f_id)

    def _convertQuery(self, query):
        items = [item for response in query for item in response]
        return [[c[1](item) for c in columns] for item in items]

    def _addLoading(self, f_ids):
        self.loading.extend(f_ids)
        for tab in self.tabs.values():
            tab.setLoading(f_ids)

    def _addLoaded(self, dict):
        self.loading = [f_id for f_id in self.loading if f_id not in dict.keys()]
        self.loaded.update(dict)
        for tab in self.tabs.values():
            tab.setLoaded(dict.keys())

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setTitle("Download Results").setOrientation(QtCore.Qt.BottomDockWidgetArea)

    @property
    def view(self) -> QtWidgets:
        return self._view


class _QueryThread(QObject, Thread):
    query_finished = pyqtSignal(object)

    def __init__(self, *attrs):
        self.attrs = attrs
        Thread.__init__(self)
        QObject.__init__(self)

    def run(self):
        query = Fido.search(*self.attrs)
        self.query_finished.emit(query)


class _DownloadThread(QObject, Thread):
    download_finished = pyqtSignal(object)

    def __init__(self, request):
        self.request = request
        Thread.__init__(self)
        QObject.__init__(self)

    def run(self):
        paths = Fido.fetch(self.request)
        self.download_finished.emit(paths)


class ResultTab(QtWidgets.QWidget):
    download = pyqtSignal(str)
    open = pyqtSignal(str)

    def __init__(self, q_id):
        self.q_id = q_id

        QtWidgets.QWidget.__init__(self)

        self.ui = Ui_ResultTab()
        self.ui.setupUi(self)
        self.ui.table.hide()
        self._addHeader()

        self.rows = {}

    def loadQuery(self, model):
        self._addRows(model)
        self.ui.progress.hide()
        self.ui.table.show()

    def setLoading(self, f_ids):
        for f_id in f_ids:
            if f_id not in self.rows:
                continue
            index = self.rows[f_id]
            progress = QtWidgets.QProgressBar()
            progress.setRange(0, 0)
            progress.setStyleSheet(''' QProgressBar{max-height: 15px;text-align: center;}''')
            self.ui.table.setCellWidget(index, 0, progress)

    def setLoaded(self, f_ids):
        for f_id in f_ids:
            if f_id not in self.rows:
                continue
            index = self.rows[f_id]
            btn = QtWidgets.QToolButton()
            btn.setText("Open")
            btn.clicked.connect(lambda evt: self.open.emit(f_id))
            self.ui.table.setCellWidget(index, 0, btn)

    def getSelectedFIds(self):
        dict = {y: x for x, y in self.rows.items()}
        for i in set([i.row() for i in self.ui.table.selectedIndexes()]):
            yield dict[i]

    def _addHeader(self):
        header = self.ui.table.horizontalHeader()
        self.ui.table.setColumnCount(len(columns))
        for i, c in enumerate(columns):
            item = QTableWidgetItem(c[0])
            self.ui.table.setHorizontalHeaderItem(i, item)
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

    def _addRows(self, rows):
        self.ui.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.ui.table.setVerticalHeaderItem(i, QTableWidgetItem(str(i)))
            for j, cell in enumerate(row):
                if j == 0:
                    self.rows[cell] = i
                    btn = QtWidgets.QToolButton()
                    btn.setText("Download")
                    btn.clicked.connect(lambda evt, f_id=cell: self.download.emit(f_id))
                    self.ui.table.setCellWidget(i, j, btn)
                    continue
                self.ui.table.setItem(i, j, QTableWidgetItem(cell))
