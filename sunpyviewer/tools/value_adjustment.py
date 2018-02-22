import numpy as np
import wx

from sunpyviewer.util.default_tool import ToolController, ItemConfig, DataControllerMixin
from sunpyviewer.viewer.content import DataType, ViewerType


class ValueAdjustmentController(DataControllerMixin, ToolController):

    def __init__(self):
        self.view = None

    @staticmethod
    def getItemConfig():
        return ItemConfig().setTitle("Value Adjustment").setMenuPath("Tools\\Value Adjustment").addSupportedData(
            DataType.MAP).addSupportedViewer(ViewerType.MPL)

    def modifyData(self, data, data_type):
        d = data.data
        if self.cutoff_radio.GetValue():
            data._data = d.clip(0)
        if self.offset_radio.GetValue():
            min_value = d.min()
            if min_value < 0:
                data._data = d - min_value + 1
        if self.cutoff_range_radio.GetValue():
            vmin = self.min_range.GetValue()
            vmax = self.max_range.GetValue()
            data._data = np.clip(d, vmin, vmax)

        if self.contrast_none.GetValue():
            return
        if self.contrast_min_max.GetValue():
            data.plot_settings["norm"].vmin = data.min()
            data.plot_settings["norm"].vmax = data.max()
        if self.contrast_average.GetValue():
            data.plot_settings["norm"].vmin = data.min()
            data.plot_settings["norm"].vmax = data.mean() + 3 * data.std()

        return data

    def getContentView(self, parent):
        panel = wx.Panel(parent)

        settings_box = wx.StaticBoxSizer(wx.VERTICAL, panel, "Settings")
        grid_sizer = wx.FlexGridSizer(1, 10, 10)
        settings_box.Add(grid_sizer, flag=wx.ALL | wx.EXPAND, border=2)

        self.cutoff_radio = wx.RadioButton(panel, 1, label="Clip Negative Values")
        self.cutoff_radio.SetValue(True)
        self.offset_radio = wx.RadioButton(panel, 2, label="Apply Offset")
        self.cutoff_range_radio = wx.RadioButton(panel, 3, label="Clip To Range")

        range_box = wx.StaticBoxSizer(wx.VERTICAL, panel, "Range")
        range_sizer = wx.FlexGridSizer(3, 10, 10)
        range_box.Add(range_sizer, flag=wx.ALL | wx.EXPAND, border=2)

        self.min_range = wx.SpinCtrlDouble(panel, inc=0.01)
        self.min_range.Enable(False)
        range_label = wx.StaticText(panel, label=" - ")
        self.max_range = wx.SpinCtrlDouble(panel, inc=0.01)
        self.max_range.Enable(False)
        range_sizer.AddMany([self.min_range, range_label, self.max_range])

        contrast_box = wx.StaticBoxSizer(wx.VERTICAL, panel, "Contrast Adjustment")
        contrast_sizer = wx.FlexGridSizer(1, 10, 10)
        contrast_box.Add(contrast_sizer, flag=wx.ALL | wx.EXPAND, border=2)

        self.contrast_none = wx.RadioButton(panel, 1, label="None", style=wx.RB_GROUP)
        self.contrast_min_max = wx.RadioButton(panel, 2, label="Min/Max")
        self.contrast_average = wx.RadioButton(panel, 3, label="Average")

        grid_sizer.AddMany([self.cutoff_radio, self.offset_radio, self.cutoff_range_radio])
        grid_sizer.AddStretchSpacer()
        grid_sizer.Add(range_box)
        contrast_sizer.AddMany([self.contrast_none, self.contrast_min_max, self.contrast_average])
        grid_sizer.Add(contrast_box)

        panel.SetSizerAndFit(settings_box)

        self.cutoff_range_radio.Bind(wx.EVT_RADIOBUTTON, self._onShowRange)
        self.cutoff_radio.Bind(wx.EVT_RADIOBUTTON, self._onHideRange)
        self.offset_radio.Bind(wx.EVT_RADIOBUTTON, self._onHideRange)

        return [panel]

    def refreshContent(self, data, data_type):
        if data is None:
            self.min_range.SetRange(0, 0)
            self.min_range.SetValue(str(0))
            self.max_range.SetRange(0, 0)
            self.max_range.SetValue(str(0))
            return
        norm = data.plot_settings["norm"]
        vmin = data.data.min()
        vmax = data.data.max()
        norm_vmin = norm.vmin if norm.vmin != None and norm.vmin >= vmin else vmin
        norm_vmax = norm.vmax if norm.vmax != None and norm.vmax <= vmax else vmax
        self.min_range.SetRange(vmin, vmax)
        self.min_range.SetValue(str(norm_vmin))
        self.max_range.SetRange(vmin, vmax)
        self.max_range.SetValue(str(norm_vmax))

    def _onShowRange(self, event):
        self.min_range.Enable(True)
        self.max_range.Enable(True)

    def _onHideRange(self, event):
        self.min_range.Enable(False)
        self.max_range.Enable(False)
