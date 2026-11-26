import numpy as np
from adapt.forecasting.base import BaseForecaster

class MovingAverageForecaster(BaseForecaster):
    """
    Model 2: Moving Average Forecaster.
    Averages the last k points of the window to smooth high-frequency jitter.
    """
    def __init__(self, horizon: int = 3, ma_window: int = 5):
        super().__init__(name="MovingAverage", horizon=horizon)
        self.ma_window = ma_window
        self.is_fitted = True

    def fit(self, X: np.ndarray, y: np.ndarray) -> "MovingAverageForecaster":
        self.is_fitted = True
        return self

    def _predict_raw(self, window: np.ndarray) -> float:
        if window.ndim == 2:
            series = window[:, 0]
        else:
            series = window
        k = min(self.ma_window, len(series))
        return float(np.mean(series[-k:]))
