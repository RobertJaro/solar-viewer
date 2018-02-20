import copy
import logging
import threading
from abc import abstractmethod, ABC
from enum import Enum

import sunpy.map
import sunpy.timeseries
import wx
from astropy import units as u
from wx import aui
from wx.lib.pubsub import pub

from sunpyviewer.tools import EVT_OPEN_MAP
from sunpyviewer.util.common import Singleton
from sunpyviewer.util.data import saveFigure, saveFits
from sunpyviewer.util.wxmatplot import PlotPanel
from sunpyviewer.viewer import EVT_MAP_CLOSED, EVT_TAB_SELECTION_CHANGED, EVT_MAP_ADDED, EVT_STATUS_BAR_UPDATE, \
    EVT_CHANGE_TAB, EVT_CHANGE_PLOT_PREFERENCE, EVT_MAP_CHANGED, EVT_MPL_MODE_CHANGED, EVT_MPL_RESET
from sunpyviewer.viewer.toolbar import ViewMode, ToolbarController


class DataType(Enum):
    MAP = "map"
    MAP_CUBE = "map_cube"
    SERIES = "series"


class ViewerType(Enum):
    MPL = "matplotlib"
    GINGA = "ginga"


class ContentModel:
    def __init__(self):
        self.viewer_controllers = {}
        self.plot_preferences = {"show_colorbar": False, "show_limb": False, "draw_contours": False, "draw_grid": False}

    def removeViewerController(self, id):
        ctrl = self.viewer_controllers[id]
        del self.viewer_controllers[id]
        if ctrl.getDataType() is DataType.MAP:
            pub.sendMessage(EVT_MAP_CLOSED, tab_id=id)
        if len(self.viewer_controllers) == 0:
            pub.sendMessage(EVT_TAB_SELECTION_CHANGED, ctrl=None)

    def changeContent(self, id, content):
        ctrl = self.viewer_controllers[id]
        ctrl.setContent(content)
        return ctrl

    def addViewerController(self, ctrl):
        tab = ctrl.getView()
        self.viewer_controllers[tab.Id] = ctrl
        if ctrl.getDataType() is DataType.MAP or ctrl.getDataType() is DataType.MAP_CUBE:
            pub.sendMessage(EVT_MAP_ADDED, tab_id=tab.Id, data=ctrl.getContent())

    def getViewerController(self, id):
        return self.viewer_controllers[id]


class ContentController(metaclass=Singleton):
    def __init__(self, parent):
        view = ContentNotebook(parent)
        view.Bind(aui.EVT_AUINOTEBOOK_ALLOW_DND, lambda event: event.Allow())
        view.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.onClose)
        view.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.onTabChanged)

        self.view = view
        self.parent = parent
        self.model = ContentModel()

        pub.subscribe(self.setTabContent, EVT_CHANGE_TAB)

        pub.subscribe(self.setPlotPreference, EVT_CHANGE_PLOT_PREFERENCE)
        pub.subscribe(self.openMap, EVT_OPEN_MAP)

    def getPlotPreferences(self):
        return self.model.plot_preferences

    def getView(self):
        return self.view

    def setTabContent(self, tab_id, data):
        ctrl = self.model.changeContent(tab_id, data)
        idx = self.view.GetPageIndex(ctrl.getView())
        self.view.SetSelection(idx)
        pub.sendMessage(EVT_TAB_SELECTION_CHANGED, ctrl=ctrl)
        threading.Thread(target=ctrl.redraw).start()

    def onClose(self, event):
        page = self.view.GetPage(event.Selection)
        self.model.removeViewerController(page.Id)

    def onTabChanged(self, *args):
        id = self.getActiveTabId()
        ctrl = self.model.viewer_controllers[id]
        pub.sendMessage(EVT_TAB_SELECTION_CHANGED, ctrl=ctrl)

    def openMap(self, path):
        try:
            map_ctrl = MapViewerController(self.parent, path)
            self.openPanel(map_ctrl)
        except Exception as ex:
            logging.exception(ex)
            self.handleFileOpenError(ex, path)

    def openCompositeMap(self, paths):
        try:
            comp_map = sunpy.map.Map(paths, composite=True)
            a = 0.5
            for i in range(len(paths)):
                comp_map.set_alpha(i, a)
            map_tab = CompositeMapViewerController(self.parent, comp_map)
            self.openPanel(map_tab)
        except Exception as ex:
            self.handleFileOpenError(ex, paths)

    def openTimeSeries(self, path):
        try:
            series = sunpy.timeseries.TimeSeries(path)
            series.path = path
            ctrl = TimeSeriesViewerController(self.parent, series)
            self.openPanel(ctrl)
        except Exception as ex:
            self.handleFileOpenError(ex, path)

    def handleFileOpenError(self, ex, path):
        error_msg = "Error during opening: {} \nCaused by: {}".format(path, str(ex))
        dlg = wx.MessageDialog(self.parent, error_msg, style=wx.ICON_ERROR)
        dlg.ShowModal()

    def openPanel(self, ctrl):
        tab = ctrl.getView()
        title = "{}: {}".format(tab.Id, ctrl.getTitle())
        self.model.addViewerController(ctrl)
        self.view.AddPage(tab, title, True)

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

    # TODO: remove maps list selection
    def getMaps(self):
        return {id: ctrl.getTitle() for id, ctrl in self.model.viewer_controllers.items() if
                ctrl.getDataType() is DataType.MAP}

    def refreshMaps(self):
        for ctrl in self.model.viewer_controllers.values():
            if ctrl.getDataType() is DataType.MAP or ctrl.getDataType() is DataType.MAP_CUBE:
                ctrl.redraw()

    def getActiveController(self):
        id = self.getActiveTabId()
        return self.model.viewer_controllers[id]

    def getActivePage(self):
        return self.view.GetCurrentPage()

    def hasPage(self):
        return self.view.GetCurrentPage() is not None

    def getActiveContent(self):
        return copy.deepcopy(self.getActiveController().getContent())

    def getActiveTabId(self):
        page = self.getActivePage()
        if page is None:
            return None
        return page.Id

    def getContent(self, tab_id):
        return copy.deepcopy(self.model.getViewerController(tab_id).getContent())

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


