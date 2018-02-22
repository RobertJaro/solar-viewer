import numpy as np
import wx
from astropy import units as u
from matplotlib.widgets import Cursor
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx.lib.pubsub import pub
from wx.lib.scrolledpanel import ScrolledPanel

from sunpyviewer.tools import EVT_SELECTION_EXPORT, EVT_SELECTION_CLEAR, EVT_SELECTION_IMPORT, \
    EVT_SELECTION_POINT_REMOVE, EVT_SELECTION_STYLE_CHANGE
from sunpyviewer.util.default_tool import ToolController, ItemConfig
from sunpyviewer.viewer import EVT_TAB_SELECTION_CHANGED
from sunpyviewer.viewer.content import DataType, ViewerType


class SelectionModel:

    def __init__(self):
        self.tab = None
        self.enabled = None
        self.points = []
        self.fig_points = []
        self.marker_colour = wx.Colour(255, 0, 0)
        self.text_colour = wx.Colour(0, 0, 255)

    def setTab(self, tab):
        self.tab = tab
        self.enabled = tab is not None

    def getCanvas(self):
        return self.tab.getFigure().canvas

    def getAxes(self):
        return self.tab.getAxes()

    def getMarkerColour(self):
        return (self.marker_colour.Red() / 255, self.marker_colour.Green() / 255, self.marker_colour.Blue() / 255)

    def getTextColour(self):
        return (self.text_colour.Red() / 255, self.text_colour.Green() / 255, self.text_colour.Blue() / 255)


class SelectionController(ToolController):

    def __init__(self):
        self.view = None
        self.model = None
        self.connection_id = None
        self.cursor = None

        pub.subscribe(self.onTabChange, EVT_TAB_SELECTION_CHANGED)
        pub.subscribe(self.onExport, EVT_SELECTION_EXPORT)
        pub.subscribe(self.onImport, EVT_SELECTION_IMPORT)
        pub.subscribe(self.onClear, EVT_SELECTION_CLEAR)
        pub.subscribe(self.onRemovePoint, EVT_SELECTION_POINT_REMOVE)
        pub.subscribe(self.onStyleChange, EVT_SELECTION_STYLE_CHANGE)

    @staticmethod
    def getItemConfig():
        return ItemConfig().setTitle("Highlight Values").setMenuPath("Tools\\Highlight Values").addSupportedData(
            DataType.MAP).addSupportedViewer(ViewerType.MPL)

    def createView(self, parent, ctrl):
        self.view = SelectionPanel(parent)
        self.model = SelectionModel()
        self.model.setTab(ctrl.getView() if ctrl is not None else None)
        self._initListener()
        self.onClear()
        return self.view

    def closeView(self):
        self._removeCursor()
        self.onClear()
        self.view = None

    def onFigureClick(self, event):
        if self.model.tab.toolbar._active is not None:
            return
        coord = self.model.tab.map.pixel_to_world(event.xdata * u.pixel, event.ydata * u.pixel)
        index = len(self.model.points)
        data = self.model.tab.map.data[int(np.rint(event.ydata)), int(np.rint(event.xdata))]
        self.model.points.append([event.xdata * u.pix, event.ydata * u.pix, coord.Tx,
                                  coord.Ty, data])
        self.view.addPointToList(coord.Tx, coord.Ty, data, index)
        self._drawPoint(event.xdata, event.ydata, index + 1)

    def onTabChange(self, ctrl):
        self._removeCursor()
        if not self.view:
            return
        self.onClear()
        self.model.setTab(ctrl.getView() if ctrl is not None else None)
        self._initListener()

    def onClear(self):
        self.model.points.clear()
        for point in self.model.fig_points:
            point.remove()
        self.model.fig_points = []
        self.view.clearPointsList()
        if self.model.enabled:
            self.model.getCanvas().draw()

    def onExport(self, path):
        data = [["{}".format(xp), "{}".format(yp), "{}".format(x), "{}".format(y), "{}".format(d)]
                for xp, yp, x, y, d in self.model.points]
        np.savetxt(path, data, delimiter=";", header="x_pixel;y_pixel;x;y;resources", fmt="%s")

    def onImport(self, path):
        self.onClear()
        data = np.loadtxt(path, dtype="str", delimiter=";").reshape(-1, 5)
        self.model.points = [
            [self._parseUnitString(xp), self._parseUnitString(yp), self._parseUnitString(x), self._parseUnitString(y),
             float(d)] for xp, yp, x, y, d in data]
        self._drawPoints()

    def onRemovePoint(self, id):
        del self.model.points[id]
        self._redrawPoints()

    def onStyleChange(self, marker_colour, text_colour):
        self.model.marker_colour = marker_colour
        self.model.text_colour = text_colour
        self._redrawPoints()

    def _initListener(self):
        self._removeCursor()
        if not self.model.enabled:
            return
        ax = self.model.tab.getAxes()
        self.connection_id = self.model.tab.getFigure().canvas.mpl_connect('button_press_event', self.onFigureClick)
        self.cursor = Cursor(ax, useblit=True, horizOn=True, vertOn=True)

    def _drawPoint(self, x, y, i, refresh=True):
        self.model.fig_points.append(self.model.getAxes().scatter(x, y, color=self.model.getMarkerColour()))
        self.model.fig_points.append(self.model.getAxes().annotate(i, (x, y), color=self.model.getTextColour()))
        if refresh:
            self.model.getCanvas().draw()

    def _drawPoints(self):
        for i, p in enumerate(self.model.points):
            self._drawPoint(p[0].value, p[1].value, i + 1, False)
            self.view.addPointToList(p[2], p[3], p[4], i)
        self.model.getCanvas().draw()

    def _redrawPoints(self):
        for point in self.model.fig_points:
            point.remove()
        self.model.fig_points = []
        self.view.clearPointsList()
        self._drawPoints()

    def _parseUnitString(self, s):
        v, unit = s.split(" ")
        return float(v) * u.Unit(unit)

    def _removeCursor(self):
        if self.connection_id:
            self.model.getCanvas().mpl_disconnect(self.connection_id)
            self.connection_id = None
        if self.cursor:
            del self.cursor
            self.cursor = None


