import logging
import os

import sunpy.map
import sunpy.timeseries
import wx
from sunpy.image.coalignment import mapcube_coalign_by_match_template
from sunpy.physics.solar_rotation import mapcube_solar_derotate
from wx import aui
from wx.lib.pubsub import pub

from sunpyviewer.download.data_viewer import DataViewer
from sunpyviewer.download.download import QueryPanel, QueryResultNotebook
from sunpyviewer.download.event_download import HEKPanel
from sunpyviewer.tools import EVT_QUERY_STARTED, EVT_QUERY_RESULT
from sunpyviewer.util.data import resources_dir
from sunpyviewer.util.default_action import ActionController
from sunpyviewer.util.default_dialog import DialogController
from sunpyviewer.util.default_tool import ToolController
from sunpyviewer.util.event import getOpenEvent, isSupported
from sunpyviewer.viewer import EVT_STATUS_BAR_UPDATE, EVT_TAB_SELECTION_CHANGED, EVT_CHANGE_PLOT_PREFERENCE, \
    EVT_MPL_CHANGE_MODE
from sunpyviewer.viewer.content import ContentController, ViewMode, AbstractViewerController
from sunpyviewer.viewer.history import History
from sunpyviewer.viewer.settings import DBDialog
from sunpyviewer.viewer.toolbar import ToolbarController