class AbstractViewerController(ABC):
    content_type = None
    viewer_type = None

    @abstractmethod
    def getView(self):
        pass

    @abstractmethod
    def getContent(self):
        pass

    @abstractmethod
    def setContent(self):
        pass

    @abstractmethod
    def getTitle(self):
        pass

    def getDataType(self):
        return self.content_type

    def getViewerType(self):
        return self.viewer_type

    def redraw(self):
        threading.Thread(target=self.getView().redraw).start()


class AbstractMPLController(AbstractViewerController):
    viewer_type = ViewerType.MPL

    def __init__(self):
        self.mode = ViewMode.NONE
        mode = ToolbarController().getMode()
        self.changeMode(mode)

        pub.subscribe(self.changeMode, EVT_MPL_MODE_CHANGED)
        pub.subscribe(self.reset, EVT_MPL_RESET)

    def changeMode(self, mode):
        # deactivate old mode
        if self.mode is ViewMode.PAN:
            self.getView().toolbar.pan()
        if self.mode is ViewMode.ZOOM:
            self.getView().toolbar.zoom()
        # activate new mode
        if mode is ViewMode.PAN:
            self.getView().toolbar.pan()
        if mode is ViewMode.ZOOM:
            self.getView().toolbar.zoom()

        self.mode = mode

    def reset(self):
        if ContentController().getActiveTabId() == self.getView().Id:
            self.getView().toolbar.home()


class MapViewerController(AbstractMPLController):
    content_type = DataType.MAP

    def __init__(self, parent, path):
        self.map = sunpy.map.Map(path)
        self.map.path = path

        self.view = MapViewer(parent, self.map)
        # add coordinates of mouse courser to status bar
        self.view.canvas.mpl_connect('motion_notify_event', self.onMapMotion)

        AbstractMPLController.__init__(self)

    def onMapMotion(self, event):
        if event.inaxes:
            coord = self.map.pixel_to_world(event.xdata * u.pixel, event.ydata * u.pixel)
            pub.sendMessage(EVT_STATUS_BAR_UPDATE, x=coord.Tx, y=coord.Ty)

    def getView(self):
        return self.view

    def getContent(self):
        return self.map

    def setContent(self, data):
        self.map = data
        self.view.map = data
        pub.sendMessage(EVT_MAP_CHANGED, tab_id=self.getView().Id, data=data)

    def getTitle(self):
        try:
            return self.map.name
        except:
            return "Map"


class MapViewer(PlotPanel):

    def __init__(self, parent, map):
        self.map = map
        PlotPanel.__init__(self, parent)

    def draw(self):
        self.figure.clear()
        plot_settings = self.map.plot_settings
        ax = self.figure.add_subplot(111, projection=self.map)
        image = ax.imshow(self.map.data, **plot_settings)
        plot_preferences = ContentController().getPlotPreferences()
        if plot_preferences["show_colorbar"]:
            self.figure.colorbar(image)
        if plot_preferences["show_limb"]:
            self.map.draw_limb(axes=ax)
        if plot_preferences["draw_contours"]:
            self.map.draw_contours([10, 20, 30, 40, 50, 60, 70, 80, 90] * u.percent, axes=ax)
        if plot_preferences["draw_grid"]:
            self.map.draw_grid(grid_spacing=10 * u.deg, axes=ax)


class CompositeMapViewerController(AbstractMPLController):
    content_type = DataType.MAP_CUBE

    def __init__(self, parent, paths):
        self.comp_map = sunpy.map.Map(paths, cube=True)
        self.view = CompositeMapViewer(parent, self.comp_map)

        AbstractMPLController.__init__(self)

    def getContent(self):
        return self.comp_map

    def setContent(self, data):
        self.comp_map = data
        self.view.comp_map = data

    def getView(self):
        return self.view

    def getTitle(self):
        return "Composite Map"


class CompositeMapViewer(PlotPanel):

    def __init__(self, parent, comp_map):
        self.comp_map = comp_map
        PlotPanel.__init__(self, parent)

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


class TimeSeriesViewerController(AbstractMPLController):
    content_type = DataType.SERIES

    def __init__(self, parent, series):
        self.series = series
        self.view = TimeSeriesViewer(parent, series)

        AbstractMPLController.__init__(self)

    def getContent(self):
        return self.series

    def setContent(self, data):
        self.series = data
        self.view.series = data

    def getView(self):
        return self.view

    def getTitle(self):
        return "{} ({:%Y-%m-%d %H:%M:%S})".format(self.series.source.upper(), self.series.time_range.start)


class TimeSeriesViewer(PlotPanel):

    def __init__(self, parent, time_series):
        self.series = time_series
        PlotPanel.__init__(self, parent)

    def draw(self):
        ax = self.figure.gca()
        self.series.plot(axes=ax)
