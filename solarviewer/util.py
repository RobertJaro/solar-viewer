import pkgutil
from threading import Event, Thread
from typing import Callable, List

from PyQt5.QtCore import pyqtSignal
from qtpy import QtCore, QtWidgets


class classproperty(object):

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


def executeWaitTask(event: Event, call_after, call_after_args=[]):
    """
    Waits for the event to finish and executes the call after function afterwards.
    Prevents long thread executions outside the main thread.

    :param event: threading event
    :param call_after: function to call after event finished
    :param call_after_args: arguments for the call after function
    :return: None
    """
    wt = _WaitingThread(event)
    wt.finished.connect(lambda: call_after(*call_after_args))
    wt.start()


def executeTask(execution: Callable, args=[], call_after: Callable = None, call_after_args=[]):
    """
    Executes the function and executes afterwards the call after function.
    The return value of the execution function will be passed to the call_after function as first parameter if not None.
    Prevents long thread executions outside the main thread.

    :param execution: function to execute
    :param args: arguments for the execution function
    :param call_after: function to call after execution finished
    :param call_after_args: additional arguments for the call after function
    :return: None
    """
    thread = _Thread(execution, args)
    if call_after:
        thread.finished.connect(lambda x: call_after(x, *call_after_args) if x else call_after(*call_after_args))
    thread.start()


def executeLongRunningTask(execution: Callable, args=[], message="", call_after: Callable = None, call_after_args=[]):
    """
    Shows a waiting indicator and executes the function. Afterwards the call after function is called.
    The return value of the execution function will be passed to the call_after function as first parameter if not None.
    Prevents long thread executions outside the main thread.

    :param execution: function to execute
    :param args: arguments for the execution function
    :param call_after: function to call after execution finished
    :param call_after_args: additional arguments for the call after function
    :return: None
    """
    thread = _Thread(execution, args)
    progress = QtWidgets.QProgressDialog(message, None, 0, 0, flags=QtCore.Qt.FramelessWindowHint)
    progress.setWindowModality(QtCore.Qt.ApplicationModal)
    bar = QtWidgets.QProgressBar()
    bar.setRange(0, 0)
    bar.setTextVisible(False)
    progress.setBar(bar)
    if call_after:
        thread.finished.connect(lambda x: call_after(x, *call_after_args) if x else call_after(*call_after_args))
    close_progress = lambda x, p=progress: p.close()
    thread.finished.connect(close_progress)
    progress.show()
    thread.start()


def installMissingAndExecute(package_names: List[str], execution: Callable, args=[]):
    """
    Checks for missing packages. The execution function is called when the requirements are fulfilled or the
    missing packages could be installed (depending on the user decision).

    :param package_names: required packages
    :param execution: callable function
    :param args: parameters of the execution
    :return: None
    """
    if _packagesInstalled(package_names):
        execution(*args)
        return
    msg = "This action requires additional python modules. Do you want to install them now?"
    reply = QtWidgets.QMessageBox.question(None, "Additional python package required", msg, QtWidgets.QMessageBox.Yes,
                                           QtWidgets.QMessageBox.No)
    if reply != QtWidgets.QMessageBox.Yes:
        return

    for pkg_name in package_names:
        if not pkgutil.find_loader(pkg_name):
            executeLongRunningTask(_install, [pkg_name], "Installing Packages", execution, args)


def checkPackages(package_names):
    """
    Checks if the required python packages are installed.

    :param package_names: python package names
    :return: True if all packages are installed, False otherwise
    """
    if _packagesInstalled(package_names):
        return True
    msg = "This action requires additional python modules. Do you want to install them now?"
    reply = QtWidgets.QMessageBox.question(None, "Additional python package required", msg, QtWidgets.QMessageBox.Yes,
                                           QtWidgets.QMessageBox.No)
    if reply != QtWidgets.QMessageBox.Yes:
        return False

    for pkg_name in package_names:
        if not pkgutil.find_loader(pkg_name):
            executeLongRunningTask(_install, [pkg_name], "Downloading Packages")
    return False


def _packagesInstalled(package_names):
    for pkg_name in package_names:
        pkg = pkgutil.find_loader(pkg_name)
        if pkg is None:
            return False
    return True


def _install(pkg_name):
    import pip
    pip.main(['install', pkg_name])


class _Thread(QtCore.QObject, Thread):
    finished = pyqtSignal(object)

    def __init__(self, execution, args):
        self.execution = execution
        self.args = args

        QtCore.QObject.__init__(self)
        Thread.__init__(self)

    def run(self):
        result = self.execution(*self.args)
        self.finished.emit(result)


class _WaitingThread(QtCore.QObject, Thread):
    finished = pyqtSignal()

    def __init__(self, event):
        self.event = event

        QtCore.QObject.__init__(self)
        Thread.__init__(self)

    def run(self):
        self.event.wait()
        self.finished.emit()
