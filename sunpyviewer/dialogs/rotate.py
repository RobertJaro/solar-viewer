import astropy.units as u
import wx
from wx.lib.pubsub import pub

from sunpyviewer.viewer import EVT_CHANGE_TAB
from sunpyviewer.viewer.settings import DefaultDialog


class RotateDialog(DefaultDialog):
    def __init__(self, parent, tab_id, map):
        self.tab_id = tab_id
        self.map = map
        DefaultDialog.__init__(self, parent, 'Rotate Map')

    def createContent(self, panel):
        content_sizer = wx.FlexGridSizer(2, 5, 5)

        angle_label = wx.StaticText(panel, label="Angle:")
        self.angle_spin = wx.SpinCtrlDouble(panel, min=0, max=360, inc=0.01)

        content_sizer.AddMany([angle_label, self.angle_spin])

        return content_sizer

    def onOk(self, event):
        plot_settings = self.map.plot_settings
        rotated_map = self.map.rotate(angle=self.angle_spin.GetValue() * u.deg)
        rotated_map.plot_settings = plot_settings
        pub.sendMessage(EVT_CHANGE_TAB, tab_id=self.tab_id, data=rotated_map)
        event.Skip()
