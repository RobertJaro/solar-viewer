from solarviewer.app.statusbar import StatusBarController
from solarviewer.config.ioc import RequiredFeature


class MPLCoordinatesMixin:
    status_bar_ctrl: StatusBarController = RequiredFeature(StatusBarController.name)

    def __init__(self):
        # add coordinates of mouse courser to status bar
        self.view.canvas.mpl_connect('motion_notify_event', self.onMapMotion)

    def onMapMotion(self, event):
        if event.inaxes:
            message = event.inaxes.format_coord(event.xdata, event.ydata)
            self.status_bar_ctrl.setText(message)
