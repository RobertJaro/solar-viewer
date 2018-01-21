import copy
import datetime
import sys
import threading
from enum import Enum

import astropy.units as u
import wx
import wx.adv
import wx.lib.masked.numctrl
import wx.lib.mixins.listctrl as listmix
from sunpy.database import Database, tables
from sunpy.net import Fido, attr
from sunpy.net import attrs
from sunpy.time import parse_time
from wx import aui
from wx.lib.pubsub import pub
from wx.lib.scrolledpanel import ScrolledPanel

from sunpyviewer.tools import EVT_FILTER_CLOSE, QueryType, EVT_QUERY_RESULT, \
    EVT_OPEN_MAP, EVT_QUERY_ERROR, EVT_QUERY_STARTED
from sunpyviewer.util import vso_keys


class QueryPanel(ScrolledPanel):
    query_id = 0

    def __init__(self, parent):
        ScrolledPanel.__init__(self, parent)
        self.SetAutoLayout(True)
        self.SetupScrolling(scroll_x=False)

        query_box = wx.StaticBox(self, label='Query')
        self.filter_panel = wx.Panel(self)

        self.filter_choice = wx.Choice(self.filter_panel, choices=["Time Range", "Instrument"], style=wx.CB_SORT)
        add_filter_button = wx.Button(self.filter_panel, label="Add Filter")

        query_button = wx.Button(self, label="Query")

        add_filter_sizer = wx.BoxSizer(wx.HORIZONTAL)
        add_filter_sizer.Add(self.filter_choice, flag=wx.ALIGN_CENTER)
        add_filter_sizer.AddSpacer(15)
        add_filter_sizer.Add(add_filter_button, flag=wx.ALIGN_CENTER)

        self.filter_sizer = wx.BoxSizer(wx.VERTICAL)
        self.filter_panel.SetSizer(self.filter_sizer)
        self.filter_sizer.Add(add_filter_sizer, flag=wx.EXPAND | wx.ALL, border=10)
        self.filter_sizer.Add(wx.StaticLine(self.filter_panel), flag=wx.EXPAND | wx.HORIZONTAL)

        self.possible_filters = [e.value for e in Filter]
        self.refreshActiveFilters()
        self.active_filters = []
        self.addMandatoryFilters()

        query_sizer = wx.StaticBoxSizer(query_box, orient=wx.VERTICAL)
        query_sizer.Add(self.filter_panel, border=5)
        query_sizer.Add(query_button, border=5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(query_sizer, flag=wx.EXPAND | wx.ALL, border=5)
        self.SetSizerAndFit(sizer)

        pub.subscribe(self.onFilterDestroyed, EVT_FILTER_CLOSE)
        add_filter_button.Bind(wx.EVT_BUTTON, self.onAddFilter)
        query_button.Bind(wx.EVT_BUTTON, self.onQuery)

    def refreshActiveFilters(self):
        self.filter_choice.SetItems([f["label"] for f in self.possible_filters])

    def addMandatoryFilters(self):
        mandatory_filters = [e for e in self.possible_filters if e["mandatory"]]
        for f in mandatory_filters:
            self.addFilter(f)

    def addFilter(self, f):
        filter_box = _FilterBox(self.filter_panel, f)
        self.filter_sizer.Add(filter_box, flag=wx.EXPAND | wx.ALL, border=10)
        self.possible_filters.remove(f)
        self.active_filters.append(f)
        self.refreshActiveFilters()
        self.adjustLayout()

    def onAddFilter(self, event):
        selection = self.filter_choice.GetStringSelection()
        selected_filter = [f for f in self.possible_filters if f["label"] == selection]
        if len(selected_filter) == 1:
            self.addFilter(selected_filter[0])

    def onFilterDestroyed(self, filter, filter_panel):
        self.possible_filters.append(filter)
        self.active_filters.remove(filter)
        self.refreshActiveFilters()
        filter_panel.Destroy()
        self.adjustLayout()

    def adjustLayout(self):
        self.Layout()
        self.FitInside()
        self.GetParent()

    def onQuery(self, event):
        attrs = []
        filters = [f for f in self.filter_panel.GetChildren() if isinstance(f, _FilterBox)]
        for f in filters:
            attrs.append(f.GetValue())

        self.query_id += 1
        pub.sendMessage(EVT_QUERY_STARTED, id=self.query_id, type=QueryType.FIDO)
        threading.Thread(target=self.executeQuery, args=(self.query_id, attrs)).start()

    def executeQuery(self, id, attrs):
        try:
            query = Fido.search(*attrs)
            pub.sendMessage(EVT_QUERY_RESULT, id=id, query=query)
        except:
            pub.sendMessage(EVT_QUERY_ERROR, id=id, message=str(sys.exc_info()[1]))


class QueryResultNotebook(aui.AuiNotebook):
    tabs = {}

    def __init__(self, parent):
        aui.AuiNotebook.__init__(self, parent)

    def addQueryPage(self, id, type):
        query_tab = QueryTab(self)
        self.tabs[id] = query_tab
        title = "Query " if type == QueryType.FIDO else "HEK "
        self.AddPage(query_tab, title + str(id), True)

    def addQueryResult(self, id, query):
        self.tabs[id].loadQueryResult(query)


class QueryTab(wx.Panel):
    query_columns = [
        [True, "Start Time", lambda item: parse_time(item.time.start) if hasattr(item.time, "start") else "None"],
        [True, "End Time", lambda item: parse_time(item.time.end) if hasattr(item.time, "end") else "None"],
        [True, "Instrument", lambda item: getattr(item, "instrument", "None")],
        [True, "Source", lambda item: getattr(item, "source", "None")],
        [False, "Provider", lambda item: getattr(item, "provider", "None")],
        [True, "Type", lambda item: getattr(getattr(item, "extent", None), "type", "None")],
        [True, "Wavelength", lambda item: "{} - {}".format(item.wave.wavemin, item.wave.wavemax)
        if hasattr(item, "wave") and hasattr(item.wave, "wavemin") and hasattr(item.wave, "wavemax") else "None"],
        [False, "Physical Observable", lambda item: getattr(item, "physobs", "None")]
    ]

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.database = Database()
        self.downloading_ids = []
        self.downloaded_ids = []
        self.download_paths = {}
        self.result = None

        self.list = FidoListCtrl(self, style=wx.LC_REPORT)
        self.image_list = wx.ImageList(24, 24)
        self.list.SetImageList(self.image_list, wx.IMAGE_LIST_SMALL)
        self.list.Hide()
        self._createListColumns()

        self.progress = wx.Gauge(self, style=wx.GA_HORIZONTAL)
        self.progress.Pulse()

        sizer = wx.BoxSizer(wx.VERTICAL)
        prog_sizer = wx.BoxSizer(wx.HORIZONTAL)

        prog_sizer.Add(self.progress, 1, wx.CENTER)
        sizer.Add(prog_sizer, 1, wx.CENTER)
        sizer.Add(self.list, 1, wx.EXPAND)

        self.SetSizerAndFit(sizer)
        self.list.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.onColumnRightClick)
        self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onItemActivated)

    def _createListColumns(self):
        l = self.list

        for i in range(l.GetColumnCount()):
            l.DeleteColumn(0)

        i = 0
        l.InsertColumn(i, "")
        for column in self.query_columns:
            if column[0]:
                i += 1
                l.InsertColumn(i, column[1])

        l.AdjustColumnWidth()

    def loadQueryResult(self, result):
        self.result = result
        wx.CallAfter(self._refreshList)

    def _refreshList(self):
        self.list.DeleteAllItems()
        self.image_list.RemoveAll()
        for response in self.result:
            for item in response:
                image_index = self.image_list.Add(wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, size=(24, 24)))
                column_values = [c[2](item) for c in self.query_columns if c[0]]
                column_values.insert(0, "")
                item_index = self.list.Append(column_values)
                self.list.SetItemImage(item_index, image_index, image_index)

        entries = tables.entries_from_fido_search_result(self.result)
        db_files = {entry.fileid: entry.path for entry in list(self.database)}
        for index, entry in enumerate(entries):
            if entry.fileid in db_files.keys():
                self.downloaded_ids.append(index)
                self.download_paths[index] = db_files[entry.fileid]

        for index in self.downloading_ids:
            self.image_list.Replace(index, wx.ArtProvider.GetBitmap(wx.ART_REDO))
        for index in self.downloaded_ids:
            self.image_list.Replace(index, wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, size=(24, 24)))
        self.list.Refresh()

        self.progress.Hide()
        self.list.Show()
        self.Layout()
        self.list.AdjustColumnWidth()

    def onColumnRightClick(self, event):
        menu = wx.Menu()
        for i, c in enumerate(self.query_columns):
            item = menu.AppendCheckItem(i, c[1])
            item.Check(c[0])
            menu.Bind(wx.EVT_MENU, self.onColumnChange, item)

        self.list.PopupMenu(menu, event.GetPoint())
        menu.Destroy()

    def onColumnChange(self, event):
        id = event.GetId()
        self.query_columns[id][0] = not self.query_columns[id][0]
        self._createListColumns()
        self._refreshList()

    def onItemActivated(self, event):
        index = event.Index

        if index in self.downloading_ids:
            return

        if index in self.download_paths.keys():
            pub.sendMessage(EVT_OPEN_MAP, path=self.download_paths[index])
            return

        self.downloading_ids.append(index)
        self.image_list.Replace(index, wx.ArtProvider.GetBitmap(wx.ART_REDO))
        self.list.Refresh()
        self.downloadData([index])

    def downloadData(self, selected):
        request = copy.copy(self.result)
        request._list = [copy.copy(list(self.result)[i]) for i in range(len(self.result))]
        index = -1
        for q_index, q in enumerate(self.result):
            for item in list(q):
                index += 1
                if index in selected:
                    continue
                request._list[q_index].remove(item)
        threading.Thread(target=self.executeDownload, args=(request, selected)).start()

    def executeDownload(self, request, selected):
        paths = Fido.fetch(request)
        entries = list(tables.entries_from_fido_search_result(request, self.database.default_waveunit))
        for i, entry in enumerate(entries):
            entry.path = paths[i]
        self.database.add_many(entries)
        self.database.commit()
        self.downloading_ids = [id for id in self.downloading_ids if id not in selected]
        self.downloaded_ids.extend(selected)
        for i, path in enumerate(paths):
            self.download_paths[selected[i]] = path
        for index in selected:
            self.image_list.Replace(index, wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, size=(24, 24)))
        self.list.Refresh()


class FidoListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

    def AdjustColumnWidth(self):
        for i in range(self.GetColumnCount()):
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE)
            content_width = self.GetColumnWidth(i)
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            header_width = self.GetColumnWidth(i)
            self.SetColumnWidth(i, max(content_width, header_width))


class _FilterBox(wx.Panel):
    def __init__(self, parent, filter):
        self.lines = []
        self.filter = filter
        self.label = filter["label"]
        self.mandatory = filter["mandatory"]
        self.component = filter["comp"]

        wx.Panel.__init__(self, parent)
        self.sizer = wx.FlexGridSizer(3, 5, 5)

        self.addLine(self.label + " : ", True)
        self.showLines()

        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vertical_sizer)
        vertical_sizer.Add(self.sizer, flag=wx.EXPAND, border=5)
        vertical_sizer.AddSpacer(15)
        vertical_sizer.Add(wx.StaticLine(self), flag=wx.EXPAND | wx.SL_HORIZONTAL, border=10)

    def addLine(self, label="Or : ", toggle_value=False):
        toggle_label = "+"
        if toggle_value:
            toggle_label = "-"
        toggle_button = wx.ToggleButton(self, label=toggle_label, style=wx.BU_EXACTFIT)
        toggle_button.SetValue(toggle_value)

        text = wx.StaticText(self)
        text.SetLabel(label=label)

        comp = self.component(self)
        comp.Hide()

        self.sizer.Add(toggle_button, flag=wx.ALIGN_CENTER)
        self.sizer.Add(text, flag=wx.ALIGN_CENTER)
        self.sizer.Add(comp, flag=wx.ALIGN_CENTER)
        toggle_button.Bind(wx.EVT_TOGGLEBUTTON, self.onToggle)
        self.lines.append({"toggle": toggle_button, "label": text, "comp": comp})

    def onToggle(self, event):
        button = event.GetEventObject()
        if button.GetValue():
            button.SetLabel("-")
        self.showLines()

    def showLines(self):
        remove_lines = []
        for line in self.lines:
            if not line["toggle"].GetValue():
                if line is self.lines[-1]:
                    line["comp"].Hide()
                else:
                    remove_lines.append(line)
            else:
                line["comp"].Show()

        for line in remove_lines:
            if self.lines.index(line) == 0:
                self.lines[1]["label"].SetLabel(line["label"].GetLabel())
            self.lines.remove(line)
            line["toggle"].Destroy()
            line["label"].Destroy()
            line["comp"].Destroy()

        if self.lines[-1]["toggle"].GetValue():
            self.addLine()

        if self.mandatory:
            if self.only_one_selected():
                self.lines[0]["toggle"].Enable(False)
            else:
                self.lines[0]["toggle"].Enable(True)

        if not any([line["toggle"].GetValue() for line in self.lines]):
            pub.sendMessage(EVT_FILTER_CLOSE, filter=self.filter, filter_panel=self)
        else:
            self.GetParent().GetParent().adjustLayout()

    def only_one_selected(self):
        return len([True for line in self.lines if line["toggle"].GetValue()]) == 1

    def GetValue(self):
        values = []
        for line in self.lines:
            comp = line["comp"]
            if comp.IsShown():
                values.append(comp.GetValue())
        return attr.or_(*values)


