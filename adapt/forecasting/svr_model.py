import numpy as np
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from adapt.forecasting.base import BaseForecaster

class SVRForecaster(BaseForecaster):
    """
    Standard Time-Series Baseline 1: Support Vector Regression (SVR).
    Uses RBF kernel on sliding window features.
    """
    def __init__(self, horizon: int = 3, C: float = 10.0, epsilon: float = 0.1):
        super().__init__(name="SupportVectorRegression", horizon=horizon)
        self.C = C
        self.epsilon = epsilon
        self.scaler = StandardScaler()
        self.model = SVR(kernel="rbf", C=self.C, epsilon=self.epsilon)

    def fit(self, X: np.ndarray, y: np.ndarray) -> "SVRForecaster":
        # X: [samples, seq_len, features] or [samples, seq_len]
        if X.ndim == 3:
            samples, seq_len, feats = X.shape
            X_flat = X.reshape(samples, seq_len * feats)
        elif X.ndim == 2:
            X_flat = X
        else:
            X_flat = X.reshape(-1, 1)

        X_scaled = self.scaler.fit_transform(X_flat)
        self.model.fit(X_scaled, y)
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
            
        w_scaled = self.scaler.transform(w_flat)
        pred = self.model.predict(w_scaled)[0]
        return float(pred)
