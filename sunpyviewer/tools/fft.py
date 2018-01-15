import numpy as np
import wx

from sunpyviewer.conversion.filter import butter2d_lp, butter2d_hp, butter2d_bp
from sunpyviewer.tools.default_tool import MapToolPanel, ToolController


class FFTController(ToolController):

    def __init__(self):
        self.view = None

    def createView(self, parent, content_ctrl):
        self.view = FFTPanel(parent, content_ctrl)
        return self.view

    def closeView(self, *args):
        self.view.Destroy()
        self.view = None


class FFTPanel(MapToolPanel):
    def __init__(self, parent, content_ctrl):
        MapToolPanel.__init__(self, parent, content_ctrl)

    def initContent(self):
        filter_panel = wx.Panel(self)

        box_sizer = wx.StaticBoxSizer(wx.VERTICAL, filter_panel, "Filter")
        grid_sizer = wx.FlexGridSizer(2, 10, 15)

        self.h_check = wx.CheckBox(filter_panel, label="Highpass")
        self.h_spiner = wx.SpinCtrlDouble(filter_panel, value="0.2", max=10000)
        self.l_check = wx.CheckBox(filter_panel, label="Lowpass")
        self.l_spiner = wx.SpinCtrlDouble(filter_panel, value="100", max=10000)
        contrast_text = wx.StaticText(filter_panel)
        contrast_text.SetLabel("Adjust Contrast")
        self.contrast_check = wx.CheckBox(filter_panel, style=wx.ALIGN_LEFT)
        self.contrast_check.SetValue(True)

        grid_sizer.Add(self.h_check, flag=wx.ALIGN_CENTER)
        grid_sizer.Add(self.h_spiner, flag=wx.EXPAND | wx.ALIGN_CENTER)
        grid_sizer.Add(self.l_check, flag=wx.ALIGN_CENTER)
        grid_sizer.Add(self.l_spiner, flag=wx.EXPAND | wx.ALIGN_CENTER)
        grid_sizer.Add(contrast_text)
        grid_sizer.Add(self.contrast_check)

        box_sizer.Add(grid_sizer, flag=wx.ALL | wx.EXPAND, border=2)
        filter_panel.SetSizerAndFit(box_sizer)

        return [filter_panel]

    def modifyMap(self, data_map):
        adjust_contrast = self.contrast_check.IsChecked()
        h_val = self.h_spiner.GetValue()
        l_val = self.l_spiner.GetValue()
        shape = data_map.data.shape
        highpass = self.h_check.IsChecked()
        lowpass = self.l_check.IsChecked()

        filt = self.createFilter(h_val, highpass, l_val, lowpass, shape)
        return self._filterMap(filt, data_map, adjust_contrast)

    def refreshContent(self, data):
        pass

    def _filterMap(self, filt, map, adjust_contrast):
        if filt is not None:
            filtered_fft = np.fft.fftshift(np.fft.fft2(map.data)) * filt
            map._data = np.abs(np.fft.ifft2(np.fft.ifftshift(filtered_fft)))

        if adjust_contrast:
            map.plot_settings["norm"].vmin = map.min()
            map.plot_settings["norm"].vmax = map.mean() + 3 * map.std()

        return map

    def createFilter(self, h_val, highpass, l_val, lowpass, shape):
        filt = None
        if highpass and lowpass:
            filt = butter2d_bp(shape, l_val, h_val)
        else:
            if highpass:
                filt = butter2d_hp(shape, h_val)
            if lowpass:
                filt = butter2d_lp(shape, l_val)
        return filt
