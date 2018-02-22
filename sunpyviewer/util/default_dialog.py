import copy
from abc import abstractmethod, ABC

import wx
from wx.lib.pubsub import pub

from sunpyviewer.util.event import getOKEvent
from sunpyviewer.viewer import EVT_CHANGE_TAB


class DialogController(ABC):

    def __init__(self):
        self.viewer_ctrl = None
        self.dlg = None
        self.info_bar = None

    @staticmethod
    @abstractmethod
    def getItemConfig():
        pass

    @abstractmethod
    def getContentView(self, parent):
        pass

    @abstractmethod
    def refreshContent(self, viewer_ctrl):
        pass

    @abstractmethod
    def modifyData(self, data, data_type):
        pass

    def openDialog(self, parent, viewer_ctrl):
        self.viewer_ctrl = viewer_ctrl
        self.dlg = DefaultDialog(parent, self.getItemConfig().title, self)
        self.info_bar = self.dlg.info_bar
        self.refreshContent(viewer_ctrl)

        pub.subscribe(self._ok, getOKEvent(self.dlg.Id))
        self.dlg.ShowModal()
        self.dlg.Destroy()

    def _ok(self):
        viewer_ctrl = self.viewer_ctrl
        content = copy.deepcopy(viewer_ctrl.getContent())
        try:
            data = self.modifyData(content, viewer_ctrl.data_type)
        except Exception as ex:
            self.info_bar.ShowMessage(str(ex), flags=wx.ICON_WARNING)
            self.dlg.Fit()
            return
        pub.sendMessage(EVT_CHANGE_TAB, tab_id=viewer_ctrl.getId(), data=data)
        self.dlg.Close()


class DefaultDialog(wx.Dialog):

    def __init__(self, parent, title, ctrl):
        wx.Dialog.__init__(self, parent, -1, title)

        self.info_bar = wx.InfoBar(self)
        content_sizer = ctrl.getContentView(self)
        button_sizer = self.createButtons(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.info_bar, border=5, flag=wx.EXPAND | wx.ALL)
        sizer.Add(content_sizer, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(wx.StaticLine(self), flag=wx.EXPAND | wx.HORIZONTAL)
        sizer.AddSpacer(5)
        sizer.Add(button_sizer, flag=wx.EXPAND)
        sizer.AddSpacer(5)
        self.SetSizerAndFit(sizer)

    def createButtons(self, panel):
        ok_button = wx.Button(panel, wx.ID_OK, "&OK")
        ok_button.SetDefault()
        cancel_button = wx.Button(panel, wx.ID_CANCEL, "&Cancel")
        button_sizer = wx.StdDialogButtonSizer()
        button_sizer.AddButton(ok_button)
        button_sizer.AddButton(cancel_button)
        button_sizer.Realize()

        ok_button.Bind(wx.EVT_BUTTON, self.onOk)

        return button_sizer

    @abstractmethod
    def onOk(self, event):
        pub.sendMessage(getOKEvent(self.Id))
