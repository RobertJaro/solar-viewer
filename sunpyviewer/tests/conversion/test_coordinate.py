import unittest
from unittest.mock import Mock

from astropy import units as u

from sunpyviewer.conversion.coordinate import extractCoordinates


class TestCoordinates(unittest.TestCase):

    def test_extractCoordinates(self):
        coord = Mock()
        coord.Tx = 3 * u.deg
        coord.Ty = 4 * u.deg
        map_mock = Mock()
        map_mock.pixel_to_world.return_value = coord

        event_mock = Mock()
        event_mock.xdata = 0.4
        event_mock.ydata = 0.6

        x, y, tx, ty = extractCoordinates(map_mock, event_mock)
        self.assertEqual(x, 0)
        self.assertEqual(y, 1)
        self.assertEqual(tx, 3)
        self.assertEqual(ty, 4)
