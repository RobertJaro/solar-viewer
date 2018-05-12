from threading import Event, Thread

from PyQt5.QtCore import pyqtSignal
from qtpy import QtCore


class classproperty(object):

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


def executeWaitTask(event: Event, call_after, call_after_arg=[]):
    wt = _WaitingThread(event)
    wt.finished.connect(lambda: call_after(*call_after_arg))
    wt.start()


class _WaitingThread(QtCore.QObject, Thread):
    finished = pyqtSignal()

    def __init__(self, event):
        self.event = event

        QtCore.QObject.__init__(self)
        Thread.__init__(self)

    def run(self):
        self.event.wait()
        self.finished.emit()
