from enum import Enum

import astropy.units as u
import numpy as np
import wx
from matplotlib.widgets import Cursor
from wx.lib.pubsub import pub
from wx.lib.scrolledpanel import ScrolledPanel

from sunpyviewer.conversion.coordinate import extractCoordinates
from sunpyviewer.tools import EVT_PROFILE_MODE_CHANGE, EVT_PROFILE_RESET
from sunpyviewer.util.default_tool import ToolController, ItemConfig
from sunpyviewer.util.wxmatplot import PlotPanel
from sunpyviewer.viewer import EVT_TAB_SELECTION_CHANGED, EVT_MPL_CHANGE_MODE
from sunpyviewer.viewer.content import ViewerType, DataType
from sunpyviewer.viewer.toolbar import ViewMode


class ProfileModel:
    def __init__(self):
        self.tab = None
        self.enabled = None
        self.setTab(None)
        self.mode = Mode.NONE
        self.points = []
        self.line = None

    def setTab(self, tab):
        self.tab = tab
        self.enabled = tab is not None

    def getCanvas(self):
        return self.tab.getFigure().canvas


class ProfileController(ToolController):

    def __init__(self):
        self.view = None
        self.model = ProfileModel()
        self.cursor = None
        self.connection_id = None

        pub.subscribe(self.onTabChange, EVT_TAB_SELECTION_CHANGED)
        pub.subscribe(self.onModeChange, EVT_PROFILE_MODE_CHANGE)
        pub.subscribe(self.resetFreeLine, EVT_PROFILE_RESET)

    @staticmethod
    def getItemConfig():
        return ItemConfig().setTitle("Profile").setMenuPath("Tools\\Profile").addSupportedData(
            DataType.MAP).addSupportedViewer(ViewerType.MPL)

    def createView(self, parent, ctrl):
        self.view = ProfilePanel(parent)
        self.onTabChange(ctrl)
        return self.view

    def closeView(self):
        self.removeLine(False)
        self._removeCursor()
        self.view = None
        self.model = ProfileModel()

    def _removeCursor(self):
        if self.cursor:
            del self.cursor
            self.cursor = None
        if self.connection_id:
            self.model.getCanvas().mpl_disconnect(self.connection_id)
            self.connection_id = None

    def onModeChange(self, mode):
        self.cursor.horizOn = mode is Mode.HORIZONTAL
        self.cursor.vertOn = mode is Mode.VERTICAL
        self.model.mode = mode
        self.resetFreeLine()
        pub.sendMessage(EVT_MPL_CHANGE_MODE, mode=ViewMode.NONE)

    def onTabChange(self, ctrl):
        if not self.view:
            return
        self._removeCursor()
        self.resetFreeLine()
        if ctrl and ctrl.viewer_type is ViewerType.MPL and ctrl.data_type is DataType.MAP:
            self.model.setTab(ctrl.getView())
        else:
            self.model.setTab(None)
            self.model.mode = Mode.NONE
        self.view.initMode(self.model.enabled)
        if self.model.enabled:
            self._initFigureListener(self.model.tab)
            self.onModeChange(self.model.mode)

    def _initFigureListener(self, tab):
        ax = tab.getAxes()
        self.connection_id = tab.getFigure().canvas.mpl_connect('button_press_event', self.onFigureClick)
        self.cursor = Cursor(ax, useblit=True, horizOn=False, vertOn=False)

    def onFigureClick(self, event):
        if self.model.tab.toolbar._active is not None:
            return
        mode = self.model.mode
        if mode is Mode.NONE:
            return
        self.view.clearViewPanel()
        coordinates = extractCoordinates(self.model.tab.map, event)
        if mode is Mode.FREE_LINE:
            self.model.points.append([coordinates[0], coordinates[1]])
            self.drawFreeLine()
            if len(self.model.points) <= 1:
                return
            profile_view = FreeLineProfilePanel(self.view.view_panel, self.model.tab.map, self.model.points)
        if mode is Mode.VERTICAL:
            profile_view = VerticalProfilePanel(self.view.view_panel, self.model.tab.map, coordinates)
        if mode is Mode.HORIZONTAL:
            profile_view = HorizontalProfilePanel(self.view.view_panel, self.model.tab.map, coordinates)
        self.view.addProfilePanel(profile_view)

    def removeLine(self, refresh=True):
        if self.model.line is None:
            return
        self.model.line.remove()
        self.model.line = None
        if refresh:
            self.model.getCanvas().draw()

    def resetFreeLine(self):
        self.model.points = []
        self.removeLine()
        self.view.clearViewPanel()

    def drawFreeLine(self):
        x_ax, y_ax = np.transpose(self.model.points)
        self.removeLine(False)
        self.model.line = self.model.tab.getAxes().plot(x_ax, y_ax, "-o", color="r")[0]
        self.model.tab.getFigure().canvas.draw()


class Mode(Enum):
    NONE = "None"
    VERTICAL = "Vertical"
    HORIZONTAL = "Horizontal"
    FREE_LINE = "Free Line"


