import numpy as np
import pywt
import wx
from skimage.restoration import estimate_sigma

from sunpyviewer.util.default_tool import ToolController, ItemConfig, DataControllerMixin
from sunpyviewer.viewer.content import ViewerType, DataType


class WaveletController(DataControllerMixin, ToolController):

    def __init__(self):
        self.view = None

    @staticmethod
    def getItemConfig():
        return ItemConfig().setTitle("Wavelet Filter").setMenuPath("Tools\\Wavelet Filter").addSupportedData(
            DataType.MAP).addSupportedViewer(ViewerType.ANY)

    def modifyData(self, data, data_type):
        noiseSigma = self.sigma_spin.GetValue()
        d = data.data
        wavelet = self.wavelet_choice.GetStringSelection()
        level = self.level_spin.GetValue()

        WC = pywt.wavedec2(data=d, wavelet=wavelet, level=level)

        threshold = noiseSigma * np.sqrt(2 * np.log2(d.size))

        NWC = map(lambda x: pywt.threshold(x, threshold), WC)
        data._data = pywt.waverec2(list(NWC), wavelet=self.wavelet_choice.GetStringSelection())
        return data

    def getContentView(self, parent):
        return [self._initDecompositionSettings(parent), self._initDenoise(parent)]

    def refreshContent(self, data, data_type):
        estimated_sigma = estimate_sigma(data.data)
        self.sigma_spin.SetValue(str(estimated_sigma))
        self.selected_map = data

    def _initDecompositionSettings(self, parent):
        panel = wx.Panel(parent)
        box_sizer = wx.StaticBoxSizer(wx.VERTICAL, panel, "Wavelet Settings")
        grid_sizer = wx.FlexGridSizer(2, 10, 15)

        family_text = wx.StaticText(panel, style=wx.ALIGN_CENTER, label="Wavelet Family")
        self.family_choices = wx.Choice(panel, choices=pywt.families(False))
        self.family_choices.SetSelection(0)
        self.family_choices.Bind(wx.EVT_CHOICE, lambda e: self.wavelet_choice.SetItems(
            pywt.wavelist(pywt.families()[self.family_choices.GetSelection()])))

        wavelet_text = wx.StaticText(panel, -1, style=wx.ALIGN_CENTER, label="Wavelet")
        self.wavelet_choice = wx.Choice(panel,
                                        choices=pywt.wavelist(pywt.families()[self.family_choices.GetSelection()]))

        level_text = wx.StaticText(panel, -1, style=wx.ALIGN_CENTER, label="Level")
        self.level_spin = wx.SpinCtrl(panel, min=1, max=12, value="1")

        box_sizer.Add(grid_sizer)
        grid_sizer.AddMany(
            [family_text, self.family_choices, wavelet_text, self.wavelet_choice, level_text, self.level_spin])
        panel.SetSizer(box_sizer)

        return panel

    def _initDenoise(self, parent):
        panel = wx.Panel(parent)
        box = wx.StaticBoxSizer(wx.VERTICAL, panel, "Denoise")
        panel.SetSizer(box)

        grid = wx.FlexGridSizer(2, 10, 15)
        box.Add(grid)

        sigma_text = wx.StaticText(panel, label="Sigma: ")
        self.sigma_spin = wx.SpinCtrlDouble(panel, inc=0.0001)
        grid.AddMany([sigma_text, self.sigma_spin])

        return panel
