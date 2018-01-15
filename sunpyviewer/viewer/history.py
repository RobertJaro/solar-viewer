import copy

from wx.lib.pubsub import pub

from sunpyviewer.viewer import EVT_TAB_ADDED, EVT_TAB_CHANGED


class History:
    tabs = {}
    skip_next_change = False

    def __init__(self):
        pub.subscribe(self.onTabAdded, EVT_TAB_ADDED)
        pub.subscribe(self.onTabChanged, EVT_TAB_CHANGED)

    def undo(self, id):
        history = self.tabs[id]
        if len(history) <= 1:
            return None
        del history[-1]
        # change event will be triggered by undo
        self.skip_next_change = True
        return copy.deepcopy(history[-1])

    def onTabAdded(self, tab_id, data):
        self.tabs[tab_id] = [copy.deepcopy(data)]

    def onTabChanged(self, tab_id, data):
        if self.skip_next_change:
            self.skip_next_change = False
            return
        history = self.tabs[tab_id]
        if (len(history) > 10):
            del history[0]
        history.append(copy.deepcopy(data))
