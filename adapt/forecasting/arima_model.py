import numpy as np
import warnings
from adapt.forecasting.base import BaseForecaster
from statsmodels.tsa.arima.model import ARIMA

class ARIMAForecaster(BaseForecaster):
    """
    Model 4: AutoRegressive Integrated Moving Average (ARIMA).
    Captures temporal autocorrelation and linear momentum.
    """
    def __init__(self, horizon: int = 3, order: tuple = (2, 1, 0)):
        super().__init__(name="ARIMA", horizon=horizon)
        self.order = order
        self.is_fitted = True

    def fit(self, X: np.ndarray, y: np.ndarray) -> "ARIMAForecaster":
        self.is_fitted = True
        return self

    def _predict_raw(self, window: np.ndarray) -> float:
        if window.ndim == 2:
            series = window[:, 0]
        else:
            series = window
            
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                # Fit compact ARIMA on the current rolling context
                model = ARIMA(series, order=self.order)
                fitted = model.fit()
                forecast = fitted.forecast(steps=self.horizon)
                return float(forecast[-1])
            except Exception:
                # Fallback to trend slope extrapolation
                diff = series[-1] - series[-2] if len(series) >= 2 else 0.0
                return float(series[-1] + diff * self.horizon)
