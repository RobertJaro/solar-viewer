import os

import sunpy
import wx


class DBDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "Change Database Setttings")

        content_sizer = self.createContent(self)
        button_sizer = self.createButtons(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
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

    def createContent(self, panel):
        url_label = wx.StaticText(panel)
        url_label.SetLabel("DB-URL:")
        self.url_input = wx.TextCtrl(panel, value=sunpy.config.get("database", "url"), size=(300, -1))
        path_label = wx.StaticText(panel)
        path_label.SetLabel("Download Directory:")
        self.dir_picker = wx.DirPickerCtrl(panel, path=sunpy.config.get("downloads", "download_dir"), size=(300, -1))

        content_sizer = wx.FlexGridSizer(2, 5, 5)
        content_sizer.Add(url_label)
        content_sizer.Add(self.url_input)
        content_sizer.Add(path_label)
        content_sizer.Add(self.dir_picker)
        return content_sizer

    def onOk(self, event):
        dir = self.dir_picker.GetPath()
        url = self.url_input.GetValue()

        if not os.path.isabs(dir):
            self.info_bar.ShowMessage("Invalid Directory!", wx.ICON_ERROR)
            self.Fit()
            return

        sunpy.config.set("database", "url", url)
        sunpy.config.set("downloads", "download_dir", dir)
        self.Destroy()
