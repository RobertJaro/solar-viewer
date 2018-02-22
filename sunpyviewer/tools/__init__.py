__all__ = ["contrast", "fft", "profile",
           "selection", "value_adjustment", "wavelet", "composite"]

from enum import Enum

EVT_FILTER_CLOSE = "fido.filter.close"
EVT_QUERY_STARTED = "query.started"
EVT_QUERY_RESULT = "query.result"
EVT_QUERY_ERROR = "query.error"

EVT_FFT_FILTER = "fft.filter"

EVT_PROFILE_MODE_CHANGE = "profile.mode.change"
EVT_PROFILE_RESET = "profile.reset"

EVT_SELECTION_EXPORT = "selection.export"
EVT_SELECTION_IMPORT = "selection.import"
EVT_SELECTION_CLEAR = "selection.clear"
EVT_SELECTION_POINT_REMOVE = "selection.point.remove"
EVT_SELECTION_STYLE_CHANGE = "selection.style.change"


class QueryType(Enum):
    FIDO = "vso"
    HEK = "hek"