class TimeRangeComponent(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        now = wx.DateTime.ToUTC(wx.DateTime(datetime.datetime.now()))
        self.start_date_picker = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN)
        self.start_date_picker.SetValue(now)
        self.start_time_picker = wx.adv.TimePickerCtrl(self)
        self.start_time_picker.SetValue(now)
        time_to_text = wx.StaticText(self)
        time_to_text.SetLabel(" - ")
        self.end_date_picker = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN)
        self.end_date_picker.SetValue(now)
        self.end_time_picker = wx.adv.TimePickerCtrl(self)
        self.end_time_picker.SetValue(now)

        time_sizer = wx.BoxSizer(wx.HORIZONTAL)

        time_sizer.Add(self.start_date_picker, border=5)
        time_sizer.Add(self.start_time_picker, border=5)
        time_sizer.Add(time_to_text, border=5)
        time_sizer.Add(self.end_date_picker, border=5)
        time_sizer.Add(self.end_time_picker, border=5)

        self.SetSizer(time_sizer)

    def GetTime(self):
        start = self.start_date_picker.GetValue().FormatISODate() + "T" + self.start_time_picker.GetValue().FormatISOTime()
        end = self.end_date_picker.GetValue().FormatISODate() + "T" + self.end_time_picker.GetValue().FormatISOTime()
        return start, end

    def GetValue(self):
        start = self.start_date_picker.GetValue().FormatISODate() + "T" + self.start_time_picker.GetValue().FormatISOTime()
        end = self.end_date_picker.GetValue().FormatISODate() + "T" + self.end_time_picker.GetValue().FormatISOTime()
        return attrs.Time(start=start, end=end)


