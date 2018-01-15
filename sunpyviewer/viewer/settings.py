import os

import sunpy
import wx

from sunpyviewer.util.dialog import DefaultDialog


class DBDialog(DefaultDialog):
    def __init__(self, parent):
        DefaultDialog.__init__(self, parent, "Change Database Setttings")

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
