import unittest

from wx.lib.pubsub import pub

from sunpyviewer.viewer import EVT_TAB_ADDED, EVT_TAB_CHANGED, EVT_MAP_CHANGED
from sunpyviewer.viewer.history import History


class TestHistory(unittest.TestCase):

    def setUp(self):
        self.history = History()

    def test_history(self):
        mock_tab_1 = "tab 1"
        mock_tab_2 = "tab 2"
        mock_tab_3 = "tab 3"
        mock_tab_4 = "tab 4"

        pub.sendMessage(EVT_TAB_ADDED, tab_id=0, data=mock_tab_1)
        self.assertEqual(len(self.history.tabs), 1)

        pub.sendMessage(EVT_TAB_ADDED, tab_id=1, data=mock_tab_2)
        self.assertEqual(len(self.history.tabs), 2)

        pub.sendMessage(EVT_TAB_CHANGED, tab_id=0, data=mock_tab_3)
        self.assertEqual(self.history.tabs[0][-1], mock_tab_3)

        pub.sendMessage(EVT_MAP_CHANGED, tab_id=1, data=mock_tab_4)
        self.assertEqual(self.history.tabs[1][-1], mock_tab_4)

        undo_tab = self.history.undo(1)
        self.assertEqual(mock_tab_2, undo_tab)

        # assert next event skipped
        pub.sendMessage(EVT_MAP_CHANGED, tab_id=1, data=mock_tab_4)
        self.assertEqual(self.history.tabs[1][-1], mock_tab_2)
        self.assertEqual(self.history.tabs[0][0], mock_tab_1)
        self.assertEqual(self.history.tabs[0][1], mock_tab_3)
