import numpy as np
from adapt.forecasting.base import BaseForecaster
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

class ExponentialSmoothingForecaster(BaseForecaster):
    """
    Model 3: Exponential Smoothing (Holt-Winters family).
    Applies geometrically decreasing weights over historical observations.
    """
    def __init__(self, horizon: int = 3, alpha: float = 0.4):
        super().__init__(name="ExponentialSmoothing", horizon=horizon)
        self.alpha = alpha
        self.is_fitted = True

    def fit(self, X: np.ndarray, y: np.ndarray) -> "ExponentialSmoothingForecaster":
        self.is_fitted = True
        return self

    def _predict_raw(self, window: np.ndarray) -> float:
        if window.ndim == 2:
            series = window[:, 0]
        else:
            series = window
        try:
            model = SimpleExpSmoothing(series, initialization_method="heuristic").fit(
                smoothing_level=self.alpha, optimized=False
            )
            forecast = model.forecast(self.horizon)
            return float(forecast[-1])
        except Exception:
            return float(series[-1])