class SelectionPanel(ScrolledPanel):
    def __init__(self, parent):
        ScrolledPanel.__init__(self, parent)
        self.SetAutoLayout(True)
        self.SetupScrolling()

        points_panel = self._initPointsPanel()
        style_panel = self._initStylePanel()
        button_panel = self._initButtons()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(points_panel, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(button_panel, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(style_panel, flag=wx.EXPAND | wx.ALL, border=10)
        self.SetSizerAndFit(sizer)

    def _initPointsPanel(self):
        values_panel = wx.Panel(self)

        box_sizer = wx.StaticBoxSizer(wx.VERTICAL, values_panel, "Selected Values")
        list = _PointsListCtrl(values_panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        list.SetMinSize((320, 400))
        list.InsertColumn(0, "ID")
        list.InsertColumn(1, "X")
        list.InsertColumn(2, "Y")
        list.InsertColumn(3, "Value")
        list.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onListRightClick)
        self.list = list

        clear_button = wx.Button(values_panel, wx.ID_CLEAR, "Clear")
        clear_button.Bind(wx.EVT_BUTTON, self.onClear)

        box_sizer.Add(list, flag=wx.EXPAND)
        box_sizer.Add(clear_button, flag=wx.EXPAND | wx.ALL, border=5)
        values_panel.SetSizerAndFit(box_sizer)

        return values_panel

    def _initStylePanel(self):
        style_panel = wx.Panel(self)

        box_sizer = wx.StaticBoxSizer(wx.VERTICAL, style_panel, "Style")
        grid_sizer = wx.GridSizer(2)

        marker_colour_label = wx.StaticText(style_panel, label="Marker Colour")
        marker_colour = wx.ColourPickerCtrl(style_panel, colour=wx.Colour(255, 0, 0))
        text_colour_label = wx.StaticText(style_panel, label="Text Colour")
        text_colour = wx.ColourPickerCtrl(style_panel, colour=wx.Colour(0, 0, 255))

        grid_sizer.AddMany([marker_colour_label, marker_colour, text_colour_label, text_colour])
        box_sizer.Add(grid_sizer, flag=wx.EXPAND)
        style_panel.SetSizerAndFit(box_sizer)

        ev = lambda x: pub.sendMessage(EVT_SELECTION_STYLE_CHANGE, marker_colour=marker_colour.GetColour(),
                                       text_colour=text_colour.GetColour())
        marker_colour.Bind(wx.EVT_COLOURPICKER_CHANGED, ev)
        text_colour.Bind(wx.EVT_COLOURPICKER_CHANGED, ev)

        return style_panel

    def _initButtons(self):
        panel = wx.Panel(self)
        export_button = wx.Button(panel, wx.ID_SAVE, "Export")
        export_button.Bind(wx.EVT_BUTTON, self.onExport)
        import_button = wx.Button(panel, wx.ID_OPEN, "Import")
        import_button.Bind(wx.EVT_BUTTON, self.onImport)
        button_sizer = wx.StdDialogButtonSizer()
        button_sizer.AddButton(export_button)
        button_sizer.AddButton(import_button)
        button_sizer.Realize()
        panel.SetSizerAndFit(button_sizer)
        return panel

    def addPointToList(self, x, y, data, index):
        self.list.InsertItem(index, "{}".format(index + 1))
        self.list.SetItem(index, 1, "{}".format(x))
        self.list.SetItem(index, 2, "{}".format(y))
        self.list.SetItem(index, 3, "{}".format(data))

    def clearPointsList(self):
        self.list.DeleteAllItems()

    def onClear(self, *args):
        pub.sendMessage(EVT_SELECTION_CLEAR)

    def onExport(self, *args):
        dialog = wx.FileDialog(self.GetParent(), "Save Data Points",
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_CANCEL:
            return
        path = dialog.GetPath()
        pub.sendMessage(EVT_SELECTION_EXPORT, path=path)

    def onImport(self, *args):
        dialog = wx.FileDialog(self.GetParent(), "Open Data Points", style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_CANCEL:
            return
        self.clearPointsList()
        path = dialog.GetPath()
        pub.sendMessage(EVT_SELECTION_IMPORT, path=path)

    def onListRightClick(self, event):
        menu = wx.Menu()
        item = menu.Append(wx.ID_ANY, "Remove")
        menu.Bind(wx.EVT_MENU, lambda x: pub.sendMessage(EVT_SELECTION_POINT_REMOVE, id=int(event.GetText()) - 1), item)
        self.PopupMenu(menu, event.GetPoint())
        menu.Destroy()


class _PointsListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent, **args):
        wx.ListCtrl.__init__(self, parent, **args)
        ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(3)
