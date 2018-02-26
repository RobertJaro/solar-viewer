import numpy as np
import wx

from sunpyviewer.conversion.filter import butter2d_lp, butter2d_hp, butter2d_bp
from sunpyviewer.util.default_tool import ToolController, ItemConfig, DataControllerMixin
from sunpyviewer.viewer.content import DataType, ViewerType


class FFTController(DataControllerMixin, ToolController):

    def __init__(self):
        self.view = None

    @staticmethod
    def getItemConfig():
        return ItemConfig().setTitle("FFT").setMenuPath("Tools\\FFT").addSupportedData(DataType.MAP).addSupportedViewer(
            ViewerType.ANY)

    def modifyData(self, data, data_type):
        adjust_contrast = self.contrast_check.IsChecked()
        h_val = self.h_spiner.GetValue()
        l_val = self.l_spiner.GetValue()
        shape = data.data.shape
        highpass = self.h_check.IsChecked()
        lowpass = self.l_check.IsChecked()

        filt = self.createFilter(h_val, highpass, l_val, lowpass, shape)
        return self._filterMap(filt, data, adjust_contrast)

    def getContentView(self, parent):
        filter_panel = wx.Panel(parent)

        box_sizer = wx.StaticBoxSizer(wx.VERTICAL, filter_panel, "Filter")
        grid_sizer = wx.FlexGridSizer(2, 10, 15)

        self.h_check = wx.CheckBox(filter_panel, label="Highpass")
        self.h_spiner = wx.SpinCtrlDouble(filter_panel, value="0.2", max=10000, inc=0.01)
        self.l_check = wx.CheckBox(filter_panel, label="Lowpass")
        self.l_spiner = wx.SpinCtrlDouble(filter_panel, value="100", max=10000, inc=0.01)
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

    def refreshContent(self, data, data_type):
        pass

    def _filterMap(self, filt, map, adjust_contrast):
        if filt is not None:
            filtered_fft = np.fft.fftshift(np.fft.fft2(map.data)) * filt
            map._data = np.abs(np.fft.ifft2(np.fft.ifftshift(filtered_fft)))

        if adjust_contrast:
            map.plot_settings["norm"].vmin = map.data.min()
            map.plot_settings["norm"].vmax = map.data.mean() + 3 * map.data.std()

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
