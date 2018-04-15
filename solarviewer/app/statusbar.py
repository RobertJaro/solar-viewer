from qtpy import QtWidgets

from solarviewer.config.base import Controller


class StatusBarController(Controller):
    def __init__(self):
        self._view = QtWidgets.QStatusBar()

    @property
    def view(self):
        return self._view

    def setText(self, text: str):
        self._view.showMessage(text, 5000)
