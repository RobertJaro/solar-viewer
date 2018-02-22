import copy
import logging
from abc import abstractmethod, ABC

import wx
from wx.lib.pubsub import pub
from wx.lib.scrolledpanel import ScrolledPanel

from sunpyviewer.util.event import isSupported, getOKEvent, getPreviewEvent
from sunpyviewer.viewer import EVT_CHANGE_TAB, EVT_TAB_SELECTION_CHANGED
from sunpyviewer.viewer.content import PreviewUtil


class ItemConfig:

    def __init__(self):
        self.menu_path = ""
        self.title = ""
        self.supported_data_types = []
        self.supported_viewer_types = []

    def setMenuPath(self, path):
        self.menu_path = path
        return self

    def setTitle(self, title):
        self.title = title
        return self

    def setSupportedData(self, data_types):
        self.supported_data_types = data_types
        return self

    def addSupportedData(self, data_type):
        self.supported_data_types.append(data_type)
        return self

    def setSupportedViewer(self, viewer_types):
        self.supported_data_types = viewer_types
        return self

    def addSupportedViewer(self, viewer_type):
        self.supported_viewer_types.append(viewer_type)
        return self


class ToolController(ABC):

    @staticmethod
    @abstractmethod
    def getItemConfig():
        return ItemConfig()

    @abstractmethod
    def closeView(self):
        pass

    @abstractmethod
    def createView(self, parent, view_ctrl):
        pass


# Use as Mixin with ToolController
class DataControllerMixin(ABC):

    def __init__(self):
        self.view = None
        self.content_view = None
        self.viewer_ctrl = None

    @abstractmethod
    def modifyData(self, data, data_type):
        pass

    @abstractmethod
    def getContentView(self, parent):
        pass

    @abstractmethod
    def refreshContent(self, data, data_type):
        pass

    def createView(self, parent, view_ctrl):
        self.view = DataToolPanel(parent, self)

        self._onTabChange(view_ctrl)
        pub.subscribe(self._onTabChange, EVT_TAB_SELECTION_CHANGED)
        pub.subscribe(self._ok, getOKEvent(self.view.Id))
        pub.subscribe(self._preview, getPreviewEvent(self.view.Id))
        return self.view

    def closeView(self):
        pub.unsubscribe(self._onTabChange, EVT_TAB_SELECTION_CHANGED)
        self.view = None
        self.content_view = None

    def _onTabChange(self, ctrl):
        self.view.info_bar.Hide()
        if not isSupported(self, ctrl):
            self.view.enable(False)
            self.viewer_ctrl = None
            self.view.info_bar.ShowMessage(
                "Only Supports:\nDataTypes: {}\nViewerTypes: {} ".format(self.getItemConfig().supported_data_types,
                                                                         self.getItemConfig().supported_viewer_types))
            self.view.Layout()
            self.view.FitInside()
            return
        self.viewer_ctrl = ctrl
        self.view.resetPreview()
        self.refreshContent(ctrl.getContent(), ctrl.data_type)
        self.view.enable(True)
        self.view.Layout()
        self.view.FitInside()

    def _ok(self):
        self.view.info_bar.Hide()
        try:
            viewer_ctrl = self.viewer_ctrl
            content = copy.deepcopy(viewer_ctrl.getContent())
            data = self.modifyData(content, viewer_ctrl.data_type)
            pub.sendMessage(EVT_CHANGE_TAB, tab_id=viewer_ctrl.getId(), data=data)
        except Exception as e:
            logging.exception(e)
            self.view.info_bar.ShowMessage(str(e), flags=wx.ICON_ERROR)
            self.view.Layout()

    def _preview(self):
        self.view.info_bar.Hide()
        try:
            viewer_ctrl = self.viewer_ctrl
            content = copy.deepcopy(viewer_ctrl.getContent())
            data = self.modifyData(content, viewer_ctrl.data_type)
            self._openPreview(data)
        except Exception as e:
            logging.exception(e)
            self.view.info_bar.ShowMessage(str(e), flags=wx.ICON_ERROR)
            self.view.Layout()

    def _openPreview(self, data):
        pane = self.view.preview_panel.GetPane()
        for children in pane.Children:
            children.Destroy()
        preview = PreviewUtil.getPreviewer(pane, data, self.viewer_ctrl.data_type, self.viewer_ctrl.viewer_type)
        preview.SetMinSize((10, 250))
        sizer = pane.GetSizer()
        sizer.Add(preview, 1, wx.GROW | wx.ALL, 2)
        self.view.preview_panel.Enable(True)
        self.view.preview_panel.Expand()
        self.view.Layout()
        self.view.FitInside()


class DataToolPanel(ScrolledPanel):

    def __init__(self, parent, ctrl):
        ScrolledPanel.__init__(self, parent)
        self.SetAutoLayout(True)
        self.SetupScrolling()

        self.info_bar = wx.InfoBar(self)
        button_sizer = self._initButtons()
        self.preview_panel = self._initPreview()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.info_bar, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(self.preview_panel, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        self.content = ctrl.getContentView(self)
        for panel in self.content:
            sizer.Add(panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(button_sizer, flag=wx.EXPAND | wx.ALL, border=10)
        self.SetSizerAndFit(sizer)

        self.preview_panel.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self._onCollapse)

    def enable(self, value=True):
        self.ok_button.Enable(value)
        self.preview_button.Enable(value)

    def _initPreview(self):
        prev_pane = wx.CollapsiblePane(self, label="Preview")
        prev_pane.SetMinSize((300, -1))
        pane = prev_pane.GetPane()
        pane_sizer = wx.BoxSizer(wx.VERTICAL)
        pane.SetSizerAndFit(pane_sizer)
        pane_sizer.SetSizeHints(pane)
        prev_pane.Enable(False)
        return prev_pane

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

        self.ok_button = ok_button
        self.preview_button = preview_button

        return button_sizer

    def resetPreview(self):
        self.preview_panel.Collapse(True)
        self.preview_panel.Enable(False)

    def _onOk(self, *args):
        pub.sendMessage(getOKEvent(self.Id))

    def _onPreview(self, *args):
        pub.sendMessage(getPreviewEvent(self.Id))

    def _onCollapse(self, *args):
        self.Layout()
        self.FitInside()