class _InstrumentComponent(wx.ComboBox):
    def __init__(self, parent):
        choices = sorted([entry[0] for entry in vso_keys.loadEntries()["INSTRUMENT"]], key=lambda s: s.lower())
        wx.ComboBox.__init__(self, parent, choices=choices)

    def GetValue(self):
        return attrs.Instrument(super(_InstrumentComponent, self).GetValue())


class _ProviderComponent(wx.ComboBox):
    def __init__(self, parent):
        choices = sorted([entry[0] for entry in vso_keys.loadEntries()["PROVIDER"]], key=lambda s: s.lower())
        wx.ComboBox.__init__(self, parent, choices=choices)

    def GetValue(self):
        return attrs.vso.Provider(super(_ProviderComponent, self).GetValue())


class _SourceComponent(wx.ComboBox):
    def __init__(self, parent):
        choices = sorted([entry[0] for entry in vso_keys.loadEntries()["SOURCE"]], key=lambda s: s.lower())
        wx.ComboBox.__init__(self, parent, choices=choices)

    def GetValue(self):
        return attrs.vso.Source(super(_SourceComponent, self).GetValue())


class _PhysObsComponent(wx.ComboBox):
    def __init__(self, parent):
        choices = sorted([entry[0] for entry in vso_keys.loadEntries()["PHYSOBS"]], key=lambda s: s.lower())
        wx.ComboBox.__init__(self, parent, choices=choices)

    def GetValue(self):
        return attrs.vso.Physobs(super(_PhysObsComponent, self).GetValue())


class _WaveRangeComponent(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.wavemin_picker = wx.SpinCtrlDouble(self, max=100000)
        wave_to_text = wx.StaticText(self)
        wave_to_text.SetLabel(" - ")
        self.wavemax_picker = wx.SpinCtrlDouble(self, max=100000)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddMany([self.wavemin_picker, wave_to_text, self.wavemax_picker])
        self.SetSizer(sizer)

    def GetValue(self):
        return attrs.vso.Wavelength(wavemin=self.wavemin_picker.GetValue() * u.AA,
                                    wavemax=self.wavemax_picker.GetValue() * u.AA)


class _WaveComponent(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.wave_picker = wx.SpinCtrlDouble(self, max=100000)
        choices = [str(u.AA), str(u.kHz), str(u.GHz), str(u.keV)]
        self.unit_picker = wx.Choice(self, choices=choices)
        self.unit_picker.SetSelection(0)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddMany([self.wave_picker, self.unit_picker])
        self.SetSizer(sizer)

    def GetValue(self):
        unit = u.Unit(self.unit_picker.GetStringSelection())
        return attrs.Wavelength(wavemin=self.wave_picker.GetValue() * unit)


class Filter(Enum):
    TIME = {"label": "Time Range", "comp": TimeRangeComponent, "mandatory": True}
    INSTRUMENT = {"label": "Instrument", "comp": _InstrumentComponent, "mandatory": False}
    PROVIDER = {"label": "Provider", "comp": _ProviderComponent, "mandatory": False}
    SOURCE = {"label": "Source", "comp": _SourceComponent, "mandatory": False}
    PHYS_OBS = {"label": "Physical Observable", "comp": _PhysObsComponent, "mandatory": False}
    WAVERANGE = {"label": "Wavelength Range [angstrom]", "comp": _WaveRangeComponent, "mandatory": False}
    WAVE = {"label": "Wavelength", "comp": _WaveComponent, "mandatory": False}
