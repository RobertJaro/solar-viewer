from sunpyviewer.viewer.content import DataType, ViewerType


def getOpenEvent(data_type, viewer_type):
    return data_type.name + "." + viewer_type.name + ".open"


def getOKEvent(id):
    return str(id) + ".ok"


def getPreviewEvent(id):
    return str(id) + ".preview"


def isSupported(item_ctrl, viewer_ctrl):
    if ViewerType.ANY in item_ctrl.getItemConfig().supported_viewer_types and DataType.ANY in item_ctrl.getItemConfig().supported_data_types:
        return True
    if viewer_ctrl is None:
        return False
    data_type_supported = viewer_ctrl.data_type in item_ctrl.getItemConfig().supported_data_types or DataType.ANY in item_ctrl.getItemConfig().supported_data_types
    viewer_type_supported = viewer_ctrl.viewer_type in item_ctrl.getItemConfig().supported_viewer_types or ViewerType.ANY in item_ctrl.getItemConfig().supported_viewer_types
    return data_type_supported and viewer_type_supported
