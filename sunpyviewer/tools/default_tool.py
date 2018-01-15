from abc import abstractmethod, ABC

import wx
from wx.lib.pubsub import pub
from wx.lib.scrolledpanel import ScrolledPanel

from sunpyviewer.util.wxmatplot import PlotPanel
from sunpyviewer.viewer import EVT_MAP_CLOSED, EVT_MAP_CHANGED, EVT_MAP_ADDED, EVT_CHANGE_TAB


class ToolController(ABC):
    @abstractmethod
    def closeView(self, *args):
        pass

    @abstractmethod
    def createView(self, *args):
        pass


class PreviewPanel(PlotPanel):
    def __init__(self, parent, map):
        self.map = map
        PlotPanel.__init__(self, parent)

    def draw(self):
        plot_settings = self.map.plot_settings
        ax = self.figure.add_subplot(111, projection=self.map)
        ax.imshow(self.map.data, **plot_settings)


class MapToolPanel(ScrolledPanel):

    def __init__(self, parent, content_ctrl):
        self.content_ctrl = content_ctrl
        self.selected_id = None

        self.maps = content_ctrl.getMaps()
        active_tab_id = content_ctrl.getActiveTabId()
        if active_tab_id in self.maps.keys():
            self.selected_id = active_tab_id

        ScrolledPanel.__init__(self, parent)
        self.SetAutoLayout(True)
        self.SetupScrolling()

        self.info_bar = wx.InfoBar(self)
        button_sizer = self._initButtons()
        self.preview_panel = self._initPreview()
        content = self.initContent()
        map_selection = self._initMapSelection()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.info_bar, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(map_selection, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(self.preview_panel, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        for panel in content:
            sizer.Add(panel, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(button_sizer, flag=wx.EXPAND | wx.ALL, border=10)
        self.SetSizerAndFit(sizer)

        self.preview_panel.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self._onCollapse)
        pub.subscribe(self.onMapAdded, EVT_MAP_ADDED)
        pub.subscribe(self.onMapRemoved, EVT_MAP_CLOSED)
        pub.subscribe(self.onMapChanged, EVT_MAP_CHANGED)

    def _initMapSelection(self):
        panel = wx.Panel(self)

        box_sizer = wx.StaticBoxSizer(wx.VERTICAL, panel, "Map Selection")
        self.map_choice = wx.Choice(panel)
        self._refreshMapChoice()
        box_sizer.Add(self.map_choice, flag=wx.ALL | wx.EXPAND, border=2)
        panel.SetSizerAndFit(box_sizer)

        self.map_choice.Bind(wx.EVT_CHOICE, self._onSelectionChanged)

        return panel

    def _initPreview(self):
        result_pane = wx.CollapsiblePane(self, label="Preview")
        pane = result_pane.GetPane()
        pane_sizer = wx.BoxSizer(wx.VERTICAL)
        pane.SetSizerAndFit(pane_sizer)
        pane_sizer.SetSizeHints(pane)
        result_pane.Enable(False)
        return result_pane

    def _initButtons(self):
        ok_button = wx.Button(self, wx.ID_OK, "&OK")
        preview_button = wx.Button(self, wx.ID_APPLY, "&Preview")
        preview_button.SetDefault()
        button_sizer = wx.StdDialogButtonSizer()
        button_sizer.AddButton(ok_button)
        button_sizer.AddButton(preview_button)
        button_sizer.Realize()

        ok_button.Bind(wx.EVT_BUTTON, self._onOk)
        preview_button.Bind(wx.EVT_BUTTON, self._onPreview)

        if not self.selected_id:
            ok_button.Enable(False)
            preview_button.Enable(False)

        self.ok_button = ok_button
        self.preview_button = preview_button

        return button_sizer

    def _refreshMapChoice(self):
        selection = self.map_choice.GetSelection()
        maps = self.content_ctrl.getMaps()
        self.map_choice.SetItems(["{}: {}".format(id, name) for id, name in maps.items()])
        if self.selected_id:
            self.map_choice.SetSelection(list(maps.keys()).index(self.selected_id))
        if selection is not self.map_choice.GetSelection():
            self._onSelectionChanged()

    def _onSelectionChanged(self, *args):
        if self.map_choice.GetSelection() is wx.NOT_FOUND:
            selected_map = None
            self.ok_button.Enable(False)
            self.preview_button.Enable(False)

        else:
            maps = self.content_ctrl.getMaps()
            self.selected_id = list(maps.keys())[self.map_choice.GetSelection()]
            selected_map = self.content_ctrl.getContent(self.selected_id)
            self.ok_button.Enable(True)
            self.preview_button.Enable(True)

        self.preview_panel.Enable(False)
        self.preview_panel.Collapse(True)
        self.refreshContent(selected_map)
        self.Layout()
        self.FitInside()

    def _preview(self, data):
        pane = self.preview_panel.GetPane()
        for children in pane.Children:
            children.Destroy()
        preview = PreviewPanel(pane, data)
        preview.SetMinSize((-1, 250))
        sizer = pane.GetSizer()
        sizer.Add(preview, 1, wx.GROW | wx.ALL, 2)
        self.preview_panel.Enable(True)
        self.preview_panel.Expand()
        self.Layout()
        self.FitInside()

    def onMapAdded(self, tab_id, data):
        self._refreshMapChoice()

    def onMapRemoved(self, tab_id):
        if tab_id is self.selected_id:
            self.selected_id = None
        self._refreshMapChoice()

    def onMapChanged(self, tab_id, data):
        if tab_id == self.selected_id:
            self._onSelectionChanged()

    def _onOk(self, *args):
        self.info_bar.Hide()
        try:
            modified_map = self.modifyMap(self.content_ctrl.getContent(self.selected_id))
            pub.sendMessage(EVT_CHANGE_TAB, tab_id=self.selected_id, data=modified_map)
        except Exception as e:
            self.info_bar.ShowMessage(str(e), flags=wx.ICON_ERROR)
            self.Layout()

    def _onPreview(self, *args):
        self.info_bar.Hide()
        try:
            modified_map = self.modifyMap(self.content_ctrl.getContent(self.selected_id))
            self._preview(modified_map)
        except Exception as e:
            self.info_bar.ShowMessage(str(e), flags=wx.ICON_ERROR)
            self.Layout()

    def _onCollapse(self, *args):
        self.Layout()
        self.FitInside()

    @abstractmethod
    def modifyMap(self, data):
        pass

    @abstractmethod
    def initContent(self):
        pass

    @abstractmethod
    def refreshContent(self, data):
        pass
