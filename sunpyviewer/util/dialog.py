from abc import abstractmethod

import wx


class DefaultDialog(wx.Dialog):

    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, -1, title)

        self.info_bar = wx.InfoBar(self)
        content_sizer = self.createContent(self)
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
    def createContent(self, panel):
        pass

    @abstractmethod
    def onOk(self, event):
        event.Skip()
