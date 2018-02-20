import logging
import os

import numpy as np
import sunpy.map
import sunpy.timeseries
import wx
from sunpy.image.coalignment import mapcube_coalign_by_match_template
from sunpy.physics.solar_rotation import mapcube_solar_derotate
from wx import aui
from wx.lib.pubsub import pub

from sunpyviewer.dialogs.cmap import CmapDialog
from sunpyviewer.dialogs.denoise import TVDenoiseDialog, BilateralDenoiseDialog, WaveletDenoiseDialog
from sunpyviewer.dialogs.norm import NormDialog
from sunpyviewer.dialogs.rotate import RotateDialog
from sunpyviewer.tools import EVT_QUERY_STARTED, EVT_QUERY_RESULT
from sunpyviewer.tools.contrast import ContrastPanel, ContrastController
from sunpyviewer.tools.data_viewer import DataViewer
from sunpyviewer.tools.download import QueryPanel, QueryResultNotebook
from sunpyviewer.tools.event_download import HEKPanel
from sunpyviewer.tools.fft import FFTPanel, FFTController
from sunpyviewer.tools.profile import ProfilePanel, ProfileController
from sunpyviewer.tools.selection import SelectionPanel, SelectionController
from sunpyviewer.tools.value_adjustment import ValueAdjustmentPanel, ValueAdjustmentController
from sunpyviewer.tools.wavelet import WaveletPanel, WaveletController
from sunpyviewer.util.data import resources_dir
from sunpyviewer.util.event import getOpenEvent
from sunpyviewer.viewer import EVT_STATUS_BAR_UPDATE, EVT_TAB_SELECTION_CHANGED, EVT_CHANGE_PLOT_PREFERENCE, \
    EVT_MPL_CHANGE_MODE
from sunpyviewer.viewer.composite import CompositeDialog
from sunpyviewer.viewer.content import MapViewerController, CompositeMapViewerController, TimeSeriesViewerController, \
    ContentController, ViewMode, AbstractViewerController
from sunpyviewer.viewer.history import History
from sunpyviewer.viewer.settings import DBDialog
from sunpyviewer.viewer.toolbar import ToolbarController


