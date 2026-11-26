from typing import Dict, Any, Tuple
import numpy as np

class SafetyGuard:
    """
    Deterministic OS Safety Guard.
    Validates model sanity, confidence boundaries, concept drift status,
    and inference latency before allowing proactive actuation to alter system state.
    
    Tracks distinct fallback episodes (transitions from safe -> fallback)
    and cumulative ticks spent in fallback state.
    """
    def __init__(
        self,
        confidence_threshold: float = 0.60,
        max_inference_latency_ms: float = 50.0,
        enabled: bool = True
    ):
        self.confidence_threshold = confidence_threshold
        self.max_inference_latency_ms = max_inference_latency_ms
        self.enabled = enabled
        
        self.fallback_episodes: int = 0
        self.fallback_ticks: int = 0
        self.is_in_fallback: bool = False
        self.last_reason: str = "SAFE"

    def evaluate(
        self,
        predicted_cpu: float,
        confidence: float,
        drift_detected: bool,
        inference_latency_ms: float = 1.0,
        telemetry_valid: bool = True
    ) -> Tuple[bool, str]:
        """
        Returns (is_safe, reason).
        If is_safe is False, scheduler MUST engage safe fallback to reactive baseline.
        """
        if not self.enabled:
            return True, "SAFETY_DISABLED_OVERRIDE"
            
        reason = "SAFE"
        is_safe = True
        
        if not telemetry_valid:
            is_safe = False
            reason = "INVALID_TELEMETRY"
        elif np.isnan(predicted_cpu) or np.isinf(predicted_cpu):
            is_safe = False
            reason = "PREDICTION_NAN_OR_INF"
        elif predicted_cpu < 0.0 or predicted_cpu > 150.0:
            is_safe = False
            reason = "PREDICTION_OUT_OF_BOUNDS"
        elif confidence < self.confidence_threshold:
            is_safe = False
            reason = f"LOW_CONFIDENCE_{confidence:.2f}"
        elif drift_detected:
            is_safe = False
            reason = "CONCEPT_DRIFT_DETECTED"
        elif inference_latency_ms > self.max_inference_latency_ms:
            is_safe = False
            reason = f"INFERENCE_TIMEOUT_{inference_latency_ms:.1f}ms"
            
        # Transition accounting
        if not is_safe:
            self.fallback_ticks += 1
            if not self.is_in_fallback:
                # Transition into new fallback episode
                self.fallback_episodes += 1
                self.is_in_fallback = True
            self.last_reason = reason
        else:
            if self.is_in_fallback:
                # Recovery transition
                self.is_in_fallback = False
            self.last_reason = "SAFE"
            
        return is_safe, reason

    def reset(self):
        self.fallback_episodes = 0
        self.fallback_ticks = 0
        self.is_in_fallback = False
        self.last_reason = "SAFE"
