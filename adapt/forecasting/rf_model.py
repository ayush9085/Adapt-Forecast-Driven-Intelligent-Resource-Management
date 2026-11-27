import numpy as np
from sklearn.ensemble import RandomForestRegressor
from adapt.forecasting.base import BaseForecaster

class RandomForestForecaster(BaseForecaster):
    """
    Standard Time-Series Baseline 2: Random Forest Regressor.
    Ensemble of decision trees on historical window features.
    """
    def __init__(self, horizon: int = 3, n_estimators: int = 50, random_state: int = 42):
        super().__init__(name="RandomForest", horizon=horizon)
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.model = RandomForestRegressor(
            n_estimators=self.n_estimators,
            max_depth=8,
            random_state=self.random_state,
            n_jobs=-1
        )

    def fit(self, X: np.ndarray, y: np.ndarray) -> "RandomForestForecaster":
        if X.ndim == 3:
            samples, seq_len, feats = X.shape
            X_flat = X.reshape(samples, seq_len * feats)
        elif X.ndim == 2:
            X_flat = X
        else:
            X_flat = X.reshape(-1, 1)

        self.model.fit(X_flat, y)
        self.is_fitted = True
        return self

    def _predict_raw(self, window: np.ndarray) -> float:
        if not self.is_fitted:
            return float(window[-1, 0] if window.ndim == 2 else window[-1])
            
        if window.ndim == 2:
            seq_len, feats = window.shape
            w_flat = window.reshape(1, seq_len * feats)
        else:
            w_flat = window.reshape(1, -1)
            
        pred = self.model.predict(w_flat)[0]
        return float(pred)

    @property
    def feature_importances_(self):
        return self.model.feature_importances_ if self.is_fitted else None
