import wx
from skimage.restoration import denoise_tv_chambolle, denoise_bilateral, denoise_wavelet, estimate_sigma
from wx.lib.pubsub import pub

from sunpyviewer.viewer import EVT_CHANGE_TAB
from sunpyviewer.viewer.settings import DefaultDialog


class TVDenoiseDialog(DefaultDialog):
    def __init__(self, parent, tab_id, map):
        self.tab_id = tab_id
        self.map = map
        DefaultDialog.__init__(self, parent, 'Denoise Total Variation Chambolle')

    def createContent(self, panel):
        content_sizer = wx.FlexGridSizer(2, 5, 5)

        weight_label = wx.StaticText(panel, label="Weight: ")
        self.weight_spin = wx.SpinCtrlDouble(panel, min=0, value="0.1", inc=0.01)

        content_sizer.AddMany([weight_label, self.weight_spin])

        return content_sizer

    def onOk(self, event):
        weight = self.weight_spin.GetValue()
        im = self.map.data
        bi = wx.BusyInfo("Denoising, please wait", parent=self.GetParent())
        self.map._data = denoise_tv_chambolle(im, weight=weight)
        self.map.plot_settings["norm"].vmin = self.map.data.min()
        self.map.plot_settings["norm"].vmax = self.map.data.max()
        del bi

        pub.sendMessage(EVT_CHANGE_TAB, tab_id=self.tab_id, data=self.map)
        event.Skip()


class BilateralDenoiseDialog(DefaultDialog):
    def __init__(self, parent, tab_id, map):
        self.tab_id = tab_id
        self.map = map
        DefaultDialog.__init__(self, parent, 'Denoise Bilateral')

    def createContent(self, panel):
        content_sizer = wx.FlexGridSizer(2, 5, 5)

        color_label = wx.StaticText(panel, label="Sigma Color: ")
        self.color_spin = wx.SpinCtrlDouble(panel, min=0, value="0.05", inc=0.01)
        spatial_label = wx.StaticText(panel, label="Spatial Color: ")
        self.spatial_spin = wx.SpinCtrlDouble(panel, min=0, value="15", inc=0.01)

        content_sizer.AddMany([color_label, self.color_spin, spatial_label, self.spatial_spin])

        return content_sizer

    def onOk(self, event):
        color = self.color_spin.GetValue()
        spatial = self.spatial_spin.GetValue()
        im = self.map.data

        bi = wx.BusyInfo("Denoising, please wait", parent=self.GetParent())
        self.map._data = denoise_bilateral(im, sigma_color=color, sigma_spatial=spatial, multichannel=False)
        self.map.plot_settings["norm"].vmin = self.map.data.min()
        self.map.plot_settings["norm"].vmax = self.map.data.max()
        del bi

        pub.sendMessage(EVT_CHANGE_TAB, tab_id=self.tab_id, data=self.map)
        event.Skip()


class WaveletDenoiseDialog(DefaultDialog):
    def __init__(self, parent, tab_id, map):
        self.tab_id = tab_id
        self.map = map
        DefaultDialog.__init__(self, parent, 'Denoise Wavelet')

    def createContent(self, panel):
        content_sizer = wx.FlexGridSizer(2, 5, 5)
        estimated_sigma = estimate_sigma(self.map.data)

        estimation_label = wx.StaticText(panel, label="Estimated Sigma: ")
        estimation_value = wx.StaticText(panel, label=str(estimated_sigma))
        wavelet_label = wx.StaticText(panel, label="Wavelet: ")
        self.wavelet_text = wx.TextCtrl(panel, value="db1")
        sigma_label = wx.StaticText(panel, label="Sigma: ")
        self.sigma_spin = wx.SpinCtrlDouble(panel, value=str(estimated_sigma), inc=0.01)
        level_label = wx.StaticText(panel, label="Level(0 for auto): ")
        self.level_spin = wx.SpinCtrl(panel, value="0")

        content_sizer.AddMany(
            [estimation_label, estimation_value, wavelet_label, self.wavelet_text, level_label, self.level_spin,
             sigma_label, self.sigma_spin])

        return content_sizer

    def onOk(self, event):
        wavelet = self.wavelet_text.GetValue()
        sigma = self.sigma_spin.GetValue()
        level = self.level_spin.GetValue()
        if level == 0:
            level = None
        im = self.map.data

        bi = wx.BusyInfo("Denoising, please wait", parent=self.GetParent())
        self.map._data = denoise_wavelet(im, sigma=sigma, wavelet=wavelet, wavelet_levels=level)
        self.map.plot_settings["norm"].vmin = self.map.data.min()
        self.map.plot_settings["norm"].vmax = self.map.data.max()
        del bi

        pub.sendMessage(EVT_CHANGE_TAB, tab_id=self.tab_id, data=self.map)
        event.Skip()
