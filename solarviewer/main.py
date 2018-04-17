import sys
from inspect import isabstract

from PyQt5.QtCore import QLocale
from qtpy import QtWidgets

from solarviewer.app.app import AppController
from solarviewer.config import viewers_name
from solarviewer.config.base import ViewerController, Controller
from solarviewer.config.ioc import features


def addExceptionHook():
    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook

    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook


def main(controllers=[], viewers=[]):
    # prepare application
    app = QtWidgets.QApplication(sys.argv)
    QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))

    addExceptionHook()
    prepareImports()
    registerControllers(controllers)
    registerViewers(viewers)
    loadResources()

    # start application
    app_ctrl = AppController()
    features.Provide(AppController.__name__, app_ctrl)
    app_ctrl.show()
    sys.exit(app.exec_())


def loadResources():
    __import__("solarviewer.ui.resources_rc", globals(), locals())


def prepareImports():
    __import__("solarviewer.app.content", globals(), locals(), ['*'])
    __import__("solarviewer.app.statusbar", globals(), locals(), ['*'])
    __import__("solarviewer.viewer", globals(), locals(), ['*'])
    __import__("solarviewer.tool", globals(), locals(), ['*'])
    __import__("solarviewer.action", globals(), locals(), ['*'])
    __import__("solarviewer.dialog", globals(), locals(), ['*'])
    __import__("solarviewer.toolbar", globals(), locals(), ['*'])


def registerControllers(controllers):
    ctrls = getAllSubclasses(Controller)  # load base controllers
    ctrls.extend(controllers)
    for c in ctrls:
        if isabstract(c):
            continue
        features.Provide(c.name, c())  # instantiate and add to ioc container


def registerViewers(viewers):
    ctrls = ViewerController.__subclasses__()
    ctrls.extend(viewers)
    features.Provide(viewers_name, ctrls)


def getAllSubclasses(cls):
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(getAllSubclasses(subclass))

    return all_subclasses


if __name__ == '__main__':
    main()
