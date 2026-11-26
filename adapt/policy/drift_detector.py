import numpy as np
from collections import deque
from typing import Deque

class ConceptDriftDetector:
    """
    Lightweight streaming concept-drift detector.
    Monitors recent forecast residuals versus historical baseline reference error.
    Triggers DRIFT if: recent_error > drift_multiplier * baseline_error.
    """
    def __init__(
        self,
        baseline_window: int = 30,
        recent_window: int = 6,
        drift_multiplier: float = 2.0,
        min_baseline_error: float = 3.0
    ):
        self.baseline_window = baseline_window
        self.recent_window = recent_window
        self.drift_multiplier = drift_multiplier
        self.min_baseline_error = min_baseline_error
        
        self.reference_errors: Deque[float] = deque(maxlen=baseline_window)
        self.recent_errors: Deque[float] = deque(maxlen=recent_window)
        self.drift_detected: bool = False
        self.last_ratio: float = 1.0

    def update(self, predicted: float, actual: float) -> bool:
        err = float(abs(predicted - actual))
        self.recent_errors.append(err)
        
        if len(self.reference_errors) < 8:
            self.reference_errors.append(err)
            self.drift_detected = False
            self.last_ratio = 1.0
            return False
            
        recent_rmse = float(np.sqrt(np.mean(np.square(self.recent_errors))))
        ref_rmse = float(np.sqrt(np.mean(np.square(self.reference_errors))))
        safe_ref = max(ref_rmse, self.min_baseline_error)
        
        self.last_ratio = recent_rmse / safe_ref
        
        if self.last_ratio > self.drift_multiplier:
            self.drift_detected = True
        else:
            self.drift_detected = False
            # Only update reference distribution when workload is under normal predictable conditions
            self.reference_errors.append(err)
            
        return self.drift_detected

    def reset(self):
        self.reference_errors.clear()
        self.recent_errors.clear()
        self.drift_detected = False
        self.last_ratio = 1.0
