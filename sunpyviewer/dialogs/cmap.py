import sunpy.cm as cm
import wx
from wx.lib.pubsub import pub

from sunpyviewer.viewer import EVT_CHANGE_TAB
from sunpyviewer.viewer.settings import DefaultDialog


class CmapDialog(DefaultDialog):
    def __init__(self, parent, tab_id, map):
        self.map = map
        self.tab_id = tab_id
        DefaultDialog.__init__(self, parent, 'Change Color Map')

    def createContent(self, panel):
        choices = list(cm.cmlist.keys())
        choices.append("Greys_r")
        choices.sort()

        cmap_label = wx.StaticText(panel)
        cmap_label.SetLabel("Colormap:")
        self.cmap_combo = wx.ComboBox(panel, choices=choices, style=wx.CB_DROPDOWN)
        if isinstance(self.map.plot_settings["cmap"], str):
            self.cmap_combo.SetValue(self.map.plot_settings["cmap"])

        content_sizer = wx.FlexGridSizer(2, 5, 5)
        content_sizer.Add(cmap_label)
        content_sizer.Add(self.cmap_combo)
        return content_sizer

    def onOk(self, event):
        self.map.plot_settings["cmap"] = self.cmap_combo.GetValue()
        pub.sendMessage(EVT_CHANGE_TAB, tab_id=self.tab_id, data=self.map)
        event.Skip()
