from enum import Enum

from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QFrame
from astropy import units as u
from qtpy import QtWidgets, QtCore
from sunpy.net import attr, attrs

from solarviewer.config.base import ToolController, ItemConfig
from solarviewer.config.ioc import RequiredFeature
from solarviewer.resource.vso import vso_keys
from solarviewer.tool.download_result import DownloadResultController
from solarviewer.ui.download import Ui_Download
from solarviewer.ui.time_range import Ui_TimeRange
from solarviewer.ui.wave_range import Ui_WaveRange
from solarviewer.ui.wave_select import Ui_WaveSelect


class DownloadController(ToolController):
    result_ctrl: DownloadResultController = RequiredFeature(DownloadResultController.name)

    def __init__(self):
        self.query_id = 0

        ToolController.__init__(self)
        self._view = QtWidgets.QWidget()
        self._ui = Ui_Download()
        self._ui.setupUi(self._view)
        self._ui.content.resizeEvent = lambda evt: self._ui.scrollArea.setMinimumWidth(
            self._ui.content.sizeHint().width() + self._ui.scrollArea.verticalScrollBar().sizeHint().width())
        self._ui.content_layout.setAlignment(QtCore.Qt.AlignTop)
        self._ui.message_box.hide()

        self.possible_filters = [e.value for e in Filter]
        self.refreshActiveFilters()
        self.active_filters = []
        self.addMandatoryFilters()

        self._ui.add_filter_button.clicked.connect(self.onAddFilter)
        self._ui.query_button.clicked.connect(self.onQuery)

    def refreshActiveFilters(self):
        self._ui.filter_combo.clear()
        self._ui.filter_combo.addItems([f["label"] for f in self.possible_filters])

    def addMandatoryFilters(self):
        mandatory_filters = [e for e in self.possible_filters if e["mandatory"]]
        for f in mandatory_filters:
            self.addFilter(f)

    def addFilter(self, f):
        filter_box = _FilterBox(f)
        filter_box.closeEvent = lambda evt, fi=filter_box: self.onFilterDestroyed(fi)
        self._ui.content_layout.addWidget(filter_box)
        self.possible_filters.remove(f)
        self.active_filters.append(f)
        self.refreshActiveFilters()

    def onAddFilter(self, event):
        selection = self._ui.filter_combo.currentText()
        selected_filter = [f for f in self.possible_filters if f["label"] == selection]
        if len(selected_filter) == 1:
            self.addFilter(selected_filter[0])

    def onQuery(self, *args):
        self._ui.message_box.hide()
        try:
            attrs = []
            filters = [f for f in self._ui.content.children() if isinstance(f, _FilterBox)]
            for f in filters:
                attrs.append(f.value())
            self.result_ctrl.query(attrs)
        except Exception as ex:
            self._ui.message_label.setText("Invalid Query: " + str(ex))
            self._ui.message_box.show()

    def onFilterDestroyed(self, filter_panel):
        filter = filter_panel.filter
        self.possible_filters.append(filter)
        self.active_filters.remove(filter)
        self.refreshActiveFilters()

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setTitle("Download Tool").setMenuPath("File/Download Data")

    @property
    def view(self) -> QtWidgets:
        return self._view


