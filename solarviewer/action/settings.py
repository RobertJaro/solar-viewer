import sunpy
from PyQt5.QtWidgets import QFileDialog
from qtpy import QtWidgets

from solarviewer.config.base import ActionController, ItemConfig
from solarviewer.ui.db_settings import Ui_DBSettings


class DBDialog(ActionController):
    def __init__(self):
        self._view = QtWidgets.QDialog()
        self._ui = Ui_DBSettings()
        self._ui.setupUi(self._view)

        def selectFile():
            path = QFileDialog.getExistingDirectory(directory=self._ui.file_path.text())
            if path:
                self._ui.file_path.setText(path)

        self._ui.file_select.clicked.connect(selectFile)
        self._ui.buttonBox.accepted.connect(self.onOk)

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setMenuPath("File/Change DB Settings")

    def onAction(self):
        self._ui.url.setText(sunpy.config.get("database", "url"))
        self._ui.file_path.setText(sunpy.config.get("downloads", "download_dir"))

        self._view.show()

    def onOk(self):
        dir = self._ui.file_path.text()
        url = self._ui.url.text()

        sunpy.config.set("database", "url", url)
        sunpy.config.set("downloads", "download_dir", dir)
