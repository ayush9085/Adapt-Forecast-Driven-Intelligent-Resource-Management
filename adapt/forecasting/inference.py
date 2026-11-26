import time
import numpy as np
from typing import Dict, Any, Optional
from adapt.forecasting.base import BaseForecaster
from adapt.forecasting.confidence import ConfidenceEstimator

class InferenceEngine:
    """
    Tier-1 Real-time Inference Engine.
    Executes in user-space, handles rolling prediction, measures inference latency,
    and updates confidence heuristics.
    """
    def __init__(self, model: BaseForecaster, confidence_window: int = 10):
        self.model = model
        self.confidence_estimator = ConfidenceEstimator(window_size=confidence_window)
        self.last_prediction: Optional[float] = None
        self.last_confidence: float = 1.0
        self.last_latency_ms: float = 0.0

    def predict(self, window: np.ndarray) -> Dict[str, Any]:
        t0 = time.perf_counter()
        pred = self.model.predict(window)
        latency_ms = (time.perf_counter() - t0) * 1000.0
        
        conf = self.confidence_estimator.get_confidence()
        
        self.last_prediction = pred
        self.last_confidence = conf
        self.last_latency_ms = latency_ms
        
        return {
            "predicted_cpu": pred,
            "confidence": conf,
            "inference_latency_ms": round(latency_ms, 3),
            "model_name": self.model.name,
            "horizon": self.model.horizon
        }

    def feedback(self, actual: float, previous_actual: float = None):
        """Called when actual demand from future epoch arrives."""
        if self.last_prediction is not None:
            self.confidence_estimator.record_outcome(
                self.last_prediction, actual, previous_actual
            )
