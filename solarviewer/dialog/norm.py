from PyQt5 import QtWidgets
from astropy.visualization import mpl_normalize
from astropy.visualization.stretch import *
from astropy.visualization.stretch import InvertedPowerDistStretch, InvertedLogStretch, InvertedContrastBiasStretch
from matplotlib import colors

from solarviewer.config.base import DialogController, ViewerController, ItemConfig, ViewerType, DataType
from solarviewer.ui.norm import Ui_Norm
from solarviewer.viewer.map import MapModel


class NormController(DialogController):
    norms = {
        colors.NoNorm: [],
        colors.LogNorm: [],
        colors.SymLogNorm: [("linthresh", float, 0)],
        LinearStretch: [],
        SqrtStretch: [],
        PowerStretch: [("power", float, 2.0)],
        PowerDistStretch: [("exp", float, 1000.0)],
        InvertedPowerDistStretch: [("exp", float, 1000.0)],
        LogStretch: [("exp", float, 1000.0)],
        InvertedLogStretch: [("exp", float, 1000.0)],
        AsinhStretch: [("a", float, 0.1)],
        SinhStretch: [("a", float, 1. / 3.)],
        ContrastBiasStretch: [("contrast", float, 0), ("bias", float, 0)],
        InvertedContrastBiasStretch: [("contrast", float, 0), ("bias", float, 0)]
    }

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

        norm_names = [norm.__name__ for norm in self.norms.keys()]
        self._ui.norm_combo.addItems(norm_names)
        self._ui.norm_combo.currentIndexChanged.connect(self._onChanged)

    def _onChanged(self, index):
        # clear old widgets
        for label, input_w in self.settings_widgets:
            label.deleteLater()
            input_w.deleteLater()
        self.settings_widgets.clear()

        args = list(self.norms.values())[index]
        for arg, type, default in args:
            label = QtWidgets.QLabel(arg)
            input_w = self._createInputWidget(default, type)
            self.settings_widgets.append((label, input_w))
            self._ui.layout.addRow(label, input_w)

    def onDataChanged(self, viewer_ctrl: ViewerController):
        norm = viewer_ctrl.model.norm
        if isinstance(norm, mpl_normalize.ImageNormalize):
            norm = norm.stretch
        self._ui.norm_combo.setCurrentText(type(norm).__name__)  # fills settings widgets
        for label, input_w in self.settings_widgets:
            input_w.setValue(getattr(norm, label.text()))

    def modifyData(self, data_model: MapModel) -> MapModel:
        old_norm = data_model.norm
        clip = old_norm.clip
        vmin = old_norm.vmin
        vmax = old_norm.vmax

        data_model.norm = self._getNorm(clip, vmax, vmin)
        return data_model

    def _createInputWidget(self, default, type):
        input_w = None
        if type is float:
            input_w = QtWidgets.QDoubleSpinBox()
            input_w.setRange(-10 ** 10, 10 ** 10)
            input_w.setDecimals(5)
            input_w.setSingleStep(0.00001)
            input_w.setValue(default)
        return input_w

    def _getNorm(self, clip, vmax, vmin):
        index = self._ui.norm_combo.currentIndex()
        norm = list(self.norms.keys())[index]
        args = [input_w.value() for _, input_w in self.settings_widgets]

        if issubclass(norm, mpl_normalize.BaseStretch):
            stretch = norm(*args)
            return mpl_normalize.ImageNormalize(vmin=vmin, vmax=vmax, clip=clip, stretch=stretch)
        else:
            return norm(vmin=vmin, vmax=vmax, clip=clip, *args)
