import os

import wx
from wx import aui
from wx.lib.pubsub import pub

from sunpyviewer.util.data import resources_dir
from sunpyviewer.viewer import EVT_ACTIVATE_PAN, EVT_ACTIVATE_RESET, EVT_ACTIVATE_ZOOM, EVT_DISABLE_TOOLBAR_ITEMS


class ToolbarController:
    def __init__(self, parent):
        toolbar = aui.AuiToolBar(parent, style=aui.AUI_TB_VERTICAL)
        pan_icon = wx.Image(os.path.join(resources_dir, "pan.png"), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        zoom_icon = wx.Image(os.path.join(resources_dir, "zoom.png"), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.pan_item = toolbar.AddTool(wx.ID_ANY, pan_icon, pan_icon, toggle=True)
        self.zoom_item = toolbar.AddTool(wx.ID_ANY, zoom_icon, zoom_icon, toggle=True)
        self.reset_item = toolbar.AddTool(wx.ID_ANY, "home", wx.ArtProvider.GetBitmap(wx.ART_GO_HOME))

        # Toggle Functionality
        toolbar.Bind(wx.EVT_MENU, self.disableZoom, self.pan_item)
        toolbar.Bind(wx.EVT_MENU, self.disablePan, self.zoom_item)

        # Distribute Events
        toolbar.Bind(wx.EVT_MENU, self.onPan, self.pan_item)
        toolbar.Bind(wx.EVT_MENU, self.onZoom, self.zoom_item)
        toolbar.Bind(wx.EVT_MENU, self.onReset, self.reset_item)

        pub.subscribe(self.disableAll, EVT_DISABLE_TOOLBAR_ITEMS)

        toolbar.Realize()
        self.view = toolbar

    def disablePan(self, *args):
        self.pan_item.SetState(False)
        self.view.Realize()

    def disableZoom(self, *args):
        self.zoom_item.SetState(False)
        self.view.Realize()

    def onPan(self, event):
        pub.sendMessage(EVT_ACTIVATE_PAN)
        event.Skip()

    def onZoom(self, event):
        pub.sendMessage(EVT_ACTIVATE_ZOOM)
        event.Skip()

    def onReset(self, event):
        pub.sendMessage(EVT_ACTIVATE_RESET)
        event.Skip()

    def getView(self):
        return self.view

    def disableAll(self):
        if self.pan_item.GetState():
            self.pan_item.SetState(False)
            pub.sendMessage(EVT_ACTIVATE_PAN)
        if self.zoom_item.GetState():
            self.zoom_item.SetState(False)
            pub.sendMessage(EVT_ACTIVATE_ZOOM)
        self.view.Realize()
