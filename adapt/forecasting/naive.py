import numpy as np
from adapt.forecasting.base import BaseForecaster

class NaivePersistenceForecaster(BaseForecaster):
    """
    Model 1: Naive Persistence baseline.
    Hypothesis: Future CPU at t+h equals current CPU at t.
    """
    def __init__(self, horizon: int = 3):
        super().__init__(name="NaivePersistence", horizon=horizon)
        self.is_fitted = True

    def fit(self, X: np.ndarray, y: np.ndarray) -> "NaivePersistenceForecaster":
        self.is_fitted = True
        return self

    def _predict_raw(self, window: np.ndarray) -> float:
        # window shape: [window_size, features] or [window_size]
        if window.ndim == 2:
            return float(window[-1, 0])
        return float(window[-1])
