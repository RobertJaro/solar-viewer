from qtpy import QtWidgets

from solarviewer.config.base import FileType


class InitUtil:

    @staticmethod
    def getAction(tree, parent, checkable=False):
        for i, name in enumerate(tree):
            if i == len(tree) - 1:
                action = InitUtil._getAction(name, parent, checkable)
                return action
            else:
                parent = InitUtil._getSubMenu(name, parent)

    @staticmethod
    def _getSubMenu(name, parent):
        for c in parent.children():
            if isinstance(c, QtWidgets.QMenu) and c.title() == name:
                return c
        return parent.addMenu(name)

    @staticmethod
    def _getAction(name, parent, checkable):
        for a in parent.actions():
            if a.text() == name:
                return a
        a = QtWidgets.QAction(name, parent)
        a.setCheckable(checkable)
        parent.addAction(a)
        return a


def supported(data_type, viewer_type, supported_types, supported_viewers):
    from solarviewer.config.base import DataType, ViewerType
    if ViewerType.NONE in supported_viewers or len(supported_viewers) == 0:
        return True
    if data_type is None or viewer_type is None:
        return False
    types = [str(t) for t in supported_types]
    viewers = [str(t) for t in supported_viewers]

    return (str(DataType.ANY) in types or str(data_type) in types) and (
            str(ViewerType.ANY) in viewers or str(viewer_type) in viewers)


def saveFits(s_map):
    f = getattr(s_map, "path", None)
    name, _ = QtWidgets.QFileDialog.getSaveFileName(directory=f, filter=getExtensionString(FileType.FITS.value))
    if name:
        s_map.save(name, overwrite=True)


def getExtensionString(file_types):
    files = []
    for f, t in file_types.items():
        types = " ".join(["*." + str(type) + "" for type in t])
        type = f + " (" + types + ")"
        files.append(type)
    return " ".join(files)