class MainFrame(wx.Frame):
    query_result_notebook = None

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "SunPy - Viewer")
        self.setIcon()

        self.toolbar_ctrl = ToolbarController(self)
        self.content_ctrl = ContentController(self)

        self.createStatusBar()
        self.manager = self.initManager()
        self.history = History()
        self.createMenuBar()
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
        menu_bar = wx.MenuBar()

        # File
        file_menu = wx.Menu()
        menu_bar.Append(file_menu, "&File")
        # Add Tab Items
        self.addViewerMenuItems(file_menu, menu_bar)

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
        menu_bar.Append(edit_menu, "&Edit")
        undo_item = edit_menu.Append(wx.NewId(), "Undo")
        edit_menu.AppendSeparator()

        # View
        view_menu = wx.Menu()
        menu_bar.Append(view_menu, "&View")
        self.toolbar_item = view_menu.AppendCheckItem(wx.ID_ANY, "Toolbar")
        self.toolbar_item.Check()
        colorbar_item = view_menu.AppendCheckItem(wx.ID_ANY, "Show Colorbar")
        limb_item = view_menu.AppendCheckItem(wx.ID_ANY, "Draw Limb")
        contours_item = view_menu.AppendCheckItem(wx.ID_ANY, "Draw Contours")
        grid_item = view_menu.AppendCheckItem(wx.ID_ANY, "Draw Grid")

        # Tools
        tool_menu = wx.Menu()
        menu_bar.Append(tool_menu, "&Tools")

        # Help
        help_menu = wx.Menu()
        menu_bar.Append(help_menu, "&Help")

        # Load Dynamic Items
        self.content_aware_items = {}
        self.tool_items = {}
        self.active_tools = {}  # used for toggle
        self.addTools(menu_bar)
        self.addDialogs(menu_bar)
        self.addActions(menu_bar)

        menu_bar.Bind(wx.EVT_MENU, self.onSaveImage, save_image_item)
        menu_bar.Bind(wx.EVT_MENU, self.onSaveFits, save_fits_item)
        menu_bar.Bind(wx.EVT_MENU, self.onExit, exit_item)
        menu_bar.Bind(wx.EVT_MENU, self.onToggleToolbar, self.toolbar_item)
        menu_bar.Bind(wx.EVT_MENU, self.onUndo, undo_item)
        menu_bar.Bind(wx.EVT_MENU, self.onDBSettings, db_settings_item)
        menu_bar.Bind(wx.EVT_MENU, self.onStartDownloader, fido_item)
        menu_bar.Bind(wx.EVT_MENU, self.onDataManager, data_item)
        menu_bar.Bind(wx.EVT_MENU, self.onHEK, hek_item)
        menu_bar.Bind(wx.EVT_MENU, self.onColorbar, colorbar_item)
        menu_bar.Bind(wx.EVT_MENU, self.onLimb, limb_item)
        menu_bar.Bind(wx.EVT_MENU, self.onContours, contours_item)
        menu_bar.Bind(wx.EVT_MENU, self.onGrid, grid_item)

        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('Z'), undo_item.GetId())])
        self.SetAcceleratorTable(accel_tbl)

        self.onTabChange(None)
        pub.subscribe(self.onTabChange, EVT_TAB_SELECTION_CHANGED)

        self.SetMenuBar(menu_bar)

    def addTools(self, menu_bar):
        __import__("sunpyviewer.tools", globals(), locals(), ['*'])
        dict = self.getItemTree(ToolController)
        return self.addToolItems(menu_bar, dict)

    def addDialogs(self, menu_bar):
        __import__("sunpyviewer.dialogs", globals(), locals(), ['*'])
        dict = self.getItemTree(DialogController)
        return self.addDialogItems(menu_bar, dict)

    def addActions(self, menu_bar):
        __import__("sunpyviewer.viewer.actions", globals(), locals(), ['*'])
        dict = self.getItemTree(ActionController)
        return self.addActionItems(menu_bar, dict)

    def getItemTree(self, super_class):
        items = super_class.__subclasses__()
        dict = {}
        for item in items:
            tree = item.getItemConfig().menu_path.split("\\")
            parent_dict = dict
            for i, node in enumerate(tree):
                if i + 1 == len(tree):
                    parent_dict.setdefault(node, item)
                    continue
                sub_dict = {}
                parent_dict = parent_dict.setdefault(node, sub_dict)
        return dict

    def addToolItems(self, parent, tree):
        for k, v in tree.items():
            if not isinstance(v, dict):
                item = parent.AppendCheckItem(wx.ID_ANY, k)
                tool_ctrl = v()
                parent.Bind(wx.EVT_MENU, lambda e, ctrl=tool_ctrl: self.onToggleTool(ctrl), item)
                self.tool_items[tool_ctrl] = item
                continue
            menus = [menu[1] for menu in parent.Menus]
            if k in menus:
                index = menus.index(k)
                sub_menu = parent.Menus[index][0]
            else:
                sub_menu = wx.Menu()
                parent.Append(sub_menu, k)
            self.addToolItems(sub_menu, v)

    def addDialogItems(self, parent, tree):
        for k, v in tree.items():
            if not isinstance(v, dict):
                item = parent.Append(wx.ID_ANY, k)
                dlg_ctrl = v()
                parent.Bind(wx.EVT_MENU, lambda e, ctrl=dlg_ctrl: self.onOpenDialog(self, ctrl), item)
                self.content_aware_items[dlg_ctrl] = item
                continue
            if isinstance(parent, wx.MenuBar) and k in [menu[1] for menu in parent.Menus]:
                index = [menu[1] for menu in parent.Menus].index(k)
                sub_menu = parent.Menus[index][0]
            else:
                sub_menu = wx.Menu()
                parent.Append(wx.ID_ANY, k, sub_menu)
            self.addDialogItems(sub_menu, v)

    def addActionItems(self, parent, tree):
        for k, v in tree.items():
            if not isinstance(v, dict):
                item = parent.Append(wx.ID_ANY, k)
                action_ctrl = v()
                parent.Bind(wx.EVT_MENU, lambda e, ctrl=action_ctrl: self.onAction(ctrl), item)
                self.content_aware_items[action_ctrl] = item
                continue
            if isinstance(parent, wx.MenuBar) and k in [menu[1] for menu in parent.Menus]:
                index = [menu[1] for menu in parent.Menus].index(k)
                sub_menu = parent.Menus[index][0]
            else:
                sub_menu = wx.Menu()
                parent.Append(wx.ID_ANY, k, sub_menu)
            self.addActionItems(sub_menu, v)

    def addViewerMenuItems(self, file_menu, menubar):
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

    def onToggleTool(self, tool_ctrl):
        if tool_ctrl.view is None:
            viewer_ctrl = self.content_ctrl.getActiveController()
            if not isSupported(tool_ctrl, viewer_ctrl):
                viewer_ctrl = None
            view = tool_ctrl.createView(self, viewer_ctrl)
            self._addToolPane(view, tool_ctrl.getItemConfig().title)
            self.active_tools[view] = tool_ctrl
        else:
            self._removeToolPane(tool_ctrl.view)
            tool_ctrl.closeView()

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

    def onTabChange(self, ctrl):
        for k, v in self.content_aware_items.items():
            if isSupported(k, ctrl):
                v.Enable()
            else:
                v.Enable(False)

    def onPaneClose(self, event):
        if event.Pane.window not in self.active_tools.keys():
            return
        ctrl = self.active_tools[event.Pane.window]
        ctrl.closeView()
        self.tool_items[ctrl].Check(False)

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

    def onOpenDialog(self, parent, ctrl):
        ctrl.openDialog(parent, self.content_ctrl.getActiveController())

    def onAction(self, ctrl):
        ctrl.doAction(self.content_ctrl.getActiveController())

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