class MainFrame(wx.Frame):
    query_result_notebook = None

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "SunPy - Viewer")
        self.setIcon()
        self.createMenuBar()

        self.toolbar_ctrl = ToolbarController(self)
        self.content_ctrl = ContentController(self)
        self.profile_ctrl = ProfileController()
        self.selection_ctrl = SelectionController()
        self.contrast_ctrl = ContrastController()
        self.fft_ctrl = FFTController()
        self.value_ctrl = ValueAdjustmentController()
        self.wavelet_ctrl = WaveletController()

        self.createStatusBar()
        self.manager = self.initManager()
        self.history = History()
        wx.CallLater(100, self.addContentPane)  # Workaround

    def addContentPane(self):
        screen_w, screen_h = wx.DisplaySize()
        self.manager.AddPane(self.content_ctrl.getView(),
                             aui.AuiPaneInfo().CloseButton(False).Floatable(True).MaximizeButton(True).Center())
        self.manager.AddPane(self.toolbar_ctrl.getView(),
                             aui.AuiPaneInfo().FloatingPosition(screen_w - 100, 100).CloseButton(False).Dockable(
                                 False).Resizable(
                                 False).Float())
        self.manager.Update()

    def initManager(self):
        manager = aui.AuiManager(self)
        manager.Bind(aui.EVT_AUI_PANE_CLOSE, self.onPaneClose)
        return manager

    def createStatusBar(self):
        status_bar = wx.StatusBar(self, -1)
        self.SetStatusBar(status_bar)
        pub.subscribe(self.onUpdateStatusBar, EVT_STATUS_BAR_UPDATE)

    def setIcon(self):
        icon = wx.Icon()
        icon.LoadFile(os.path.join(resources_dir, "icon.png"))
        self.SetIcon(icon)

    def createMenuBar(self):
        menubar = wx.MenuBar()

        # File
        file_menu = wx.Menu()
        # Add Tab Items
        self.addTabMenuItems(file_menu, menubar)

        save_image_item = file_menu.Append(wx.ID_ANY, "Save Image")
        save_fits_item = file_menu.Append(wx.ID_ANY, "Save as fits")
        file_menu.AppendSeparator()
        data_item = file_menu.Append(wx.ID_ANY, "Data Manager")
        fido_item = file_menu.Append(wx.ID_ANY, "Download Data")
        hek_item = file_menu.Append(wx.ID_ANY, "Download from HEK")
        db_settings_item = file_menu.Append(wx.ID_ANY, "Change DB Settings")
        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT)

        # Edit
        edit_menu = wx.Menu()
        undo_item = edit_menu.Append(wx.NewId(), "Undo")
        edit_menu.AppendSeparator()
        cmap_item = edit_menu.Append(wx.ID_ANY, "Change Colormap")
        norm_item = edit_menu.Append(wx.ID_ANY, "Change Norm")
        denoise_submenu = wx.Menu()
        tv_item = denoise_submenu.Append(wx.ID_ANY, "TV Chambolle")
        bilateral_item = denoise_submenu.Append(wx.ID_ANY, "Bilateral")
        wavelet_denoise_item = denoise_submenu.Append(wx.ID_ANY, "Wavelet")
        edit_menu.Append(wx.ID_ANY, "Denoise", denoise_submenu)
        rotate_item = edit_menu.Append(wx.ID_ANY, "Rotate")
        cut_item = edit_menu.Append(wx.ID_ANY, "Cut To Current View")
        comp_submenu = wx.Menu()
        alpha_item = comp_submenu.Append(wx.ID_ANY, "Adjust Alpha")
        derotate_item = comp_submenu.Append(wx.ID_ANY, "Derotate")
        coalign_item = comp_submenu.Append(wx.ID_ANY, "Coalign")
        edit_menu.Append(wx.ID_ANY, "Composite Map Options", comp_submenu)

        # View
        view_menu = wx.Menu()
        self.toolbar_item = view_menu.AppendCheckItem(wx.ID_ANY, "Toolbar")
        self.toolbar_item.Check()
        colorbar_item = view_menu.AppendCheckItem(wx.ID_ANY, "Show Colorbar")
        limb_item = view_menu.AppendCheckItem(wx.ID_ANY, "Draw Limb")
        contours_item = view_menu.AppendCheckItem(wx.ID_ANY, "Draw Contours")
        grid_item = view_menu.AppendCheckItem(wx.ID_ANY, "Draw Grid")

        # Tools
        tools_menu = wx.Menu()
        self.contrast_item = tools_menu.AppendCheckItem(wx.ID_ANY, "Modify Contrast")
        self.value_item = tools_menu.AppendCheckItem(wx.ID_ANY, "Adjust Values")
        self.profile_item = tools_menu.AppendCheckItem(wx.ID_ANY, "Profile Analysis")
        self.selection_item = tools_menu.AppendCheckItem(wx.ID_ANY, "Highlight Values")
        self.fft_item = tools_menu.AppendCheckItem(wx.ID_ANY, "FFT")
        self.wavelet_item = tools_menu.AppendCheckItem(wx.ID_ANY, "Wavelet Filter")

        # Help
        help_menu = wx.Menu()
        snr_item = help_menu.Append(wx.ID_ANY, "Calculate Signal to Noise Ratio")

        self.general_items = [data_item, fido_item, hek_item,
                              db_settings_item, exit_item, self.toolbar_item, undo_item, colorbar_item]
        self.map_items = [save_image_item, save_fits_item, cmap_item, norm_item, tv_item, bilateral_item,
                          wavelet_denoise_item, rotate_item, snr_item, cut_item]
        self.map_cube_items = [alpha_item, derotate_item, coalign_item]
        self.map_tool_items = [self.contrast_item, self.value_item, self.profile_item, self.selection_item,
                               self.fft_item, self.wavelet_item]
        self.series_items = [save_image_item, save_fits_item]

        menubar.Append(file_menu, "&File")
        menubar.Append(edit_menu, "&Edit")
        menubar.Append(view_menu, "&View")
        menubar.Append(tools_menu, "&Tools")
        menubar.Append(help_menu, "&Help")

        menubar.Bind(wx.EVT_MENU, self.onSaveImage, save_image_item)
        menubar.Bind(wx.EVT_MENU, self.onSaveFits, save_fits_item)
        menubar.Bind(wx.EVT_MENU, self.onExit, exit_item)
        menubar.Bind(wx.EVT_MENU, self.onToggleToolbar, self.toolbar_item)
        menubar.Bind(wx.EVT_MENU, self.onToggleProfile, self.profile_item)
        menubar.Bind(wx.EVT_MENU, self.onToggleSelection, self.selection_item)
        menubar.Bind(wx.EVT_MENU, self.onToggleFFT, self.fft_item)
        menubar.Bind(wx.EVT_MENU, self.onChangeCmap, cmap_item)
        menubar.Bind(wx.EVT_MENU, self.onUndo, undo_item)
        menubar.Bind(wx.EVT_MENU, self.onToggleContrast, self.contrast_item)
        menubar.Bind(wx.EVT_MENU, self.onToggleValueAdjust, self.value_item)
        menubar.Bind(wx.EVT_MENU, self.onChangeNorm, norm_item)
        menubar.Bind(wx.EVT_MENU, self.onDenoiseTV, tv_item)
        menubar.Bind(wx.EVT_MENU, self.onDenoiseBilateral, bilateral_item)
        menubar.Bind(wx.EVT_MENU, self.onDenoiseWavelet, wavelet_denoise_item)
        menubar.Bind(wx.EVT_MENU, self.onToggleWavelet, self.wavelet_item)
        menubar.Bind(wx.EVT_MENU, self.onDBSettings, db_settings_item)
        menubar.Bind(wx.EVT_MENU, self.onStartDownloader, fido_item)
        menubar.Bind(wx.EVT_MENU, self.onDataManager, data_item)
        menubar.Bind(wx.EVT_MENU, self.onHEK, hek_item)
        menubar.Bind(wx.EVT_MENU, self.onColorbar, colorbar_item)
        menubar.Bind(wx.EVT_MENU, self.onLimb, limb_item)
        menubar.Bind(wx.EVT_MENU, self.onContours, contours_item)
        menubar.Bind(wx.EVT_MENU, self.onGrid, grid_item)
        menubar.Bind(wx.EVT_MENU, self.onRotate, rotate_item)
        menubar.Bind(wx.EVT_MENU, self.onCut, cut_item)
        menubar.Bind(wx.EVT_MENU, self.onAdjustAlpha, alpha_item)
        menubar.Bind(wx.EVT_MENU, self.onDerotateCube, derotate_item)
        menubar.Bind(wx.EVT_MENU, self.onCoalign, coalign_item)
        menubar.Bind(wx.EVT_MENU, self.onSNR, snr_item)

        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('Z'), undo_item.GetId())])
        self.SetAcceleratorTable(accel_tbl)

        self.disableAllMenuItems()
        pub.subscribe(self.onTabChange, EVT_TAB_SELECTION_CHANGED)

        self.SetMenuBar(menubar)

    def addTabMenuItems(self, file_menu, menubar):
        tab_ctrls = AbstractViewerController.__subclasses__()
        open_dict = {}
        for ctrl in tab_ctrls:
            open_dict.setdefault(ctrl.data_type, []).append(ctrl)
        self.open_functions = []
        for k, ctrls in open_dict.items():
            data_type_menu = wx.Menu()
            file_menu.Append(wx.ID_ANY, "Open " + k.value + " with", data_type_menu)
            for c in ctrls:
                menu_item = data_type_menu.Append(wx.ID_ANY, c.viewer_type.value)
                menubar.Bind(wx.EVT_MENU, lambda e, ctrl=c: self.onSelectAndOpen(ctrl), menu_item)
                func = lambda path, ctrl=c: self.onOpen(ctrl, path)
                self.open_functions.append(func)  # Workaround
                pub.subscribe(func, getOpenEvent(c.data_type, c.viewer_type))

    def onTabChange(self, ctrl):
        self.disableAllMenuItems()

        enable = []
        if isinstance(ctrl, MapViewerController):
            enable.extend(self.map_items)
        if isinstance(ctrl, TimeSeriesViewerController):
            enable.extend(self.series_items)
        if isinstance(ctrl, CompositeMapViewerController):
            enable.extend(self.map_cube_items)

        for item in enable:
            item.Enable(True)

    def disableAllMenuItems(self):
        for item in (self.map_items + self.series_items + self.map_cube_items):
            item.Enable(False)

    def onPaneClose(self, event):
        if isinstance(event.Pane.window, ProfilePanel):
            self.profile_ctrl.closeView()
            self.profile_item.Check(False)
        if isinstance(event.Pane.window, SelectionPanel):
            self.selection_ctrl.closeView()
            self.selection_item.Check(False)
        if isinstance(event.Pane.window, FFTPanel):
            self.fft_ctrl.closeView()
            self.fft_item.Check(False)
        if isinstance(event.Pane.window, ContrastPanel):
            self.contrast_ctrl.closeView()
            self.contrast_item.Check(False)
        if isinstance(event.Pane.window, ValueAdjustmentPanel):
            self.value_ctrl.closeView()
            self.value_item.Check(False)
        if isinstance(event.Pane.window, WaveletPanel):
            self.wavelet_ctrl.closeView()
            self.wavelet_item.Check(False)

    def onUpdateStatusBar(self, x, y):
        text = "x={0:.5f} ; y={1:.5f}".format(x, y)
        self.GetStatusBar().SetStatusText(text, 0)

    def onSelectAndOpen(self, ctrl_class):
        multiple = ctrl_class.file_configuration["multiple"]
        if multiple:
            dlg = wx.FileDialog(self, "Open Files", "", "", ctrl_class.file_configuration["extensions"],
                                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
            if dlg.ShowModal() == wx.ID_CANCEL:
                return
            path = dlg.GetPaths()
        else:
            dlg = wx.FileDialog(self, "Open Files", "", "", ctrl_class.file_configuration["extensions"],
                                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if dlg.ShowModal() == wx.ID_CANCEL:
                return
            path = dlg.GetPath()
        self.onOpen(ctrl_class, path)

    def onOpen(self, ctrl_class, path):
        try:
            controller = ctrl_class(self, path)
            self.content_ctrl.openViewerController(controller)
        except Exception as ex:
            logging.exception(ex)
            self.handleFileOpenError(ex, path)

    def handleFileOpenError(self, ex, path):
        error_msg = "Error during opening: {} \nCaused by: {}".format(path, str(ex))
        dlg = wx.MessageDialog(self, error_msg, style=wx.ICON_ERROR)
        dlg.ShowModal()

    def onSaveImage(self, event):
        self.content_ctrl.saveImage()

    def onSaveFits(self, event):
        self.content_ctrl.saveFits()

    def onExit(self, event):
        self.Close(True)

    def onToggleProfile(self, *args):
        if self.profile_ctrl.view is None:
            profile_tool = self.profile_ctrl.createView(self, self.content_ctrl.getActiveController())
            self._addToolPane(profile_tool, "Profile Analysis")
            pub.sendMessage(EVT_MPL_CHANGE_MODE, mode=ViewMode.NONE)
        else:
            self._removeToolPane(self.profile_ctrl.view)
            self.profile_ctrl.closeView()

    def onToggleSelection(self, *args):
        if self.selection_ctrl.view is None:
            selection_tool = self.selection_ctrl.createView(self, self.content_ctrl.getActivePage())
            self._addToolPane(selection_tool, "Value Highlighting")
            pub.sendMessage(EVT_MPL_CHANGE_MODE, mode=ViewMode.NONE)
        else:
            self._removeToolPane(self.selection_ctrl.view)
            self.selection_ctrl.closeView()

    def onToggleFFT(self, *args):
        if self.fft_ctrl.view is None:
            fft_tool = self.fft_ctrl.createView(self, self.content_ctrl)
            self._addToolPane(fft_tool, "FFT - Filter")
        else:
            self._removeToolPane(self.fft_ctrl.view)
            self.fft_ctrl.closeView()

    def onToggleContrast(self, *args):
        if self.contrast_ctrl.view is None:
            contrast_tool = self.contrast_ctrl.createView(self, self.content_ctrl)
            self._addToolPane(contrast_tool, "Contrast Modification")
        else:
            self._removeToolPane(self.contrast_ctrl.view)
            self.contrast_ctrl.closeView()

    def onToggleValueAdjust(self, *args):
        if self.value_ctrl.view is None:
            value_tool = self.value_ctrl.createView(self, self.content_ctrl)
            self._addToolPane(value_tool, "Value Adjustment")
        else:
            self._removeToolPane(self.value_ctrl.view)
            self.value_ctrl.closeView()

    def onToggleWavelet(self, *args):
        if self.wavelet_ctrl.view is None:
            wavelet_tool = self.wavelet_ctrl.createView(self, self.content_ctrl)
            self._addToolPane(wavelet_tool, "Wavelet Analysis")
        else:
            self._removeToolPane(self.wavelet_ctrl.view)
            self.wavelet_ctrl.closeView()

    def _removeToolPane(self, tool):
        self.manager.GetPane(tool).Show(False)
        self.manager.DetachPane(tool)
        tool.Destroy()
        self.manager.Update()

    def _addToolPane(self, panel, name):
        size = panel.GetSize()
        size[0] += 18
        size[1] = 200
        info = aui.AuiPaneInfo().MinSize(size).MaximizeButton(True).DestroyOnClose(True).Name(name).Left()
        self.manager.AddPane(panel, info)
        self.manager.Update()

    def onChangeCmap(self, event):
        dlg = CmapDialog(self, self.content_ctrl.getActiveTabId(), self.content_ctrl.getActiveContent())
        dlg.ShowModal()
        dlg.Destroy()

    def onChangeNorm(self, event):
        dlg = NormDialog(self, self.content_ctrl.getActiveTabId(), self.content_ctrl.getActiveContent())
        dlg.ShowModal()
        dlg.Destroy()

    def onDenoiseTV(self, event):
        dlg = TVDenoiseDialog(self, self.content_ctrl.getActiveTabId(), self.content_ctrl.getActiveContent())
        dlg.ShowModal()
        dlg.Destroy()

    def onDenoiseBilateral(self, event):
        if np.any(self.content_ctrl.getActiveContent().data < 0):
            wx.MessageDialog(self, "Negative Values Encountered").ShowModal()
            return
        dlg = BilateralDenoiseDialog(self, self.content_ctrl.getActiveTabId(), self.content_ctrl.getActiveContent())
        dlg.ShowModal()
        dlg.Destroy()

    def onDenoiseWavelet(self, event):
        dlg = WaveletDenoiseDialog(self, self.content_ctrl.getActiveTabId(), self.content_ctrl.getActiveContent())
        dlg.ShowModal()
        dlg.Destroy()

    def onStartDownloader(self, *args):
        query = QueryPanel(self)
        self._addToolPane(query, "Data Download")
        pub.subscribe(self.onQueryStarted, EVT_QUERY_STARTED)
        pub.subscribe(self.onQueryResult, EVT_QUERY_RESULT)

    def onDataManager(self, *args):
        viewer = DataViewer(self)
        self.manager.AddPane(viewer, wx.LEFT, "Data Manager")
        self.manager.Update()

    def onQueryStarted(self, id, type):
        if self.query_result_notebook is None or not self.query_result_notebook.IsShown():
            self.query_result_notebook = QueryResultNotebook(self)
            self.manager.AddPane(self.query_result_notebook,
                                 aui.AuiPaneInfo().Caption("Query Result").MinSize(wx.Size(250, 250)).Bottom())
            self.manager.Update()
        self.query_result_notebook.addQueryPage(id, type)

    def onQueryResult(self, id, query):
        self.query_result_notebook.addQueryResult(id, query)

    def onDBSettings(self, event):
        DBDialog(self).ShowModal()

    def onHEK(self, event):
        hek = HEKPanel(self)
        self._addToolPane(hek, "HEK Download")
        pub.subscribe(self.onQueryStarted, EVT_QUERY_STARTED)
        pub.subscribe(self.onQueryResult, EVT_QUERY_RESULT)

    def onToggleToolbar(self, *args):
        pane = self.manager.GetPane(self.toolbar_ctrl.getView())
        pane.Show(not pane.IsShown())
        self.manager.Update()

    def onColorbar(self, event):
        pub.sendMessage(EVT_CHANGE_PLOT_PREFERENCE, key="show_colorbar", value=event.Selection)

    def onLimb(self, event):
        pub.sendMessage(EVT_CHANGE_PLOT_PREFERENCE, key="show_limb", value=event.Selection)

    def onContours(self, event):
        pub.sendMessage(EVT_CHANGE_PLOT_PREFERENCE, key="draw_contours", value=event.Selection)

    def onGrid(self, event):
        pub.sendMessage(EVT_CHANGE_PLOT_PREFERENCE, key="draw_grid", value=event.Selection)

    def onUndo(self, event):
        tab_id = self.content_ctrl.getActiveTabId()
        data = self.history.undo(tab_id)
        if data != None:
            self.content_ctrl.setTabContent(tab_id, data)

    def onRotate(self, event):
        dlg = RotateDialog(self, self.content_ctrl.getActiveTabId(), self.content_ctrl.getActiveContent())
        dlg.ShowModal()
        dlg.Destroy()

    def onCut(self, event):
        sub_map = self.content_ctrl.getZoomSubMap()
        self.content_ctrl.setTabContent(self.content_ctrl.getActiveTabId(), sub_map)

    def onAdjustAlpha(self, event):
        dlg = CompositeDialog(self, self.content_ctrl.getActiveTabId(), self.content_ctrl.getActiveContent())
        dlg.ShowModal()
        dlg.Destroy()

    def onDerotateCube(self, event):
        comp_map = self.content_ctrl.getActiveContent()
        mc = sunpy.map.Map(comp_map._maps, cube=True)
        derotated = mapcube_solar_derotate(mc)
        result = sunpy.map.Map(derotated.maps, composite=True)
        self.content_ctrl.setTabContent(self.content_ctrl.getActiveTabId(), result)

    def onCoalign(self, event):
        comp_map = self.content_ctrl.getActiveContent()
        mc = sunpy.map.Map(comp_map._maps, cube=True)
        derotated = mapcube_coalign_by_match_template(mc)
        result = sunpy.map.Map(derotated.maps, composite=True)
        self.content_ctrl.setTabContent(self.content_ctrl.getActiveTabId(), result)

    def onSNR(self, event):
        data = self.content_ctrl.getZoomSubMap().data
        snr = np.mean(data) / np.std(data)
        message = "Estimated SNR: {0:.7}".format(float(snr))
        wx.MessageDialog(self, message).ShowModal()
