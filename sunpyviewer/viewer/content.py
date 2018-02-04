import copy
import threading
from abc import abstractmethod
from enum import Enum

import sunpy.map
import sunpy.timeseries
import wx
from astropy import units as u
from wx import aui
from wx.lib.pubsub import pub

from sunpyviewer.tools import EVT_OPEN_MAP
from sunpyviewer.util.data import saveFigure, saveFits, getMapName
from sunpyviewer.util.wxmatplot import PlotPanel
from sunpyviewer.viewer import EVT_MAP_CLOSED, EVT_TAB_SELECTION_CHANGED, EVT_MAP_ADDED, EVT_STATUS_BAR_UPDATE, \
    EVT_CHANGE_TAB, EVT_ACTIVATE_PAN, EVT_ACTIVATE_ZOOM, EVT_ACTIVATE_RESET, \
    EVT_CHANGE_PLOT_PREFERENCE, EVT_MAP_CHANGED


class ViewMode(Enum):
    PAN = "pan"
    ZOOM = "zoom"


class ContentModel:
    def __init__(self):
        self.tabs = {}
        self.mode = None
        self.plot_preferences = {"show_colorbar": False, "show_limb": False, "draw_contours": False, "draw_grid": False}

    def removeTab(self, page):
        self.tabs = {k: v for k, v in self.tabs.items() if v is not page}
        if isinstance(page, MapTab):
            pub.sendMessage(EVT_MAP_CLOSED, tab_id=page.Id)
        if len(self.tabs) == 0:
            pub.sendMessage(EVT_TAB_SELECTION_CHANGED, tab=None)

    def changeContent(self, id, content):
        tab = self.tabs[id]
        tab.setContent(content)
        if isinstance(tab, MapTab):
            pub.sendMessage(EVT_MAP_CHANGED, tab_id=id, data=content)
        pub.sendMessage(EVT_TAB_SELECTION_CHANGED, tab=tab)
        return tab

    def addTab(self, tab):
        self.tabs[tab.Id] = tab
        if isinstance(tab, MapTab) or isinstance(tab, CompositeMapTab):
            pub.sendMessage(EVT_MAP_ADDED, tab_id=tab.Id, data=tab.getContent())

    def getTab(self, id):
        return self.tabs[id]


class ContentController:
    def __init__(self, parent):
        view = ContentNotebook(parent)
        view.Bind(aui.EVT_AUINOTEBOOK_ALLOW_DND, lambda event: event.Allow())
        view.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.onClose)
        view.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.onTabChanged)

        self.view = view
        self.parent = parent
        self.model = ContentModel()

        pub.subscribe(self.setTabContent, EVT_CHANGE_TAB)

        pub.subscribe(self.pan, EVT_ACTIVATE_PAN)
        pub.subscribe(self.zoom, EVT_ACTIVATE_ZOOM)
        pub.subscribe(self.reset, EVT_ACTIVATE_RESET)

        pub.subscribe(self.setPlotPreference, EVT_CHANGE_PLOT_PREFERENCE)
        pub.subscribe(self.openMap, EVT_OPEN_MAP)

    def getView(self):
        return self.view

    def setTabContent(self, tab_id, data):
        tab = self.model.changeContent(tab_id, data)
        idx = self.view.GetPageIndex(tab)
        self.view.SetSelection(idx)
        threading.Thread(target=tab.redraw).start()

    def onClose(self, event):
        page = self.view.GetPage(event.Selection)
        self.model.removeTab(page)

    def onTabChanged(self, *args):
        tab = self.getActivePage()
        pub.sendMessage(EVT_TAB_SELECTION_CHANGED, tab=tab)

    def onMapMotion(self, event):
        if event.inaxes:
            coord = self.getActiveContent().pixel_to_world(event.xdata * u.pixel, event.ydata * u.pixel)
            pub.sendMessage(EVT_STATUS_BAR_UPDATE, x=coord.Tx, y=coord.Ty)

    def openMap(self, path):
        try:
            map = sunpy.map.Map(path)
            map.path = path
            map_tab = MapTab(self.parent, map, self.model.plot_preferences)
            self.openPanel(getMapName(map), map_tab)
            # add coordinates of mouse courser to status bar
            map_tab.canvas.mpl_connect('motion_notify_event', self.onMapMotion)
        except Exception as ex:
            self.handleFileOpenError(ex, path)

    def openCompositeMap(self, paths):
        try:
            comp_map = sunpy.map.Map(paths, composite=True)
            a = 0.5
            for i in range(len(paths)):
                comp_map.set_alpha(i, a)
            map_tab = CompositeMapTab(self.parent, comp_map)
            self.openPanel("Composite Map", map_tab)
        except Exception as ex:
            self.handleFileOpenError(ex, paths)

    def openTimeSeries(self, path):
        try:
            series = sunpy.timeseries.TimeSeries(path)
            series.path = path
            series_tab = TimeSeriesTab(self.parent, series)
            name = "{} ({:%Y-%m-%d %H:%M:%S})".format(series.source.upper(), series.time_range.start)
            self.openPanel(name, series_tab)
        except Exception as ex:
            self.handleFileOpenError(ex, path)

    def handleFileOpenError(self, ex, path):
        error_msg = "Error during opening: {} \nCaused by: {}".format(path, str(ex))
        dlg = wx.MessageDialog(self.parent, error_msg, style=wx.ICON_ERROR)
        dlg.ShowModal()

    def openPanel(self, name, tab):
        title = "{}: {}".format(tab.Id, name)
        self.view.AddPage(tab, title, True)
        self._initTools(tab)
        self.model.addTab(tab)

    def _initTools(self, tab):
        if self.model.mode is ViewMode.PAN:
            tab.toolbar.pan()
        if self.model.mode is ViewMode.ZOOM:
            tab.toolbar.zoom()

    def pan(self):
        if self.model.mode is ViewMode.PAN:
            self.model.mode = None
        else:
            self.model.mode = ViewMode.PAN
        for page in self.model.tabs.values():
            page.toolbar.pan()

    def zoom(self):
        if self.model.mode is ViewMode.ZOOM:
            self.model.mode = None
        else:
            self.model.mode = ViewMode.ZOOM
        for page in self.model.tabs.values():
            page.toolbar.zoom()

    def reset(self):
        if self.hasPage():
            self.getActivePage().toolbar.home()

    def saveImage(self):
        figure = self.getActivePage().figure
        saveFigure(self.parent, figure)

    def saveFits(self):
        content = self.getActiveContent()
        saveFits(self.parent, content)

    def redrawActive(self):
        threading.Thread(target=self.getActivePage().redraw).start()

    def getMaps(self):
        return {id: getMapName(tab.getContent()) for id, tab in self.model.tabs.items() if isinstance(tab, MapTab)}

    def refreshMaps(self):
        for tab in self.model.tabs.values():
            if isinstance(tab, MapTab) or isinstance(tab, CompositeMapTab):
                threading.Thread(target=tab.redraw).start()

    def getActivePage(self):
        return self.view.GetCurrentPage()

    def hasPage(self):
        return self.view.GetCurrentPage() is not None

    def getActiveContent(self):
        return copy.deepcopy(self.getActivePage().getContent())

    def getActiveTabId(self):
        page = self.getActivePage()
        if page is None:
            return None
        return page.Id

    def getContent(self, tab_id):
        return copy.deepcopy(self.model.getTab(tab_id).getContent())

    def setPlotPreference(self, key, value):
        self.model.plot_preferences[key] = value
        self.refreshMaps()

    def getZoomSubMap(self):
        x = self.getActivePage().figure.axes[0].get_xlim()
        y = self.getActivePage().figure.axes[0].get_ylim()
        bl = [x[0], y[0]]
        tr = [x[1], y[1]]
        current_map = self.getActiveContent()
        sub_map = current_map.submap(bl * u.pixel, tr * u.pixel)
        sub_map.plot_settings = current_map.plot_settings  # preserve settings
        return sub_map


