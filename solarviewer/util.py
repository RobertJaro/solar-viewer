from threading import Event, Thread
from typing import Callable

from PyQt5.QtCore import pyqtSignal
from qtpy import QtCore


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
