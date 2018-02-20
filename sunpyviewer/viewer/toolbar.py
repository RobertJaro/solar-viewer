import os
from enum import Enum

import wx
from wx import aui
from wx.lib.pubsub import pub

from sunpyviewer.util.common import Singleton
from sunpyviewer.util.data import resources_dir
from sunpyviewer.viewer import EVT_MPL_MODE_CHANGED, EVT_MPL_CHANGE_MODE, EVT_MPL_RESET


class ViewMode(Enum):
    NONE = "none"
    PAN = "pan"
    ZOOM = "zoom"


class ToolbarModel():
    def __init__(self):
        self.mode = ViewMode.NONE

    def setMode(self, mode):
        self.mode = mode
        pub.sendMessage(EVT_MPL_MODE_CHANGED, mode=mode)

    def getMode(self):
        return self.mode


class ToolbarController(metaclass=Singleton):

    def __init__(self, parent):
        self.model = ToolbarModel()

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

        pub.subscribe(self.setMode, EVT_MPL_CHANGE_MODE)

        toolbar.Realize()
        self.view = toolbar

    def getMode(self):
        return self.model.getMode()

    def setMode(self, mode):
        self.pan_item.SetState(False)
        self.zoom_item.SetState(False)

        self.model.setMode(mode)
        if mode is ViewMode.PAN:
            self.pan_item.SetState(True)
        if mode is ViewMode.ZOOM:
            self.zoom_item.SetState(True)
        self.view.Realize()

    def disablePan(self, *args):
        self.pan_item.SetState(False)
        self.view.Realize()

    def disableZoom(self, *args):
        self.zoom_item.SetState(False)
        self.view.Realize()

    def onPan(self, event):
        if self.model.getMode() is ViewMode.PAN:
            self.model.setMode(ViewMode.NONE)
        else:
            self.model.setMode(ViewMode.PAN)
        event.Skip()

    def onReset(self, event):
        pub.sendMessage(EVT_MPL_RESET)
        event.Skip()

    def onZoom(self, event):
        if self.model.getMode() is ViewMode.ZOOM:
            self.model.setMode(ViewMode.NONE)
        else:
            self.model.setMode(ViewMode.ZOOM)
        event.Skip()

    def getView(self):
        return self.view
