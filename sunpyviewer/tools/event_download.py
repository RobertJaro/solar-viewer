import sys
import threading

import wx
import wx.adv
import wx.lib.masked.numctrl
import wx.lib.mixins.listctrl as listmix
from sunpy.net import Fido
from sunpy.net.hek import hek
from sunpy.net.hek2vso import hek2vso
from wx.lib.pubsub import pub
from wx.lib.scrolledpanel import ScrolledPanel

from sunpyviewer.tools import QueryType, EVT_QUERY_RESULT, EVT_QUERY_ERROR, EVT_QUERY_STARTED
from sunpyviewer.tools.download import TimeRangeComponent


class HEKListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(9)


class HEKPanel(ScrolledPanel):
    def __init__(self, parent):
        self.client = hek.HEKClient()
        self.vso_query_id = 0

        ScrolledPanel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        query_box = wx.StaticBox(self, label="Filter")
        query_sizer = wx.StaticBoxSizer(query_box, wx.VERTICAL)

        self.filter_panel = _FilterPanel(self)
        query_sizer.Add(self.filter_panel, flag=wx.EXPAND)
        query_sizer.AddSpacer(5)

        self.search_button = wx.Button(self, label="Search")
        query_sizer.Add(self.search_button, flag=wx.ALL, border=5)

        result_box = wx.StaticBox(self, label="Result")
        result_sizer = wx.StaticBoxSizer(result_box, wx.VERTICAL)

        self.query_button = wx.Button(self, label="Query")

        self.list = HEKListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.list.InsertColumn(0, "No.")
        self.list.InsertColumn(1, "Type")
        self.list.InsertColumn(2, "Start Time")
        self.list.InsertColumn(3, "End Time")
        self.list.InsertColumn(4, "Location")
        self.list.InsertColumn(5, "Observatory")
        self.list.InsertColumn(6, "Instrument")
        self.list.InsertColumn(7, "Channel")
        self.list.InsertColumn(8, "FRM")
        result_sizer.Add(self.list, flag=wx.EXPAND | wx.ALL, border=5)
        result_sizer.Add(self.query_button, flag=wx.BOTTOM | wx.LEFT, border=5)

        sizer.Add(query_sizer, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.AddSpacer(10)
        sizer.Add(result_sizer, flag=wx.EXPAND | wx.ALL, border=5)

        self.Fit()

        self.search_button.Bind(wx.EVT_BUTTON, self._onSearch)
        self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._onCallVSO)
        self.query_button.Bind(wx.EVT_BUTTON, self._onCallVSO)

    def _onSearch(self, event):
        self.search_button.Enable(False)
        self.search_button.SetLabel("Loading...")

        self.list.DeleteAllItems()
        attrs = self.filter_panel.GetValue()

        self.query = self.client.search(*attrs)
        for index, item in enumerate(self.query):
            location = self.createLocation(item)
            self.list.Append(
                [index + 1, item["event_type"], item["event_starttime"], item["event_endtime"], location,
                 item["obs_observatory"], item["obs_instrument"], item["obs_channelid"], item["frm_name"]])
        self.list.resizeColumn(-1)

        self.search_button.Enable(True)
        self.search_button.SetLabel("Search")

    def createLocation(self, item):
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

    def _onCallVSO(self, event):
        selected_index = self.list.GetFirstSelected()
        if selected_index == -1:
            return

        self.vso_query_id += 1
        pub.sendMessage(EVT_QUERY_STARTED, id=self.vso_query_id, type=QueryType.HEK)
        vso_query = hek2vso.translate_results_to_query(self.query[selected_index])
        threading.Thread(target=self.executeVSOQuery, args=(self.vso_query_id, vso_query)).start()

    def executeVSOQuery(self, id, vso_query):
        try:
            fido_result = Fido.search(*vso_query[0])
            pub.sendMessage(EVT_QUERY_RESULT, id=id, query=fido_result)
        except:
            pub.sendMessage(EVT_QUERY_ERROR, id=id, message=str(sys.exc_info()[1]))


class _FilterPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        filter_sizer = wx.FlexGridSizer(2, 10, 10)
        self.SetSizer(filter_sizer)

        time_text = wx.StaticText(self, label="Time Range: ")
        self.time_component = TimeRangeComponent(self)
        filter_sizer.AddMany([time_text, self.time_component])

        event_text = wx.StaticText(self, label="Event Type: ")
        self.event_input = wx.TextCtrl(self)
        filter_sizer.AddMany([event_text, self.event_input])

    def GetValue(self):
        start, end = self.time_component.GetTime()
        event = self.event_input.GetValue()
        return [hek.attrs.Time(start=start, end=end), hek.attrs.EventType(event)]
