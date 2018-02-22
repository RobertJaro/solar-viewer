import astropy.units as u
import wx

from sunpyviewer.util.default_dialog import DialogController
from sunpyviewer.util.default_tool import ItemConfig
from sunpyviewer.viewer.content import ViewerType, DataType


class RotateController(DialogController):
    def __init__(self):
        DialogController.__init__(self)

    @staticmethod
    def getItemConfig():
        return ItemConfig().setTitle("Rotate").setMenuPath("Edit\\Rotate").addSupportedViewer(
            ViewerType.ANY).addSupportedData(
            DataType.MAP)

    def getContentView(self, parent):
        panel = wx.Panel(parent)
        content_sizer = wx.FlexGridSizer(2, 5, 5)

        angle_label = wx.StaticText(panel, label="Angle:")
        self.angle_spin = wx.SpinCtrlDouble(panel, min=-360, max=360, inc=0.01)

        content_sizer.AddMany([angle_label, self.angle_spin])

        panel.SetSizerAndFit(content_sizer)
        return panel

    def refreshContent(self, viewer_ctrl):
        pass

    def modifyData(self, data, data_type):
        plot_settings = data.plot_settings
        rotated_map = data.rotate(angle=self.angle_spin.GetValue() * u.deg)
        rotated_map.plot_settings = plot_settings
        return rotated_map
