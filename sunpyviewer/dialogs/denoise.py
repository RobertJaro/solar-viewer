import wx
from skimage.restoration import denoise_tv_chambolle, denoise_bilateral, denoise_wavelet, estimate_sigma

from sunpyviewer.util.default_dialog import DialogController
from sunpyviewer.util.default_tool import ItemConfig
from sunpyviewer.viewer.content import ViewerType, DataType


class TVDenoiseController(DialogController):
    def __init__(self):
        DialogController.__init__(self)

    @staticmethod
    def getItemConfig():
        return ItemConfig().setTitle("TV Denoising").setMenuPath("Edit\\Denoise\\TV").addSupportedViewer(
            ViewerType.ANY).addSupportedData(
            DataType.MAP)

    def getContentView(self, parent):
        self.parent = parent
        content_sizer = wx.FlexGridSizer(2, 5, 5)

        weight_label = wx.StaticText(parent, label="Weight: ")
        self.weight_spin = wx.SpinCtrlDouble(parent, min=0, value="0.1", inc=0.01)

        content_sizer.AddMany([weight_label, self.weight_spin])

        return content_sizer

    def refreshContent(self, viewer_ctrl):
        pass

    def modifyData(self, data, data_type):
        weight = self.weight_spin.GetValue()
        im = data.data
        bi = wx.BusyInfo("Denoising, please wait", parent=self.parent)
        data._data = denoise_tv_chambolle(im, weight=weight)
        data.plot_settings["norm"].vmin = data.data.min()
        data.plot_settings["norm"].vmax = data.data.max()
        del bi
        return data


class BilateralDenoiseController(DialogController):
    def __init__(self):
        DialogController.__init__(self)

    @staticmethod
    def getItemConfig():
        return ItemConfig().setTitle("Bilateral Denoising").setMenuPath("Edit\\Denoise\\Bilateral").addSupportedViewer(
            ViewerType.ANY).addSupportedData(
            DataType.MAP)

    def getContentView(self, parent):
        self.parent = parent
        panel = wx.Panel(parent)
        content_sizer = wx.FlexGridSizer(2, 5, 5)

        color_label = wx.StaticText(panel, label="Sigma Color: ")
        self.color_spin = wx.SpinCtrlDouble(panel, min=0, value="0.05", inc=0.01)
        spatial_label = wx.StaticText(panel, label="Spatial Color: ")
        self.spatial_spin = wx.SpinCtrlDouble(panel, min=0, value="15", inc=0.01)

        content_sizer.AddMany([color_label, self.color_spin, spatial_label, self.spatial_spin])

        panel.SetSizerAndFit(content_sizer)
        return panel

    def refreshContent(self, viewer_ctrl):
        pass

    def modifyData(self, data, data_type):
        color = self.color_spin.GetValue()
        spatial = self.spatial_spin.GetValue()
        im = data.data

        bi = wx.BusyInfo("Denoising, please wait", parent=self.parent)
        data._data = denoise_bilateral(im, sigma_color=color, sigma_spatial=spatial, multichannel=False)
        data.plot_settings["norm"].vmin = data.data.min()
        data.plot_settings["norm"].vmax = data.data.max()
        del bi

        return data


class WaveletDenoiseController(DialogController):
    def __init__(self):
        DialogController.__init__(self)

    @staticmethod
    def getItemConfig():
        return ItemConfig().setTitle("Wavelet Denoising").setMenuPath("Edit\\Denoise\\Wavelet").addSupportedViewer(
            ViewerType.ANY).addSupportedData(
            DataType.MAP)

    def getContentView(self, parent):
        self.parent = parent
        panel = wx.Panel(parent)
        content_sizer = wx.FlexGridSizer(2, 5, 5)

        estimation_label = wx.StaticText(panel, label="Estimated Sigma: ")
        self.estimation_value = wx.StaticText(panel)
        wavelet_label = wx.StaticText(panel, label="Wavelet: ")
        self.wavelet_text = wx.TextCtrl(panel, value="db1")
        sigma_label = wx.StaticText(panel, label="Sigma: ")
        self.sigma_spin = wx.SpinCtrlDouble(panel, inc=0.01)
        level_label = wx.StaticText(panel, label="Level(0 for auto): ")
        self.level_spin = wx.SpinCtrl(panel, value="0")

        content_sizer.AddMany(
            [estimation_label, self.estimation_value, wavelet_label, self.wavelet_text, level_label, self.level_spin,
             sigma_label, self.sigma_spin])

        panel.SetSizerAndFit(content_sizer)
        return panel

    def refreshContent(self, viewer_ctrl):
        estimated_sigma = estimate_sigma(viewer_ctrl.getContent().data)
        self.sigma_spin.SetValue(estimated_sigma)
        self.estimation_value.SetLabel(str(estimated_sigma))

    def modifyData(self, data, data_type):
        wavelet = self.wavelet_text.GetValue()
        sigma = self.sigma_spin.GetValue()
        level = self.level_spin.GetValue()
        if level == 0:
            level = None
        im = data.data

        bi = wx.BusyInfo("Denoising, please wait", parent=self.parent)
        data._data = denoise_wavelet(im, sigma=sigma, wavelet=wavelet, wavelet_levels=level)
        data.plot_settings["norm"].vmin = data.data.min()
        data.plot_settings["norm"].vmax = data.data.max()
        del bi

        return data
