import numpy as np
from collections import deque
from typing import Deque

class ConfidenceEstimator:
    """
    Evaluates forecasting confidence based on recent residual tracking.
    Confidence score is bounded in [0.0, 1.0].
    
    ENGINEERING HEURISTIC CLARIFICATION:
    This is an empirical engineering heuristic based on rolling forecast error variance
    and directional consistency. It is NOT a calibrated Bayesian posterior probability.
    """
    def __init__(self, window_size: int = 10, max_tolerated_error: float = 30.0):
        self.window_size = window_size
        self.max_tolerated_error = max_tolerated_error
        self.recent_errors: Deque[float] = deque(maxlen=window_size)
        self.recent_direction_matches: Deque[int] = deque(maxlen=window_size)

    def record_outcome(self, predicted: float, actual: float, previous_actual: float = None):
        err = float(abs(predicted - actual))
        self.recent_errors.append(err)
        
        if previous_actual is not None:
            pred_dir = 1 if predicted >= previous_actual else -1
            actual_dir = 1 if actual >= previous_actual else -1
            self.recent_direction_matches.append(1 if pred_dir == actual_dir else 0)

    def get_confidence(self) -> float:
        # If cold-start (< 3 observations), use a conservative neutral confidence rather than 1.0
        if len(self.recent_errors) < 3:
            return 0.75  # Cautious initial heuristic
            
        mean_err = np.mean(self.recent_errors)
        err_penalty = max(0.0, 1.0 - (mean_err / self.max_tolerated_error))
        
        dir_factor = 1.0
        if self.recent_direction_matches:
            dir_acc = np.mean(self.recent_direction_matches)
            dir_factor = 0.5 + 0.5 * dir_acc
            
        score = float(np.clip(err_penalty * dir_factor, 0.0, 1.0))
        return round(score, 3)

    def reset(self):
        self.recent_errors.clear()
        self.recent_direction_matches.clear()
