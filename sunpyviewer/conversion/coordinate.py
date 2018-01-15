import astropy.units as u
import numpy as np


def extractCoordinates(sotMap, event):
    x = int(np.rint(event.xdata))
    y = int(np.rint(event.ydata))
    coord = sotMap.pixel_to_world(event.xdata * u.pixel, event.ydata * u.pixel)
    return [x, y, coord.Tx.value, coord.Ty.value]
