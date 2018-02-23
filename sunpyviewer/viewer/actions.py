import numpy as np
import sunpy.map
import wx
from sunpy.image.coalignment import mapcube_coalign_by_match_template
from sunpy.physics.solar_rotation import mapcube_solar_derotate
from wx.lib.pubsub import pub

from sunpyviewer.util.default_action import ActionController
from sunpyviewer.util.default_tool import ItemConfig
from sunpyviewer.viewer import EVT_CHANGE_TAB
from sunpyviewer.viewer.content import ViewerType, DataType


class CutController(ActionController):

    @staticmethod
    def getItemConfig():
        return ItemConfig().setMenuPath("Edit\\Cut To Current View").addSupportedViewer(
            ViewerType.MPL).addSupportedData(DataType.MAP)

    def doAction(self, viewer_ctrl):
        map = viewer_ctrl.getZoomSubMap()
        pub.sendMessage(EVT_CHANGE_TAB, tab_id=viewer_ctrl.getId(), data=map)


class DerotateController(ActionController):

    @staticmethod
    def getItemConfig():
        return ItemConfig().setMenuPath("Edit\\Composite Map\\Derotate").addSupportedViewer(
            ViewerType.ANY).addSupportedData(DataType.MAP_CUBE)

    def doAction(self, viewer_ctrl):
        comp_map = viewer_ctrl.getContent()
        mc = sunpy.map.Map(comp_map._maps, cube=True)
        derotated = mapcube_solar_derotate(mc)
        result = sunpy.map.Map(derotated.maps, composite=True)
        pub.sendMessage(EVT_CHANGE_TAB, tab_id=viewer_ctrl.getId(), data=result)


class CoalignController(ActionController):

    @staticmethod
    def getItemConfig():
        return ItemConfig().setMenuPath("Edit\\Composite Map\\Coalign").addSupportedViewer(
            ViewerType.ANY).addSupportedData(DataType.MAP_CUBE)

    def doAction(self, viewer_ctrl):
        comp_map = viewer_ctrl.getContent()
        mc = sunpy.map.Map(comp_map._maps, cube=True)
        coaligned = mapcube_coalign_by_match_template(mc)
        result = sunpy.map.Map(coaligned.maps, composite=True)
        pub.sendMessage(EVT_CHANGE_TAB, tab_id=viewer_ctrl.getId(), data=result)


class SNRController(ActionController):

    @staticmethod
    def getItemConfig():
        return ItemConfig().setMenuPath("Help\\Calculate SNR").addSupportedViewer(
            ViewerType.MPL).addSupportedData(DataType.MAP)

    def doAction(self, viewer_ctrl):
        data = viewer_ctrl.getZoomSubMap().data
        snr = np.mean(data) / np.std(data)
        message = "Estimated SNR: {0:.7}".format(float(snr))
        wx.MessageDialog(None, message).ShowModal()
