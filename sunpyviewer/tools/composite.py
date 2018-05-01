import wx
from wx.lib.scrolledpanel import ScrolledPanel

from sunpyviewer.util.default_tool import ToolController, DataControllerMixin, ItemConfig
from sunpyviewer.viewer.content import ViewerType, DataType


class AdjustAlphaController(DataControllerMixin, ToolController):

    def __init__(self):
        self.alpha_inputs = []
        self.order_inputs = []
        self.panel = None

        DataControllerMixin.__init__(self)

    @staticmethod
    def getItemConfig():
        return ItemConfig().setTitle("Adjust alpha and level").setMenuPath("Tools\\Adjust Alpha").addSupportedData(
            DataType.MAP_CUBE).addSupportedViewer(ViewerType.ANY)

    def modifyData(self, data, data_type):
        alpha_list = [a.GetValue() for a in self.alpha_inputs]
        order_list = [o.GetValue() for o in self.order_inputs]
        for i in range(len(data._maps)):
            data.set_alpha(i, alpha_list[i])
            data.set_zorder(i, order_list[i])
        return data

    def getContentView(self, parent):
        base = wx.Panel(parent)
        box_sizer = wx.StaticBoxSizer(wx.VERTICAL, base, "Composite Map Adjustment")
        box_sizer.SetMinSize((500, 300))

        panel = ScrolledPanel(base)
        panel.SetAutoLayout(True)
        panel.SetupScrolling(scroll_x=False, scroll_y=True)

        grid_sizer = wx.FlexGridSizer(3, 15, 15)
        grid_sizer.AddGrowableCol(2, 1)

        order_label = wx.StaticText(panel, label="Order")
        alpha_label = wx.StaticText(panel, label="Alpha")
        map_label = wx.StaticText(panel, label="Map")
        grid_sizer.Add(order_label, flag=wx.ALIGN_CENTER)
        grid_sizer.Add(alpha_label, flag=wx.ALIGN_CENTER)
        grid_sizer.Add(map_label, flag=wx.ALIGN_CENTER)

        panel.SetSizer(grid_sizer)
        box_sizer.Add(panel, proportion=1, flag=wx.ALL | wx.EXPAND, border=2)
        base.SetSizerAndFit(box_sizer)
        panel.Hide()
        self.panel = panel
        self.grid_sizer = grid_sizer
        return [base]

    def refreshContent(self, data, data_type):
        panel = self.panel
        panel.Hide()
        grid_sizer = self.grid_sizer
        length = len(data._maps)
        # remove old data
        for child in list(panel.GetChildren())[3:]:
            grid_sizer.Detach(child)
            child.Destroy()
        self.alpha_inputs = []
        self.order_inputs = []
        # add new data
        for i in range(length):
            order_input = wx.SpinCtrl(panel, min=1, max=100, value=str(data.get_zorder(i)))
            alpha_input = wx.SpinCtrlDouble(panel, min=0, max=1, inc=0.01, value=str(data.get_alpha(i)))
            image_panel = wx.StaticText(panel, label=data.get_map(i).name)
            grid_sizer.Add(order_input, 0, wx.ALIGN_CENTER)
            grid_sizer.Add(alpha_input, 0, wx.ALIGN_CENTER)
            grid_sizer.Add(image_panel, 1, wx.ALIGN_CENTER)
            self.alpha_inputs.append(alpha_input)
            self.order_inputs.append(order_input)
        panel.Show()
