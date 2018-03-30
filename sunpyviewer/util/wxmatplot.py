import threading
import time
from abc import abstractmethod

import wx
from matplotlib.backends.backend_wx import wxc
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
from matplotlib.figure import Figure

from sunpyviewer.util.data import saveFigure


class PlotPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.SetBackgroundColour(wxc.NamedColour("WHITE"))

        self.initProgress()
        self.initMainCanvas()
        self.initLayout()
        self.initPopupMenu()

        self._resize_flag = False
        self._drawn_flag = False

        self.Bind(wx.EVT_IDLE, self._onIdle)
        self.Bind(wx.EVT_SIZE, self._onSize)
        self.Bind(wx.EVT_CONTEXT_MENU, self._onShowPopup)

        threading.Thread(target=self.redraw).start()

    def initProgress(self):
        self.progress = wx.Gauge(self, style=wx.GA_HORIZONTAL)
        self.progress.Pulse()

    def initMainCanvas(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self, wx.NewId(), self.figure)
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()
        self.toolbar.Hide()
        self.canvas.Hide()

    def initLayout(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h.Add(self.progress, 1, wx.CENTER)
        self.sizer.Add(sizer_h, 1, wx.CENTER)
        self.sizer.Add(self.canvas, flag=wx.EXPAND)
        self.SetSizerAndFit(self.sizer)

    def initPopupMenu(self):
        self.popupmenu = wx.Menu()
        item = self.popupmenu.Append(-1, "Save Image")
        self.Bind(wx.EVT_MENU, self._onSaveImage, item)

    def _onSize(self, event):
        self._resize_flag = True
        self.canvas.Hide()
        self.progress.Show()
        self.Layout()

    def _onIdle(self, evt):
        if self._resize_flag and self._drawn_flag:
            self._resize_flag = False
            threading.Thread(target=self._SetSize).start()

    def _onShowPopup(self, evt):
        pos = evt.GetPosition()
        pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popupmenu, pos)

    def _onSaveImage(self, evt):
        figure = self.getFigure()
        saveFigure(None, figure)

    def _SetSize(self):
        pixels = tuple(self.GetClientSize())
        self.canvas.SetSize(pixels)
        self.figure.set_size_inches(float(pixels[0]) / self.figure.get_dpi(),
                                    float(pixels[1]) / self.figure.get_dpi())
        wx.CallAfter(self.canvas.draw)
        self.canvas.Show(True)
        self.progress.Show(False)

    def redraw(self):
        self.canvas.Hide()
        self.progress.Show()
        self.draw()
        self._SetSize()
        self._drawn_flag = True

    def getAxes(self):
        # Wait for ax
        while len(self.figure.axes) == 0:
            time.sleep(0.01)
        return self.figure.axes[0]

    def getFigure(self):
        return self.figure

    def getCanvas(self):
        return self.canvas

    @abstractmethod
    def draw(self):
        pass
