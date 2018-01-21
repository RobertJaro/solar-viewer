import time

import wx

from sunpyviewer.tools.default_tool import MapToolPanel, ToolController
from sunpyviewer.util.wxmatplot import PlotPanel


class ContrastController(ToolController):
    def __init__(self):
        self.view = None

    def createView(self, parent, content_ctrl):
        self.view = ContrastPanel(parent, content_ctrl)
        return self.view

    def closeView(self, *args):
        self.view = None


class ContrastHist(PlotPanel):
    def __init__(self, parent, map):
        self.map = map
        self.ax = None
        PlotPanel.__init__(self, parent)

    def draw(self):
        min_value = min(self.map.data.flatten())
        max_value = max(self.map.data.flatten())

        self.ax = self.figure.add_subplot(1, 1, 1)
        self.ax.hist(self.map.data.ravel(), bins=300, range=(min_value, max_value), fc='k', ec='k')

    def plotLine(self, x):
        while self.ax is None:
            time.sleep(0.1)
        line = self.ax.axvline(x)
        self.canvas.draw()
        return line


class ContrastPanel(MapToolPanel):
    def __init__(self, parent, content_ctrl):
        self.min_line = None
        self.max_line = None
        MapToolPanel.__init__(self, parent, content_ctrl)
        self.hist_panel.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self._onCollapse)

    def initContent(self):
        return [self._initHistPane(), self._initSettingsBox()]

    def refreshContent(self, map):
        self.map = map
        self._drawHist()
        self._applyValues()

    def modifyMap(self, map):
        map.plot_settings["norm"].vmin = self.min_spin.GetValue()
        map.plot_settings["norm"].vmax = self.max_spin.GetValue()
        return map

    def _initHistPane(self):
        self.hist_panel = wx.CollapsiblePane(self, label="Histogram")
        pane = self.hist_panel.GetPane()
        pane_sizer = wx.BoxSizer(wx.VERTICAL)
        pane.SetSizerAndFit(pane_sizer)
        pane_sizer.SetSizeHints(pane)
        self.hist_panel.Enable(False)
        return self.hist_panel

    def _initSettingsBox(self):
        panel = wx.Panel(self)

        box_sizer = wx.StaticBoxSizer(wx.VERTICAL, panel, "Settings")
        grid_sizer = wx.FlexGridSizer(2, 10, 15)

        min_label = wx.StaticText(panel, label="Min:")
        self.min_spin = wx.SpinCtrlDouble(panel, name="min")
        max_label = wx.StaticText(panel, label="Max:")
        self.max_spin = wx.SpinCtrlDouble(panel, name="max")

        min_max_button = wx.Button(panel, label="Adjust Min/Max")
        avg_button = wx.Button(panel, label="Adjust Average")

        grid_sizer.AddMany([min_label, self.min_spin, max_label, self.max_spin])
        grid_sizer.AddStretchSpacer()
        grid_sizer.Add(min_max_button)
        grid_sizer.AddStretchSpacer()
        grid_sizer.Add(avg_button)

        box_sizer.Add(grid_sizer, flag=wx.ALL | wx.EXPAND, border=2)
        panel.SetSizerAndFit(box_sizer)

        self.min_spin.Bind(wx.EVT_SPINCTRLDOUBLE, self._drawMinLine)
        self.max_spin.Bind(wx.EVT_SPINCTRLDOUBLE, self._drawMaxLine)
        min_max_button.Bind(wx.EVT_BUTTON, self._onAdjustMinMax)
        avg_button.Bind(wx.EVT_BUTTON, self._onAdjustAvg)

        return panel

    def _applyValues(self):
        if not self.map:
            self.min_spin.SetMin(0)
            self.min_spin.SetMax(0)
            self.max_spin.SetMin(0)
            self.max_spin.SetMax(0)
            self.min_spin.SetValue(0)
            self.max_spin.SetValue(0)
            return
        min = self.map.data.min()
        max = self.map.data.max()
        self.min_spin.SetMin(min)
        self.min_spin.SetMax(max)
        self.max_spin.SetMin(min)
        self.max_spin.SetMax(max)

        v_min = self.map.plot_settings["norm"].vmin
        v_max = self.map.plot_settings["norm"].vmax
        self.min_spin.SetValue(v_min)
        self.max_spin.SetValue(v_max)

        self._drawLines()

    def _drawLines(self):
        self._drawMinLine()
        self._drawMaxLine()

    def _drawMaxLine(self, *args):
        if self.max_line is not None:
            wx.CallAfter(self.max_line.remove)
        self.max_line = self.contrast_hist.plotLine(x=self.max_spin.GetValue())

    def _drawMinLine(self, *args):
        if self.min_line is not None:
            wx.CallAfter(self.min_line.remove)
        self.min_line = self.contrast_hist.plotLine(x=self.min_spin.GetValue())

    def _onAdjustMinMax(self, event):
        self.map.plot_settings["norm"].vmin = self.map.min()
        self.map.plot_settings["norm"].vmax = self.map.max()
        self._applyValues()

    def _onAdjustAvg(self, event):
        self.map.plot_settings["norm"].vmin = self.map.min()
        self.map.plot_settings["norm"].vmax = self.map.mean() + 3 * self.map.std()
        self._applyValues()

    def _drawHist(self):
        pane = self.hist_panel.GetPane()
        for children in pane.Children:
            children.Destroy()

        self.hist_panel.Collapse(True)
        if not self.map:
            self.hist_panel.Enable(False)
            return

        self.hist_panel.Enable(True)
        self.contrast_hist = ContrastHist(pane, self.map)
        self.contrast_hist.SetMinSize((250, 250))
        sizer = pane.GetSizer()
        sizer.Add(self.contrast_hist, 1, wx.GROW | wx.ALL, 2)