class _FilterBox(QtWidgets.QFrame):
    def __init__(self, filter):
        self.lines = []
        self.filter = filter
        self.label = filter["label"]
        self.mandatory = filter["mandatory"]
        self.component = filter["comp"]

        QtWidgets.QFrame.__init__(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFrameShape(QtWidgets.QFrame.Box)

        self.layout = QtWidgets.QGridLayout(self)

        self.addLine(self.label + " : ", True)
        self.showLines()

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(separator)
        self.resize(414, 85)

    def addLine(self, label="Or : ", toggle_value=False):
        toggle_label = "+"
        if toggle_value:
            toggle_label = "-"

        label = QtWidgets.QLabel(label)

        comp = self.component()
        comp.hide()

        toggle_button = QtWidgets.QToolButton()
        toggle_button.setText(toggle_label)
        toggle_button.setCheckable(True)
        toggle_button.setChecked(toggle_value)

        row = len(self.lines)
        self.layout.addWidget(toggle_button, row, 0, 1, 1)
        self.layout.addWidget(label, row, 1, 1, 1)
        self.layout.addWidget(comp, row, 2, 1, 1)
        toggle_button.clicked.connect(lambda evt, b=toggle_button: self.onToggle(b))
        self.lines.append({"toggle": toggle_button, "label": label, "comp": comp})

    def onToggle(self, button):
        if button.isChecked():
            button.setText("-")
        self.showLines()

    def showLines(self):
        remove_lines = []
        for line in self.lines:
            if not line["toggle"].isChecked():
                if line is self.lines[-1]:
                    line["comp"].hide()
                else:
                    remove_lines.append(line)
            else:
                line["comp"].show()

        for line in remove_lines:
            if self.lines.index(line) == 0:
                self.lines[1]["label"].setText(line["label"].text())
            self.lines.remove(line)
            self.layout.removeWidget(line["toggle"])
            self.layout.removeWidget(line["label"])
            self.layout.removeWidget(line["comp"])
            line["toggle"].close()
            line["label"].close()
            line["comp"].close()

        if self.lines[-1]["toggle"].isChecked():
            self.addLine()

        if self.mandatory:
            if self.only_one_selected():
                self.lines[0]["toggle"].setEnabled(False)
            else:
                self.lines[0]["toggle"].setEnabled(True)

        if not any([line["toggle"].isChecked() for line in self.lines]):
            self.close()

    def only_one_selected(self):
        return len([True for line in self.lines if line["toggle"].isChecked()]) == 1

    def value(self):
        values = []
        for line in self.lines:
            comp = line["comp"]
            if comp.isVisible():
                values.append(comp.value())
        return attr.or_(*values)


class TimeRangeComponent(QtWidgets.QWidget):
    def __init__(self, *args):
        QtWidgets.QWidget.__init__(self, *args)
        self.ui = Ui_TimeRange()
        self.ui.setupUi(self)
        now = QDateTime.currentDateTimeUtc()
        self.ui.from_time.setDateTime(now.addSecs(-2 * 60 * 60))
        self.ui.to_time.setDateTime(now.addSecs(-1.50 * 60 * 60))

    def value(self):
        start = self.ui.from_time.dateTime().toString(QtCore.Qt.ISODate)
        end = self.ui.to_time.dateTime().toString(QtCore.Qt.ISODate)
        return attrs.Time(start=start, end=end)


class _InstrumentComponent(QtWidgets.QComboBox):
    def __init__(self):
        choices = sorted([entry[0] for entry in vso_keys.loadEntries()["INSTRUMENT"]], key=lambda s: s.lower())
        QtWidgets.QComboBox.__init__(self)
        self.addItems(choices)
        self.setEditable(True)

    def value(self):
        return attrs.Instrument(self.currentText())


class _ProviderComponent(QtWidgets.QComboBox):
    def __init__(self):
        choices = sorted([entry[0] for entry in vso_keys.loadEntries()["PROVIDER"]], key=lambda s: s.lower())
        QtWidgets.QComboBox.__init__(self)
        self.addItems(choices)
        self.setEditable(True)

    def value(self):
        return attrs.vso.Provider(self.currentText())


class _SourceComponent(QtWidgets.QComboBox):
    def __init__(self):
        choices = sorted([entry[0] for entry in vso_keys.loadEntries()["SOURCE"]], key=lambda s: s.lower())
        QtWidgets.QComboBox.__init__(self)
        self.addItems(choices)
        self.setEditable(True)

    def value(self):
        return attrs.vso.Source(self.currentText())


class _PhysObsComponent(QtWidgets.QComboBox):
    def __init__(self):
        choices = sorted([entry[0] for entry in vso_keys.loadEntries()["PHYSOBS"]], key=lambda s: s.lower())
        QtWidgets.QComboBox.__init__(self)
        self.addItems(choices)
        self.setEditable(True)

    def value(self):
        return attrs.vso.Physobs(self.currentText())


class _WaveRangeComponent(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_WaveRange()
        self.ui.setupUi(self)

    def value(self):
        return attrs.vso.Wavelength(wavemin=self.ui.from_spin.value() * u.AA,
                                    wavemax=self.ui.to_spin.value() * u.AA)


class _WaveComponent(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_WaveSelect()
        choices = [str(u.AA), str(u.kHz), str(u.GHz), str(u.keV)]
        self.ui.unit_combo.addItems(choices)

    def value(self):
        unit = u.Unit(self.ui.unit_combo.currentText())
        return attrs.Wavelength(wavemin=self.ui.wave_spin.value() * unit)


class Filter(Enum):
    TIME = {"label": "Time Range", "comp": TimeRangeComponent, "mandatory": True}
    INSTRUMENT = {"label": "Instrument", "comp": _InstrumentComponent, "mandatory": False}
    PROVIDER = {"label": "Provider", "comp": _ProviderComponent, "mandatory": False}
    SOURCE = {"label": "Source", "comp": _SourceComponent, "mandatory": False}
    PHYS_OBS = {"label": "Physical Observable", "comp": _PhysObsComponent, "mandatory": False}
    WAVERANGE = {"label": "Wavelength Range [angstrom]", "comp": _WaveRangeComponent, "mandatory": False}
    WAVE = {"label": "Wavelength", "comp": _WaveComponent, "mandatory": False}
