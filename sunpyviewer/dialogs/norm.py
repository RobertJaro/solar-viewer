from enum import Enum

import matplotlib.colors as colors
import wx
from astropy.visualization import mpl_normalize, stretch

from sunpyviewer.util.default_dialog import DialogController
from sunpyviewer.util.default_tool import ItemConfig
from sunpyviewer.viewer.content import ViewerType, DataType


class Norm(Enum):
    NO = "no norm"
    LINEAR = "linear norm"
    LOG = "log norm"
    POWER = "power norm"
    IMAGE = "image normalize"

    @staticmethod
    def convertToString(norm):
        if isinstance(norm, colors.LogNorm):
            return Norm.LOG.value
        if isinstance(norm, colors.PowerNorm):
            return Norm.POWER.value
        if isinstance(norm, colors.NoNorm):
            return Norm.NO.value
        if isinstance(norm, mpl_normalize.ImageNormalize):
            return Norm.IMAGE.value
        if isinstance(norm, colors.Normalize):
            return Norm.LINEAR.value


class Stretch(Enum):
    LINEAR = "linear"
    SINH = "sinh"
    ASINH = "asinh"
    POWER = "power"

    @staticmethod
    def convertToString(norm):
        if isinstance(norm, stretch.AsinhStretch):
            return Stretch.ASINH.value
        if isinstance(norm, stretch.SinhStretch):
            return Stretch.SINH.value
        if isinstance(norm, stretch.LinearStretch):
            return Stretch.LINEAR.value
        if isinstance(norm, stretch.PowerStretch):
            return Stretch.POWER.value


class NormController(DialogController):
    def __init__(self):
        DialogController.__init__(self)

    @staticmethod
    def getItemConfig():
        return ItemConfig().setTitle("Select Normalization").setMenuPath("Edit\\Change Norm").addSupportedViewer(
            ViewerType.MPL).addSupportedData(
            DataType.MAP).addSupportedData(DataType.PLAIN_2D)

    def getContentView(self, parent):
        panel = wx.Panel(parent)
        content_sizer = wx.FlexGridSizer(2, 5, 5)

        norm_label = wx.StaticText(panel)
        norm_label.SetLabel("Normalization:")

        choices = [e.value for e in Norm]
        self.norm_combo = wx.Choice(panel, choices=choices)

        self.stretch_label = wx.StaticText(panel)
        self.stretch_label.SetLabel("Stretch:")
        stretch_choices = [e.value for e in Stretch]
        self.stretch_combo = wx.Choice(panel, choices=stretch_choices)

        self.stretch_a_label = wx.StaticText(panel, label="a:")
        self.stretch_a_spin = wx.SpinCtrlDouble(panel, min=0, value="0.1", inc=0.01)

        self.stretch_power_label = wx.StaticText(panel, label="power:")
        self.stretch_power_spin = wx.SpinCtrlDouble(panel, min=0, value="0.1", inc=0.01)

        self.power_label = wx.StaticText(panel)
        self.power_label.SetLabel("Power:")
        self.power_spin = wx.SpinCtrl(panel, min=1, value="1")

        content_sizer.AddMany(
            [norm_label, self.norm_combo, self.stretch_label, self.stretch_combo, self.stretch_a_label,
             self.stretch_a_spin, self.stretch_power_label, self.stretch_power_spin,
             self.power_label, self.power_spin])

        self.norm_combo.Bind(wx.EVT_CHOICE, self.onSelect)
        self.stretch_combo.Bind(wx.EVT_CHOICE, self.onSelect)

        panel.SetSizerAndFit(content_sizer)
        return panel

    def refreshContent(self, viewer_ctrl):
        map = viewer_ctrl.getContent()
        self.norm_combo.SetStringSelection(Norm.convertToString(map.plot_settings["norm"]))
        if self.norm_combo.GetStringSelection() == Norm.IMAGE.value:
            self.stretch_combo.SetStringSelection(Stretch.convertToString(map.plot_settings["norm"].stretch))
        if self.stretch_combo.GetStringSelection() == Stretch.SINH.value or self.stretch_combo.GetStringSelection() == Stretch.ASINH.value:
            self.stretch_a_spin.SetValue(map.plot_settings["norm"].stretch.a)
        if self.stretch_combo.GetStringSelection() == Stretch.POWER.value:
            self.stretch_power_spin.SetValue(map.plot_settings["norm"].stretch.power)
        if self.norm_combo.GetStringSelection() == Norm.POWER.value:
            self.power_spin.SetValue(map.plot_settings["norm"].gamma)
        self.onSelect()

    def modifyData(self, data, data_type):
        selection = Norm(self.norm_combo.GetStringSelection())
        old_norm = data.plot_settings["norm"]
        clip = old_norm.clip
        vmin = old_norm.vmin
        vmax = old_norm.vmax

        if selection is Norm.LOG:
            if vmin <= 0:
                raise Exception("Values must be positive for log-norm")
            data.plot_settings["norm"] = colors.LogNorm(vmin=vmin, vmax=vmax, clip=clip)
        if selection is Norm.NO:
            data.plot_settings["norm"] = colors.NoNorm(vmin=vmin, vmax=vmax, clip=clip)
        if selection is Norm.LINEAR:
            data.plot_settings["norm"] = colors.Normalize(vmin=vmin, vmax=vmax, clip=clip)
        if selection is Norm.POWER:
            data.plot_settings["norm"] = colors.PowerNorm(self.power_spin.GetValue(), vmin=vmin, vmax=vmax,
                                                          clip=clip)
        if selection is Norm.IMAGE:
            data.plot_settings["norm"] = mpl_normalize.ImageNormalize(vmin=vmin, vmax=vmax, clip=clip,
                                                                      stretch=self.getStretch())

        return data

    def onSelect(self, *args):
        if self.norm_combo.GetStringSelection() == Norm.POWER.value:
            self.power_label.Show()
            self.power_spin.Show()
        else:
            self.power_label.Hide()
            self.power_spin.Hide()
        if self.norm_combo.GetStringSelection() == Norm.IMAGE.value:
            self.stretch_combo.Show()
            self.stretch_label.Show()
        else:
            self.stretch_combo.Hide()
            self.stretch_label.Hide()
        if self.norm_combo.GetStringSelection() == Norm.IMAGE.value and (
                self.stretch_combo.GetStringSelection() == Stretch.SINH.value or self.stretch_combo.GetStringSelection() == Stretch.ASINH.value):
            self.stretch_a_spin.Show()
            self.stretch_a_label.Show()
        else:
            self.stretch_a_spin.Hide()
            self.stretch_a_label.Hide()
        if self.norm_combo.GetStringSelection() == Norm.IMAGE.value and self.stretch_combo.GetStringSelection() == Stretch.POWER.value:
            self.stretch_power_spin.Show()
            self.stretch_power_label.Show()
        else:
            self.stretch_power_spin.Hide()
            self.stretch_power_label.Hide()

        self.dlg.Layout()
        self.dlg.Fit()

    def getStretch(self):
        selection = Stretch(self.stretch_combo.GetStringSelection())
        if selection is Stretch.LINEAR:
            return stretch.LinearStretch()
        if selection is Stretch.SINH:
            return stretch.SinhStretch(self.stretch_a_spin.GetValue())
        if selection is Stretch.ASINH:
            return stretch.AsinhStretch(self.stretch_a_spin.GetValue())
        if selection is Stretch.POWER:
            return stretch.PowerStretch(self.stretch_power_spin.GetValue())
        return None
