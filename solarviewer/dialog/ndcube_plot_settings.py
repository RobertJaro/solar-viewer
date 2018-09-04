from ndcube import NDCube

from solarviewer.config.base import DialogController, DataModel, ViewerController, ItemConfig, DataType, ViewerType
from solarviewer.ui.ndcube_plot_settings import Ui_NDCubePlotSettings
from solarviewer.viewer.ndcube import NDCubeModel


class NDCubePlotSettingsController(DialogController):

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().addSupportedData(DataType.ANY).addSupportedViewer(ViewerType.NDCUBE).setMenuPath(
            "View/Plot Settings").setTitle("NDCube Plot Settings")

    def setupContent(self, content_widget):
        self._ui = Ui_NDCubePlotSettings()
        self._ui.setupUi(content_widget)

    def onDataChanged(self, viewer_ctrl: ViewerController):
        image_axes = viewer_ctrl.model.image_axes
        cube: NDCube = viewer_ctrl.model.cube

        axes = [ax if ax else "Unknown Axis Type" for ax in cube.world_axis_physical_types]

        self._ui.xaxis.clear()
        self._ui.xaxis.addItems(axes)
        x_index = image_axes[0] if image_axes[0] >= 0 else len(axes) + image_axes[0]
        self._ui.xaxis.setCurrentIndex(x_index)

        self._ui.yaxis.clear()
        self._ui.yaxis.addItems(axes)
        y_index = image_axes[1] if image_axes[1] >= 0 else len(axes) + image_axes[1]
        self._ui.yaxis.setCurrentIndex(y_index)

    def modifyData(self, data_model: NDCubeModel) -> DataModel:
        data_model.image_axes = [self._ui.xaxis.currentIndex(), self._ui.yaxis.currentIndex()]
        return data_model
