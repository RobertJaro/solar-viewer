import numpy as np
import pywt
import wx
from skimage.restoration import estimate_sigma

from sunpyviewer.tools.default_tool import MapToolPanel, ToolController


class WaveletController(ToolController):

    def __init__(self):
        self.view = None

    def createView(self, parent, content_ctrl):
        self.view = WaveletPanel(parent, content_ctrl)
        return self.view

    def closeView(self, *args):
        self.view.Destroy()
        self.view = None


class WaveletPanel(MapToolPanel):
    def __init__(self, parent, content_ctrl):
        MapToolPanel.__init__(self, parent, content_ctrl)

    def initContent(self):
        return [self.initDecompositionSettings(), self.initDenoise()]

    def initDecompositionSettings(self):
        panel = wx.Panel(self)
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

    def initDenoise(self):
        panel = wx.Panel(self)
        box = wx.StaticBoxSizer(wx.VERTICAL, panel, "Denoise")
        panel.SetSizer(box)

        grid = wx.FlexGridSizer(2, 10, 15)
        box.Add(grid)

        sigma_text = wx.StaticText(panel, label="Sigma: ")
        self.sigma_spin = wx.SpinCtrlDouble(panel)
        grid.AddMany([sigma_text, self.sigma_spin])

        return panel

    def modifyMap(self, d_map):
        noiseSigma = self.sigma_spin.GetValue()
        data = d_map.data
        wavelet = self.wavelet_choice.GetStringSelection()
        level = self.level_spin.GetValue()

        WC = pywt.wavedec2(data=data, wavelet=wavelet, level=level)

        threshold = noiseSigma * np.sqrt(2 * np.log2(data.size))

        NWC = map(lambda x: pywt.threshold(x, threshold), WC)
        d_map._data = pywt.waverec2(list(NWC), wavelet=self.wavelet_choice.GetStringSelection())
        return d_map

    def refreshContent(self, data):
        estimated_sigma = estimate_sigma(data.data)
        self.sigma_spin.SetValue(str(estimated_sigma))
        self.selected_map = data
