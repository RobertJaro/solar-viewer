import numpy as np
from PyQt5.QtWidgets import QWidget

from solarviewer.config.base import ItemConfig, ViewerType, DataType
from solarviewer.config.impl import DataToolController
from solarviewer.ui.fft import Ui_FFT


class FFTController(DataToolController):

    @property
    def item_config(self) -> ItemConfig:
        return ItemConfig().setTitle("FFT").setMenuPath("Tools/FFT").addSupportedData(
            DataType.PLAIN_2D).addSupportedData(DataType.MAP).addSupportedViewer(
            ViewerType.ANY)

    def setupContent(self, content_widget: QWidget):
        self._ui = Ui_FFT()
        self._ui.setupUi(content_widget)

    def onDataChanged(self, viewer_ctrl):
        # no action needed
        pass

    def modifyData(self, data_model):
        data = data_model.data

        # calculate radius
        shape = data.shape
        r = np.sqrt((shape[0] / 2) ** 2 + (shape[1] / 2) ** 2)

        # calculate cut off frequencies
        h_val = self._ui.highpass_spin.value() / 100 * r
        l_val = self._ui.lowpass_spin.value() / 100 * r

        # determine check box status
        highpass = self._ui.highpass_check.isChecked()
        lowpass = self._ui.lowpass_check.isChecked()

        # create filter
        if self._ui.butter_radio.isChecked():
            order = self._ui.butter_order_spin.value()
            filt = self._createButterworthFilter(h_val, highpass, l_val, lowpass, shape, order)
        else:
            filt = self._createIdealFilter(h_val, highpass, l_val, lowpass, shape)

        # filter and set data
        data = self._filterMap(filt, data)
        data_model.setData(data)
        return data_model

    def _filterMap(self, filt, data):
        np.nan_to_num(data, copy=False)
        fft = np.fft.fftshift(np.fft.fft2(data))
        filtered_fft = fft * filt
        back_transformed = np.abs(np.fft.ifft2(np.fft.ifftshift(filtered_fft)))
        return back_transformed

    def _createButterworthFilter(self, h_val, highpass, l_val, lowpass, shape, order):
        if highpass and lowpass:
            filt = butter2d_bp(shape, l_val, h_val, order)
        else:
            if highpass:
                filt = butter2d_hp(shape, h_val, order)
            if lowpass:
                filt = butter2d_lp(shape, l_val, order)
        return filt

    def _createIdealFilter(self, h_val, highpass, l_val, lowpass, shape):
        if highpass and lowpass:
            filt = ideal2d_bp(shape, l_val, h_val)
        else:
            if highpass:
                filt = ideal2d_hp(shape, h_val)
            if lowpass:
                filt = ideal2d_lp(shape, l_val)
        return filt


def butter2d_lp(shape, f, n=2, pxd=1):
    """Designs an n-th order lowpass 2D Butterworth filter with cutoff
   frequency f. pxd defines the number of pixels per unit of frequency (e.g.,
   degrees of visual angle)."""
    pxd = float(pxd)
    rows, cols = shape
    x = np.linspace(-0.5, 0.5, cols) * cols / pxd
    y = np.linspace(-0.5, 0.5, rows) * rows / pxd
    radius = np.sqrt((x ** 2)[np.newaxis] + (y ** 2)[:, np.newaxis])
    filt = 1 / (1.0 + (radius / f) ** (2 * n))
    return filt


def butter2d_bp(shape, cutin, cutoff, n=2, pxd=1):
    """Designs an n-th order bandpass 2D Butterworth filter with cutin and
   cutoff frequencies. pxd defines the number of pixels per unit of frequency
   (e.g., degrees of visual angle)."""
    return butter2d_lp(shape, cutoff, n, pxd) - butter2d_lp(shape, cutin, n, pxd)


def butter2d_hp(shape, f, n=2, pxd=1):
    """Designs an n-th order highpass 2D Butterworth filter with cutin
   frequency f. pxd defines the number of pixels per unit of frequency (e.g.,
   degrees of visual angle)."""
    return 1. - butter2d_lp(shape, f, n, pxd)


def ideal2d_lp(shape, f, pxd=1):
    """Designs an ideal filter with cutoff frequency f. pxd defines the number
   of pixels per unit of frequency (e.g., degrees of visual angle)."""
    pxd = float(pxd)
    rows, cols = shape
    x = np.linspace(-0.5, 0.5, cols) * cols / pxd
    y = np.linspace(-0.5, 0.5, rows) * rows / pxd
    radius = np.sqrt((x ** 2)[np.newaxis] + (y ** 2)[:, np.newaxis])
    filt = np.ones(shape)
    filt[radius > f] = 0
    return filt


def ideal2d_bp(shape, cutin, cutoff, pxd=1):
    """Designs an ideal filter with cutin and cutoff frequencies. pxd defines
   the number of pixels per unit of frequency (e.g., degrees of visual
   angle)."""
    return ideal2d_lp(shape, cutoff, pxd) - ideal2d_lp(shape, cutin, pxd)


def ideal2d_hp(shape, f, pxd=1):
    """Designs an ideal filter with cutin frequency f. pxd defines the number
   of pixels per unit of frequency (e.g., degrees of visual angle)."""
    return 1. - ideal2d_lp(shape, f, pxd)
