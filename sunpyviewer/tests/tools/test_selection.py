import tempfile
import unittest
from unittest.mock import Mock

from astropy import units as u

from sunpyviewer.tools.selection import SelectionController


class TestSelection(unittest.TestCase):
    import_export_str = "# x_pixel;y_pixel;x;y;resources\n1.0 pix;2.0 pix;10.1 arcsec;10.2 arcsec;100.1\n3.0 pix;4.0 pix;20.1 arcsec;20.2 arcsec;200.2\n"
    import_export_data = [[1 * u.pix, 2 * u.pix, 10.1 * u.arcsec, 10.2 * u.arcsec, 100.1],
                          [3 * u.pix, 4 * u.pix, 20.1 * u.arcsec, 20.2 * u.arcsec, 200.2]]

    def setUp(self):
        self.ctrl = SelectionController()
        self.model_mock = Mock()
        self.view_mock = Mock()
        self.ctrl.model = self.model_mock
        self.ctrl.view = self.view_mock
        self.ctrl._drawPoints = Mock()
        self.model_mock.fig_points = []

    def test_closeView(self):
        self.ctrl.connection_id = 1

        cursor_mock = Mock()
        self.ctrl.cursor = cursor_mock

        self.ctrl.closeView()

        self.assertIsNone(self.ctrl.cursor)
        self.model_mock.getCanvas().mpl_disconnect.assert_called_once_with(1)
        self.assertIsNone(self.ctrl.view)

    def test_onExport(self):
        self.model_mock.points = self.import_export_data

        new_file, filename = tempfile.mkstemp()

        self.ctrl.onExport(filename)

        self.assertEqual(open(filename).read(), self.import_export_str)

    def test_onImport(self):
        new_file, filename = tempfile.mkstemp()
        open(filename, "w").write(self.import_export_str)

        self.ctrl.onImport(filename)

        self.assertEqual(self.model_mock.points, self.import_export_data)
