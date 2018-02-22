import unittest
from unittest.mock import Mock

from astropy import units as u

from sunpyviewer.dialogs.cmap import CmapController
from sunpyviewer.dialogs.rotate import RotateController
from sunpyviewer.viewer.content import DataType


class TestDialogs(unittest.TestCase):

    def test_cmap(self):
        map_mock = Mock()
        map_mock.plot_settings = {"cmap": "TEST_CMAP"}

        controller = CmapController()
        controller.cmap_combo = Mock()
        controller.cmap_combo.GetValue = lambda: "CHANGED_CMAP"
        data = controller.modifyData(map_mock, DataType.MAP)
        self.assertEqual(map_mock.plot_settings["cmap"], "CHANGED_CMAP")

    def test_rotate(self):
        map_mock = Mock()
        map_mock.rotate = Mock()

        controller = RotateController()
        controller.angle_spin = Mock()
        controller.angle_spin.GetValue = lambda: str(10)
        data = controller.modifyData(map_mock, DataType.MAP)
        map_mock.rotate.assert_called_once_with(angle=10 * u.deg)
