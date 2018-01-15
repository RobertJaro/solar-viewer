import numpy as np
from skimage.exposure import exposure


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


def ideal2d_hp(shape, f, n, pxd=1):
    """Designs an ideal filter with cutin frequency f. pxd defines the number
   of pixels per unit of frequency (e.g., degrees of visual angle)."""
    return 1. - ideal2d_lp(shape, f, n, pxd)


def bandpass(data, highpass, lowpass, n, pxd, eq='histogram'):
    """Designs then applies a 2D bandpass filter to the resources array. If n is
   None, and ideal filter (with perfectly sharp transitions) is used
   instead."""
    fft = np.fft.fftshift(np.fft.fft2(data))
    if n:
        H = butter2d_bp(data.shape, highpass, lowpass, n, pxd)
    else:
        H = ideal2d_bp(data.shape, highpass, lowpass, pxd)
    fft_new = fft * H
    new_image = np.abs(np.fft.ifft2(np.fft.ifftshift(fft_new)))
    if eq == 'histogram':
        new_image = exposure.equalize_hist(new_image)
    return new_image
