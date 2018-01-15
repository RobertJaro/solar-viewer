import unittest
from unittest.mock import Mock

import wx
from astropy import units as u
from matplotlib.colors import PowerNorm, Normalize
from wx.lib.pubsub import pub

from sunpyviewer.dialogs.cmap import CmapDialog
from sunpyviewer.dialogs.norm import NormDialog
from sunpyviewer.dialogs.rotate import RotateDialog
from sunpyviewer.viewer import EVT_CHANGE_TAB


class TestDialogs(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()

    def tearDown(self):
        self.app.MainLoop()

    def test_cmap(self):
        tab_id = 0
        map_mock = Mock()
        map_mock.plot_settings = {"cmap": "TEST_CMAP"}
        event_mock = Mock()

        self.event_send = False

        def changeTab(tab_id, data):
            self.event_send = True

        pub.subscribe(changeTab, EVT_CHANGE_TAB)

        cmap_dlg = CmapDialog(None, tab_id, map_mock)
        cmap_dlg.cmap_combo.SetValue("CHANGED_CMAP")
        cmap_dlg.onOk(event_mock)
        self.assertEqual(map_mock.plot_settings["cmap"], "CHANGED_CMAP")
        self.assertTrue(self.event_send)
        cmap_dlg.Destroy()

    def test_norm(self):
        tab_id = 0
        map_mock = Mock()
        map_mock.plot_settings = {"norm": Normalize()}
        event_mock = Mock()

        self.event_send = False

        def changeTab(tab_id, data):
            self.event_send = True

        pub.subscribe(changeTab, EVT_CHANGE_TAB)

        dlg = NormDialog(None, tab_id, map_mock)
        dlg.norm_combo.SetStringSelection("power norm")
        dlg.power_spin.SetValue(str(5))
        dlg.onOk(event_mock)
        self.assertIsInstance(map_mock.plot_settings["norm"], PowerNorm)
        self.assertEqual(map_mock.plot_settings["norm"].gamma, 5)
        self.assertTrue(self.event_send)
        dlg.Destroy()

    def test_rotate(self):
        tab_id = 0
        map_mock = Mock()
        map_mock.rotate = Mock()
        event_mock = Mock()

        self.event_send = False

        def changeTab(tab_id, data):
            self.event_send = True

        pub.subscribe(changeTab, EVT_CHANGE_TAB)

        dlg = RotateDialog(None, tab_id, map_mock)
        dlg.angle_spin.SetValue(str(10))
        dlg.onOk(event_mock)
        self.assertTrue(self.event_send)
        map_mock.rotate.assert_called_once_with(angle=10 * u.deg)
        dlg.Destroy()
