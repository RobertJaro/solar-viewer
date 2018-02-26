import time

import wx

from sunpyviewer.util.default_tool import ToolController, ItemConfig, DataControllerMixin
from sunpyviewer.util.wxmatplot import PlotPanel
from sunpyviewer.viewer.content import DataType, ViewerType


class ContrastModel:
    def __init__(self):
        self.min = None
        self.max = None
        self.min_line = None
        self.max_line = None

    def setMin(self, min):
        self.min = min

    def setMax(self, max):
        self.max = max


class ContrastController(DataControllerMixin, ToolController):
    def __init__(self):
        self.model = ContrastModel()

        DataControllerMixin.__init__(self)

    @staticmethod
    def getItemConfig():
        return ItemConfig().setTitle("Contrast Adjustment").setMenuPath("Tools\\Contrast").addSupportedData(
            DataType.MAP).addSupportedData(DataType.PLAIN_2D).addSupportedViewer(ViewerType.MPL)

    def modifyData(self, data, data_type):
        data.plot_settings["norm"].vmin = self.model.min
        data.plot_settings["norm"].vmax = self.model.max
        return data

    def getContentView(self, parent):
        content = [self._initHistPane(parent), self._initSettingsBox(parent)]
        return content

    def refreshContent(self, data, data_type):
        self.model.min = data.plot_settings["norm"].vmin
        self.model.max = data.plot_settings["norm"].vmax
        self._drawHist()
        self._applyValues()

    def _initHistPane(self, parent):
        self.hist_panel = wx.CollapsiblePane(parent, label="Histogram")
        pane = self.hist_panel.GetPane()
        pane_sizer = wx.BoxSizer(wx.VERTICAL)
        pane.SetSizerAndFit(pane_sizer)
        pane_sizer.SetSizeHints(pane)
        self.hist_panel.Enable(False)
        self.hist_panel.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self._onCollapse)
        return self.hist_panel

    def _initSettingsBox(self, parent):
        panel = wx.Panel(parent)

        box_sizer = wx.StaticBoxSizer(wx.VERTICAL, panel, "Settings")
        grid_sizer = wx.FlexGridSizer(2, 10, 15)

        min_label = wx.StaticText(panel, label="Min:")
        self.min_spin = wx.SpinCtrlDouble(panel, name="min", inc=0.01)
        max_label = wx.StaticText(panel, label="Max:")
        self.max_spin = wx.SpinCtrlDouble(panel, name="max", inc=0.01)

        min_max_button = wx.Button(panel, label="Adjust Min/Max")
        avg_button = wx.Button(panel, label="Adjust Average")

        grid_sizer.AddMany([min_label, self.min_spin, max_label, self.max_spin])
        grid_sizer.AddStretchSpacer()
        grid_sizer.Add(min_max_button)
        grid_sizer.AddStretchSpacer()
        grid_sizer.Add(avg_button)

        box_sizer.Add(grid_sizer, flag=wx.ALL | wx.EXPAND, border=2)
        panel.SetSizerAndFit(box_sizer)

        self.min_spin.Bind(wx.EVT_SPINCTRLDOUBLE, self._onMin)
        self.max_spin.Bind(wx.EVT_SPINCTRLDOUBLE, self._onMax)
        min_max_button.Bind(wx.EVT_BUTTON, self._onAdjustMinMax)
        avg_button.Bind(wx.EVT_BUTTON, self._onAdjustAvg)

        return panel

    def _onMin(self, *args):
        self.model.setMin(self.min_spin.GetValue())
        self._drawMinLine()

    def _onMax(self, *args):
        self.model.setMax(self.max_spin.GetValue())
        self._drawMaxLine()

    def _applyValues(self):
        sun_map = self.viewer_ctrl.getContent()
        min = sun_map.data.min()
        max = sun_map.data.max()
        self.min_spin.SetMin(min)
        self.min_spin.SetMax(max)
        self.max_spin.SetMin(min)
        self.max_spin.SetMax(max)

        v_min = self.model.min
        v_max = self.model.max
        self.min_spin.SetValue(v_min)
        self.max_spin.SetValue(v_max)

        self._drawLines()

    def _drawLines(self):
        self._drawMinLine()
        self._drawMaxLine()

    def _drawMaxLine(self, *args):
        if self.model.max_line is not None:
            wx.CallAfter(self.model.max_line.remove)
        self.model.max_line = self.contrast_hist.plotLine(x=self.model.max)

    def _drawMinLine(self, *args):
        if self.model.min_line is not None:
            wx.CallAfter(self.model.min_line.remove)
        self.model.min_line = self.contrast_hist.plotLine(x=self.model.min)

    def _onAdjustMinMax(self, event):
        data = self.viewer_ctrl.getContent().data
        self.model.min = data.min()
        self.model.max = data.max()
        self._applyValues()

    def _onAdjustAvg(self, event):
        data = self.viewer_ctrl.getContent().data
        self.model.min = data.min()
        self.model.max = data.mean() + 3 * data.std()
        self._applyValues()

    def _drawHist(self):
        pane = self.hist_panel.GetPane()
        for children in pane.Children:
            children.Destroy()

        self.hist_panel.Collapse(True)
        self.hist_panel.Enable(True)
        self.contrast_hist = ContrastHist(pane, self.viewer_ctrl.getContent())
        self.contrast_hist.SetMinSize((250, 250))
        sizer = pane.GetSizer()
        sizer.Add(self.contrast_hist, 1, wx.GROW | wx.ALL, 2)

    def _onCollapse(self, *args):
        self.view.Layout()
        self.view.FitInside()


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
        wx.CallAfter(self.canvas.draw)
        return line
