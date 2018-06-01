import datetime

import sunpy
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget, QMenu, QStyle
from qtpy import QtWidgets, QtSql, QtCore
from sunpy.database import Database

from solarviewer.app.content import ContentController
from solarviewer.config.base import ToolController, ItemConfig
from solarviewer.config.ioc import RequiredFeature
from solarviewer.ui.data_manager import Ui_DataManager
from solarviewer.ui.data_manager_filter import Ui_DataManagerFilter
from solarviewer.viewer.map import MapViewerController


class DataManagerController(ToolController):
    content_ctrl: ContentController = RequiredFeature(ContentController.name)

    def __init__(self):
        self._view = QtWidgets.QWidget()
        self._ui = Ui_DataManager()
        self._ui.setupUi(self._view)

        self._ui.refresh_button.setIcon(self._view.style().standardIcon(QStyle.SP_BrowserReload))
        self._ui.remove_button.setIcon(self._view.style().standardIcon(QStyle.SP_DialogNoButton))
        self._ui.add_button.setIcon(self._view.style().standardIcon(QStyle.SP_DialogYesButton))

        self.dlg = DataManagerFilterDialog()

        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(sunpy.config.get("database", "url").replace("sqlite:///", ""))

        model = QtSql.QSqlTableModel()
        model.setTable("data")
        model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        model.select()
        self._ui.data_table.setModel(model)

        self.initTableHeader(model)

        self._ui.add_button.clicked.connect(lambda x: self.onAdd())
        self._ui.remove_button.clicked.connect(lambda x: self.onRemove())
        self._ui.open_button.clicked.connect(lambda x: self.onOpen())
        self._ui.refresh_button.clicked.connect(lambda x: self.model.select())
        self._ui.filter_button.clicked.connect(lambda x: self.onFilter())

        self.sunpy_db = Database()
        self.model = model

    def initTableHeader(self, model):
        header = self._ui.data_table.horizontalHeader()
        for i in range(model.columnCount()):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        header.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        header.customContextMenuRequested.connect(self.onHeaderMenu)
        self._ui.data_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._ui.data_table.customContextMenuRequested.connect(self.onHeaderMenu)

        self._ui.data_table.hideColumn(0)
        self._ui.data_table.hideColumn(2)
        self._ui.data_table.hideColumn(3)
        self._ui.data_table.hideColumn(4)
        self._ui.data_table.hideColumn(8)
        self._ui.data_table.hideColumn(11)
        self._ui.data_table.hideColumn(12)
        self._ui.data_table.hideColumn(13)
        self._ui.data_table.hideColumn(14)

    def onAdd(self):
        paths, _ = QtWidgets.QFileDialog.getOpenFileNames(None, filter="FITS files (*.fits; *.fit; *.fts)")
        for p in paths:
            self.sunpy_db.add_from_file(p)
            self.sunpy_db.commit()
        self.model.select()

    def onRemove(self):
        rows = set([i.row() for i in self._ui.data_table.selectedIndexes()])
        for r in rows:
            self.model.removeRow(r)
        self.model.submitAll()
        self.model.select()

    def onOpen(self):
        rows = set([i.row() for i in self._ui.data_table.selectedIndexes()])
        paths = [self.model.index(row, self.model.fieldIndex("path")).data() for row in rows]
        for path in paths:
            viewer_ctrl = MapViewerController.fromFile(path)
            self.content_ctrl.addViewerController(viewer_ctrl)

    def onFilter(self):
        if self.dlg.exec_():
            self.model.setFilter(self.dlg.getFilter())
            self.model.select()

    def onHeaderMenu(self, point):
        menu = QMenu(self._view)

        actions = []
        for column in range(self.model.columnCount()):
            label = self.model.headerData(column, QtCore.Qt.Horizontal)
            action = QtWidgets.QAction(label)
            action.setCheckable(True)
            action.setChecked(not self._ui.data_table.isColumnHidden(column))
            event = lambda checked, c=column: self._ui.data_table.showColumn(
                c) if checked else self._ui.data_table.hideColumn(c)
            action.triggered.connect(event)
            actions.append(action)
        menu.addActions(actions)

        menu.exec_(QCursor.pos())

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setMenuPath("File/Data Manager").setTitle("Data Manager")

    @property
    def view(self) -> QWidget:
        self.model.select()
        return self._view


class DataManagerFilterDialog(QtWidgets.QDialog):

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_DataManagerFilter()
        self.ui.setupUi(self)

        now = datetime.datetime.utcnow()
        self.ui.from_time.setDateTime(now - datetime.timedelta(days=1))
        self.ui.to_time.setDateTime(now)

    def getFilter(self):
        filters = []
        if self.ui.instrument_check.isChecked():
            filters.append("{} LIKE '{}'".format("instrument", self.ui.instrument.text()))
        if self.ui.source_check.isChecked():
            filters.append("{} LIKE '{}'".format("source", self.ui.source.text()))
        if self.ui.provider_check.isChecked():
            filters.append("{} LIKE '{}'".format("provider", self.ui.provider.text()))
        if self.ui.physobs_check.isChecked():
            filters.append("{} LIKE '{}'".format("physobs", self.ui.physobs.text()))
        if self.ui.time_check.isChecked():
            query = "({0} BETWEEN '{2}' AND '{3}' OR {1} BETWEEN '{2}' AND '{3}')"
            filters.append(query.format("observation_time_start", "observation_time_end",
                                        self.ui.from_time.dateTime().toString(QtCore.Qt.ISODate).replace("T", " "),
                                        self.ui.to_time.dateTime().toString(QtCore.Qt.ISODate).replace("T", " ")))
        if self.ui.wave_check.isChecked():
            query = "({0} BETWEEN '{2}' AND '{3}' OR {1} BETWEEN '{2}' AND '{3}')"
            filters.append(query.format("wavemin", "wavemax",
                                        self.ui.from_wave.value(), self.ui.to_wave.value()))
        if self.ui.starred_check.isChecked():
            filters.append("{}={}".format("starred", 1 if self.ui.starred.isChecked() else 0))

        return " AND ".join(filters)