# only valid for non-rotated
class VerticalProfilePanel(PlotPanel):
    def __init__(self, parent, map, coordinates):
        self.map = map
        self.coordinates = coordinates
        PlotPanel.__init__(self, parent)

    def draw(self):
        x, y, x_data, y_data = self.coordinates
        data = self.map.data
        self.createVerticalProfile(data, x, y, x_data, y_data)

    def createVerticalProfile(self, data, x, y, x_data, y_data):
        vertical_data = np.transpose(data)[x]
        yrange_min = self.map.yrange.min().to(u.arcsec).value
        yrange_max = self.map.yrange.max().to(u.arcsec).value
        y_scale = self.map.scale[1].to(u.arcsec / u.pix).value
        x_axis = np.arange(yrange_min, yrange_max, y_scale)
        ax = self.figure.add_subplot(111)
        ax.plot(x_axis, vertical_data, zorder=1)
        ax.scatter([y_data], [vertical_data[y]], color="red", zorder=2)  # mark selected pixel
        ax.xaxis.set_label_text("Y-position [arcsec]")
        ax.set_title("Longitude: %f arcsec" % x_data)


# only valid for non-rotated
class HorizontalProfilePanel(PlotPanel):
    def __init__(self, parent, map, coordinates):
        self.map = map
        self.coordinates = coordinates
        PlotPanel.__init__(self, parent)

    def draw(self):
        x, y, x_data, y_data = self.coordinates
        data = self.map.data
        self.createHorizontalProfile(data, x, y, x_data, y_data)

    def createHorizontalProfile(self, data, x, y, x_data, y_data):
        horizontal_data = data[y]
        xrange_min = self.map.xrange.min().to(u.arcsec).value
        xrange_max = self.map.xrange.max().to(u.arcsec).value
        x_scale = self.map.scale[0].to(u.arcsec / u.pix).value
        x_axis = np.arange(xrange_min, xrange_max, x_scale)
        ax = self.figure.add_subplot(111)
        ax.plot(x_axis, horizontal_data, zorder=1)
        ax.scatter([x_data], [horizontal_data[x]], color="red", zorder=2)  # mark selected pixel
        ax.xaxis.set_label_text("X-position [arcsec]")
        ax.set_title("Latitude: %f arcsec" % y_data)


class FreeLineProfilePanel(PlotPanel):
    def __init__(self, parent, map, points):
        self.values = []
        x0 = None
        y0 = None
        for x1, y1 in points:
            if x0 is not None and y0 is not None:
                length = int(np.hypot(x1 - x0, y1 - y0))
                x, y = np.linspace(x0, x1, length), np.linspace(y0, y1, length)
                # Extract the values along the line
                self.values = np.append(self.values, map.data[y.astype(np.int), x.astype(np.int)])
            x0 = x1
            y0 = y1
        PlotPanel.__init__(self, parent)

    def draw(self):
        if len(self.values) <= 1:
            return
        ax = self.figure.add_subplot(111)
        ax.plot(self.values)
        ax.get_xaxis().set_ticks([])


class ProfilePanel(ScrolledPanel):
    def __init__(self, parent):
        self.profile_view = None

        ScrolledPanel.__init__(self, parent)
        self.SetAutoLayout(True)
        self.SetupScrolling()

        self.view_panel = self._initViewPanel()
        mode_panel = self._initModePanel()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.view_panel, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(mode_panel, flag=wx.EXPAND | wx.ALL, border=10)
        self.SetSizerAndFit(sizer)

    def initMode(self, enabled):
        self.h_radio.Enable(enabled)
        self.v_radio.Enable(enabled)
        self.fl_radio.Enable(enabled)

        if not enabled:
            self.none_radio.SetValue(True)

        self.clearViewPanel()

    def _initViewPanel(self):
        view_panel = wx.Panel(self)

        box_sizer = wx.StaticBoxSizer(wx.VERTICAL, view_panel, "Profile")
        box_sizer.SetMinSize((300, 300))

        view_panel.SetSizerAndFit(box_sizer)
        return view_panel

    def _initModePanel(self):
        mode_panel = wx.Panel(self)

        box_sizer = wx.StaticBoxSizer(wx.VERTICAL, mode_panel, "Mode")

        self.none_radio = wx.RadioButton(mode_panel, 1, label="None", pos=(10, 0))
        self.none_radio.SetValue(True)
        self.h_radio = wx.RadioButton(mode_panel, 2, label="Horizontal", pos=(10, 30))
        self.v_radio = wx.RadioButton(mode_panel, 3, label="Vertical", pos=(10, 60))
        self.fl_radio = wx.RadioButton(mode_panel, 4, label="Free Line", pos=(10, 90))
        fl_button = wx.Button(mode_panel, 5, label="Reset Line", pos=(10, 120))

        box_sizer.AddMany([self.none_radio, self.h_radio, self.v_radio, self.fl_radio, fl_button])
        mode_panel.SetSizerAndFit(box_sizer)

        self.Bind(wx.EVT_RADIOBUTTON, self.onRadioClick)
        fl_button.Bind(wx.EVT_BUTTON, self.onResetLine)

        return mode_panel

    def clearViewPanel(self):
        if self.profile_view is None:
            return
        self.view_panel.GetSizer().Remove(0)
        self.profile_view.Destroy()
        self.profile_view = None

    def onRadioClick(self, *args):
        pub.sendMessage(EVT_PROFILE_MODE_CHANGE, mode=self._getMode())

    def onResetLine(self, *args):
        pub.sendMessage(EVT_PROFILE_RESET)

    def _getMode(self):
        if self.v_radio.GetValue():
            return Mode.VERTICAL
        if self.h_radio.GetValue():
            return Mode.HORIZONTAL
        if self.fl_radio.GetValue():
            return Mode.FREE_LINE
        return Mode.NONE

    def addProfilePanel(self, profile_view):
        self.profile_view = profile_view
        self.view_panel.GetSizer().Add(profile_view, 1, flag=wx.EXPAND | wx.ALL, border=10)
        self.Layout()
