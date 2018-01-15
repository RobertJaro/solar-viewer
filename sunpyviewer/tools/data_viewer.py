import wx
from sunpy.database import Database
from wx import dataview
from wx.lib.pubsub import pub

from sunpyviewer.tools import EVT_OPEN_MAP


class DataViewer(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        data_viewer = self.initDataViewer()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(data_viewer, 1, flag=wx.EXPAND | wx.ALL, border=10)
        self.SetSizerAndFit(sizer)
        self.Layout()

    def initDataViewer(self):
        viewer = dataview.DataViewCtrl(self,
                                       style=wx.BORDER_THEME | dataview.DV_ROW_LINES | dataview.DV_VERT_RULES | dataview.DV_MULTIPLE)

        self.model = InstrumentModel(list(Database()))
        viewer.AssociateModel(self.model)

        viewer.AppendTextColumn("File ID", 0)
        viewer.AppendDateColumn("Start Date", 1)
        viewer.AppendDateColumn("End Date", 2)
        viewer.AppendTextColumn("Wave", 3)

        viewer.Bind(dataview.EVT_DATAVIEW_ITEM_ACTIVATED, self.onItemActivated)

        return viewer

    def onItemActivated(self, event):
        for selection in event.EventObject.Selections:
            node = self.model.ItemToObject(selection)
            if isinstance(node, Entry):
                path = node.path
                pub.sendMessage(EVT_OPEN_MAP, path=path)


class InstrumentModel(dataview.PyDataViewModel):
    columns = {0: ("ID", "string", "title"), 1: ("Start Date", "datetime", "start"), 2: ("End Date", "datetime", "end"),
               3: ("Wavelength", "string", "wave")}

    def __init__(self, entries):
        self.instruments = self.createInstruments(entries)
        self.addEntries(entries)

        dataview.PyDataViewModel.__init__(self)

        self.UseWeakRefs(True)

    def addEntries(self, entries):
        for k in self.instruments:
            v = [Entry(entry, k) for entry in entries if entry.instrument == k.title]
            k.entries.extend(v)

    def createInstruments(self, entries):
        titles = list(set([entry.instrument for entry in entries]))
        return [Instrument(title) for title in titles]

    def IsContainer(self, item):
        if not item:
            return True

        node = self.ItemToObject(item)
        if isinstance(node, Instrument):
            return True

        return False

    def GetParent(self, item):
        node = self.ItemToObject(item)

        if isinstance(node, Entry):
            return self.ObjectToItem(node.parent)
        return dataview.NullDataViewItem

    def GetChildren(self, item, children):
        if not item:
            for instrument in self.instruments:
                children.append(self.ObjectToItem(instrument))
            return len(self.instruments)

        node = self.ItemToObject(item)

        if isinstance(node, Instrument):
            for entry in node.entries:
                children.append(self.ObjectToItem(entry))
            return len(node.entries)

        return 0

    def GetColumnCount(self):
        return len(self.columns)

    def GetColumnType(self, col):
        return self.columns[col][1]

    def GetValue(self, item, col):
        node = self.ItemToObject(item)

        if isinstance(node, Instrument):
            return node.title

        if isinstance(node, Entry):
            return getattr(node, self.columns[col][2], "")


class Entry(object):
    def __init__(self, db_entry, parent):
        self.title = db_entry.fileid
        self.start = db_entry.observation_time_start
        self.end = db_entry.observation_time_end
        self.wave = "{} - {}".format(db_entry.wavemin, db_entry.wavemax)
        self.path = db_entry.path
        self.parent = parent


class Instrument(object):
    def __init__(self, title):
        self.title = title
        self.entries = []
