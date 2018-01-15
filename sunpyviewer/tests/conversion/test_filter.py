import unittest

from sunpyviewer.conversion.filter import butter2d_lp, butter2d_hp, butter2d_bp


class TestFilter(unittest.TestCase):

    def test_butter2d_lp(self):
        shape = (5, 5)
        filter = butter2d_lp(shape, 0.2)
        self.assertEqual(filter[2, 2], 1)
        self.assertAlmostEqual(filter[0, 0], 0, delta=0.01)

    def test_butter2d_hp(self):
        shape = (5, 5)
        filter = butter2d_hp(shape, 1)
        self.assertEqual(filter[2, 2], 0)
        self.assertAlmostEqual(filter[0, 0], 1, delta=0.01)

    def test_butter2d_bp(self):
        shape = (5, 5)
        filter = butter2d_bp(shape, 0.2, 1)
        self.assertEqual(filter[2, 2], 0)
        self.assertAlmostEqual(filter[0, 0], 0, delta=0.01)
