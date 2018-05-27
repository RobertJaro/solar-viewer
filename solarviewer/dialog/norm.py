from astropy.visualization import mpl_normalize
from astropy.visualization.stretch import *
from astropy.visualization.stretch import InvertedPowerDistStretch, InvertedLogStretch, InvertedContrastBiasStretch
from qtpy import QtWidgets

from solarviewer.config.base import DialogController, ViewerController, ItemConfig, ViewerType, DataType
from solarviewer.ui.norm import Ui_Norm
from solarviewer.viewer.map import MapModel


class NormController(DialogController):
    stretches = {LinearStretch: [],
                 SqrtStretch: [],
                 PowerStretch: [("power", float, 2.0)],
                 PowerDistStretch: [("exp", float, 1000.0)],
                 InvertedPowerDistStretch: [("exp", float, 1000.0)],
                 LogStretch: [("exp", float, 1000.0)],
                 InvertedLogStretch: [("exp", float, 1000.0)],
                 AsinhStretch: [("a", float, 0.1)],
                 SinhStretch: [("a", float, 1. / 3.)],
                 ContrastBiasStretch: [("contrast", float, 0), ("bias", float, 0)],
                 InvertedContrastBiasStretch: [("contrast", float, 0), ("bias", float, 0)]}

    def __init__(self):
        self.settings_widgets = []

        DialogController.__init__(self)

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setTitle("Normalization").setMenuPath("Edit/Normalization").addSupportedViewer(
            ViewerType.MPL).addSupportedData(DataType.MAP)

    def setupContent(self, content_widget):
        self._ui = Ui_Norm()
        self._ui.setupUi(content_widget)

        norm_names = [s.__name__ for s in self.stretches.keys()]
        self._ui.norm_combo.addItems(norm_names)
        self._ui.norm_combo.currentIndexChanged.connect(self._onChanged)

    def _onChanged(self, index):
        # clear old widgets
        for label, input_w in self.settings_widgets:
            label.deleteLater()
            input_w.deleteLater()
        self.settings_widgets.clear()

        args = list(self.stretches.values())[index]
        for arg, type, default in args:
            label = QtWidgets.QLabel(arg)
            input_w = self._createInputWidget(default, type)
            self.settings_widgets.append((label, input_w))
            self._ui.layout.addRow(label, input_w)

    def _createInputWidget(self, default, type):
        input_w = None
        if type is float:
            input_w = QtWidgets.QDoubleSpinBox()
            input_w.setRange(-10 ** 10, 10 ** 10)
            input_w.setValue(default)
        return input_w

    def onDataChanged(self, viewer_ctrl: ViewerController):
        norm = viewer_ctrl.model.norm
        if not issubclass(type(norm), mpl_normalize.ImageNormalize):
            # only image normalizations supported
            clip = norm.clip
            vmin = norm.vmin
            vmax = norm.vmax
            norm = mpl_normalize.ImageNormalize(vmin=vmin, vmax=vmax, clip=clip, stretch=LinearStretch())
        stretch = norm.stretch
        self._ui.norm_combo.setCurrentText(type(stretch).__name__)
        for label, input_w in self.settings_widgets:
            input_w.setValue(getattr(stretch, label.text()))

    def modifyData(self, data_model: MapModel) -> MapModel:
        old_norm = data_model.norm
        clip = old_norm.clip
        vmin = old_norm.vmin
        vmax = old_norm.vmax

        norm = mpl_normalize.ImageNormalize(vmin=vmin, vmax=vmax, clip=clip, stretch=self._getStretch())
        data_model.norm = norm
        return data_model

    def _getStretch(self):
        index = self._ui.norm_combo.currentIndex()
        stretch = list(self.stretches.keys())[index]
        args = [input_w.value() for _, input_w in self.settings_widgets]
        return stretch(*args)
