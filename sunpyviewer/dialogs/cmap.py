import sunpy.cm as cm
import wx

from sunpyviewer.util.default_dialog import DialogController
from sunpyviewer.util.default_tool import ItemConfig
from sunpyviewer.viewer.content import ViewerType, DataType


class CmapController(DialogController):
    def __init__(self):
        DialogController.__init__(self)

    @staticmethod
    def getItemConfig():
        return ItemConfig().setTitle("Select Coloramap").setMenuPath("Edit\\Change Colormap").addSupportedViewer(
            ViewerType.MPL).addSupportedData(
            DataType.MAP)

    def getContentView(self, parent):
        panel = wx.Panel(parent)
        choices = list(cm.cmlist.keys())
        choices.append("Greys_r")
        choices.sort()

        cmap_label = wx.StaticText(panel)
        cmap_label.SetLabel("Colormap:")
        self.cmap_combo = wx.ComboBox(panel, choices=choices, style=wx.CB_DROPDOWN)

        content_sizer = wx.FlexGridSizer(2, 5, 5)
        content_sizer.Add(cmap_label)
        content_sizer.Add(self.cmap_combo)
        panel.SetSizerAndFit(content_sizer)
        return panel

    def refreshContent(self, viewer_ctrl):
        if isinstance(viewer_ctrl.getContent().plot_settings["cmap"], str):
            self.cmap_combo.SetValue(viewer_ctrl.getContent().plot_settings["cmap"])

    def modifyData(self, data, data_type):
        data.plot_settings["cmap"] = self.cmap_combo.GetValue()
        return data
