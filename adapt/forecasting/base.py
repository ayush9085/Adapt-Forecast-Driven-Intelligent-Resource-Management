from abc import ABC, abstractmethod
import time
import numpy as np
from typing import Dict, Any, Optional

class BaseForecaster(ABC):
    """
    Abstract Base Class for all Adapt Time-Series Forecasters.
    Guarantees unified interface, safety checks, and latency profiling.
    """
    def __init__(self, name: str = "BaseForecaster", horizon: int = 3):
        self.name = name
        self.horizon = horizon
        self.is_fitted = False
        self.last_inference_latency_ms: float = 0.0

    @abstractmethod
    def fit(self, X: np.ndarray, y: np.ndarray) -> "BaseForecaster":
        """
        Fit model on historical sliding window data.
        X shape: [samples, window_size, features] or [samples, window_size]
        y shape: [samples]
        """
        pass

    @abstractmethod
    def _predict_raw(self, window: np.ndarray) -> float:
        """
        Predict future CPU demand for a single rolling window.
        window shape: [window_size, features] or [window_size]
        Returns scalar predicted CPU %.
        """
        pass

    def predict(self, window: np.ndarray) -> float:
        """
        Public inference method with latency tracking and safety validation.
        """
        t0 = time.perf_counter()
        try:
            val = self._predict_raw(window)
            # Validation check
            if np.isnan(val) or np.isinf(val):
                val = 50.0  # Safe neutral default
            val = float(np.clip(val, 0.0, 100.0))
        except Exception:
            val = 50.0
        finally:
            self.last_inference_latency_ms = (time.perf_counter() - t0) * 1000.0
        return val

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "horizon": self.horizon,
            "is_fitted": self.is_fitted,
            "last_inference_latency_ms": round(self.last_inference_latency_ms, 3)
        }
