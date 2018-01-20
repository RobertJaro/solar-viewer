import wx

from sunpyviewer.viewer.mainframe import MainFrame


def main():
    app = wx.App(False)
    frame = MainFrame()
    frame.Show(True)
    frame.Maximize(True)
    app.MainLoop()


if __name__ == '__main__':
    main()