class ContentNotebook(aui.AuiNotebook):
    def __init__(self, parent):
        aui.AuiNotebook.__init__(self, parent, style=aui.AUI_NB_DEFAULT_STYLE | aui.AUI_NB_TAB_EXTERNAL_MOVE)


class AbstractTab(PlotPanel):

    @abstractmethod
    def getContent(self):
        pass

    @abstractmethod
    def setContent(self):
        pass


class MapTab(AbstractTab):
    def __init__(self, parent, map, plot_preferences):
        self.map = map
        self.plot_preferences = plot_preferences
        PlotPanel.__init__(self, parent)

    def getContent(self):
        return self.map

    def setContent(self, data):
        self.map = data

    def draw(self):
        self.figure.clear()
        plot_settings = self.map.plot_settings
        ax = self.figure.add_subplot(111, projection=self.map)
        image = ax.imshow(self.map.data, **plot_settings)
        if self.plot_preferences["show_colorbar"]:
            self.figure.colorbar(image)
        if self.plot_preferences["show_limb"]:
            self.map.draw_limb(axes=ax)
        if self.plot_preferences["draw_contours"]:
            self.map.draw_contours([10, 20, 30, 40, 50, 60, 70, 80, 90] * u.percent, axes=ax)
        if self.plot_preferences["draw_grid"]:
            self.map.draw_grid(grid_spacing=10 * u.deg, axes=ax)


class CompositeMapTab(AbstractTab):
    def __init__(self, parent, comp_map):
        self.comp_map = comp_map
        PlotPanel.__init__(self, parent)

    def getContent(self):
        return self.comp_map

    def setContent(self, comp_map):
        self.comp_map = comp_map

    def draw(self):
        self.figure.clear()
        axes = self.figure.add_subplot(111, projection=self.comp_map.get_map(0))
        for m in self.comp_map._maps:
            params = {
                "origin": "lower",
                # "extent": list(m.xrange.value) + list(m.yrange.value),
                "cmap": m.plot_settings['cmap'],
                "norm": m.plot_settings['norm'],
                "alpha": m.alpha,
                "zorder": m.zorder,
            }
            if m.levels is False:
                axes.imshow(m.data, **params)
            else:
                axes.contour(m.data, m.levels, **params)


class TimeSeriesTab(AbstractTab):
    def __init__(self, parent, time_series):
        self.series = time_series
        PlotPanel.__init__(self, parent)

    def getContent(self):
        return self.series

    def setContent(self, data):
        self.series = data

    def draw(self):
        ax = self.figure.gca()
        self.series.plot(axes=ax)
