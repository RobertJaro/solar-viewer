import wx
from wx.lib.pubsub import pub

from sunpyviewer.util.wxmatplot import PlotPanel
from sunpyviewer.viewer import EVT_CHANGE_TAB
from sunpyviewer.viewer.settings import DefaultDialog


class _ImagePanel(PlotPanel):
    def __init__(self, parent, map):
        self.map = map
        PlotPanel.__init__(self, parent)

    def draw(self):
        plot_settings = self.map.plot_settings
        ax = self.figure.add_subplot(111, projection=self.map)
        ax.axis("off")
        ax.imshow(self.map.data, **plot_settings)


class CompositeDialog(DefaultDialog):
    def __init__(self, parent, tab_id, comp_map):
        self.tab_id = tab_id
        self.composite_map = comp_map
        self.alpha_inputs = []
        self.order_inputs = []
        DefaultDialog.__init__(self, parent, 'Open Composite Map')

    def createContent(self, panel):
        content_sizer = wx.FlexGridSizer(3, 15, 15)

        order_label = wx.StaticText(panel, label="Order")
        alpha_label = wx.StaticText(panel, label="Alpha")
        map_label = wx.StaticText(panel, label="Map")
        content_sizer.Add(order_label, 0, wx.ALIGN_CENTER)
        content_sizer.Add(alpha_label, 0, wx.ALIGN_CENTER)
        content_sizer.Add(map_label, 0, wx.ALIGN_CENTER)

        maps = self.composite_map._maps
        for i, map in enumerate(maps):
            order_input = wx.SpinCtrl(panel, min=1, max=len(maps), value=str(i + 1))
            alpha_input = wx.SpinCtrlDouble(panel, min=0, max=1, inc=0.01, value=str(map.alpha))
            image_panel = _ImagePanel(panel, map)
            image_panel.SetMinSize((100, 100))
            content_sizer.Add(order_input, 0, wx.ALIGN_CENTER)
            content_sizer.Add(alpha_input, 0, wx.ALIGN_CENTER)
            content_sizer.Add(image_panel, 0, wx.ALIGN_CENTER)
            self.alpha_inputs.append(alpha_input)
            self.order_inputs.append(order_input)

        return content_sizer

    def onOk(self, event):
        alpha_list = [a.GetValue() for a in self.alpha_inputs]
        maps = self.composite_map._maps
        for i, map in enumerate(maps):
            map.alpha = alpha_list[i]
        order_list = [o.GetValue() for o in self.order_inputs]
        maps.sort(key=dict(zip(maps, order_list)).get)  # sort
        pub.sendMessage(EVT_CHANGE_TAB, tab_id=self.tab_id, data=self.composite_map)
        event.Skip()
