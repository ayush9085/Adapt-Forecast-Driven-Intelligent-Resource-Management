from collections import deque
import numpy as np
from typing import Dict, Any, Optional

from adapt.scheduler.base import BaseScheduler
from adapt.forecasting.base import BaseForecaster
from adapt.forecasting.confidence import ConfidenceEstimator
from adapt.policy.policy_engine import PolicyEngine
from adapt.policy.safety_guard import SafetyGuard
from adapt.policy.drift_detector import ConceptDriftDetector
from adapt.policy.hysteresis import HysteresisController
from adapt.scheduler.cfs_baseline import CFSBaselineScheduler
from adapt.actuator.base import BaseActuator
from adapt.actuator.simulator import SimulatedActuator

class AdaptScheduler(BaseScheduler):
    """
    Proposed Architecture: Adapt: Forecast-Driven Intelligent Resource Management.
    Decoupled user-space predictive scheduling orchestrator with confidence tracking,
    drift detection, hysteresis suppression, and deterministic safety fallback.
    """
    def __init__(
        self,
        forecaster: BaseForecaster,
        window_size: int = 12,
        policy_engine: Optional[PolicyEngine] = None,
        safety_guard: Optional[SafetyGuard] = None,
        drift_detector: Optional[ConceptDriftDetector] = None,
        hysteresis: Optional[HysteresisController] = None,
        actuator: Optional[BaseActuator] = None
    ):
        super().__init__(name="Adapt (Proactive ML)")
        self.forecaster = forecaster
        self.window_size = window_size
        self.policy_engine = policy_engine or PolicyEngine()
        self.safety_guard = safety_guard or SafetyGuard()
        self.drift_detector = drift_detector or ConceptDriftDetector()
        self.hysteresis = hysteresis or HysteresisController()
        self.actuator = actuator or SimulatedActuator()
        self.fallback_scheduler = CFSBaselineScheduler()
        self.confidence_estimator = ConfidenceEstimator()
        
        self.history_buffer = deque(maxlen=window_size)
        self.last_predicted: Optional[float] = None
        self.last_decision = "INITIALIZING"
        self.is_currently_fallback = False
        self.fallback_reason = "NONE"

    def schedule(self, current_demand: float, epoch: int, **kwargs) -> Dict[str, Any]:
        prev_demand = self.history_buffer[-1] if self.history_buffer else current_demand
        self.history_buffer.append(current_demand)
        
        # 1. Provide feedback on previous forecast
        if self.last_predicted is not None:
            self.confidence_estimator.record_outcome(
                self.last_predicted, current_demand, prev_demand
            )
            self.drift_detector.update(self.last_predicted, current_demand)
            
        # 2. Check if sliding window buffer is populated
        if len(self.history_buffer) < self.window_size:
            # Buffer warming up -> safe baseline behavior
            fb_res = self.fallback_scheduler.schedule(current_demand, epoch)
            self.current_allocation = fb_res["allocated_cpu"]
            self.actuator.set_cpu_quota(self.current_allocation)
            return {
                "allocated_cpu": self.current_allocation,
                "decision": "BUFFER_WARMUP_BASELINE",
                "is_fallback": True,
                "predicted_cpu": current_demand,
                "confidence": 0.75,
                "safety_reason": "WARMING_UP"
            }
            
        # 3. Model Inference (User-space Tier 1)
        window_arr = np.array(self.history_buffer, dtype=float)
        predicted_cpu = self.forecaster.predict(window_arr)
        self.last_predicted = predicted_cpu
        
        # 4. Confidence & Drift evaluation
        confidence = self.confidence_estimator.get_confidence()
        drift = self.drift_detector.drift_detected
        inference_latency = self.forecaster.last_inference_latency_ms
        
        # 5. Deterministic Safety Guard check
        is_safe, safety_reason = self.safety_guard.evaluate(
            predicted_cpu=predicted_cpu,
            confidence=confidence,
            drift_detected=drift,
            inference_latency_ms=inference_latency
        )
        
        if not is_safe:
            # SAFETY FALLBACK: Revert to baseline allocation
            self.is_currently_fallback = True
            self.fallback_reason = safety_reason
            self.fallback_count = self.safety_guard.fallback_episodes
            
            fb_res = self.fallback_scheduler.schedule(current_demand, epoch)
            target_quota = fb_res["allocated_cpu"]
            self.current_allocation = target_quota
            self.actuator.set_cpu_quota(target_quota)
            
            return {
                "allocated_cpu": target_quota,
                "decision": f"FALLBACK_ENGAGED_{safety_reason}",
                "is_fallback": True,
                "predicted_cpu": predicted_cpu,
                "confidence": confidence,
                "safety_reason": safety_reason
            }
            
        # 6. Policy Engine Calculation
        self.is_currently_fallback = False
        self.fallback_reason = "NONE"
        policy_res = self.policy_engine.decide_allocation(
            current_cpu=current_demand,
            predicted_cpu=predicted_cpu,
            current_quota=self.current_allocation
        )
        
        target_quota = policy_res["target_quota"]
        is_critical = policy_res["is_critical"]
        
        # 7. Hysteresis Anti-Oscillation Guard
        should_change = self.hysteresis.should_apply_change(
            target_quota=target_quota,
            current_quota=self.current_allocation,
            is_critical=is_critical
        )
        
        if should_change:
            if abs(target_quota - self.current_allocation) > 0.5:
                self.allocation_changes += 1
            self.current_allocation = target_quota
            self.actuator.set_cpu_quota(target_quota)
            self.actuator.set_cpu_weight(policy_res["target_weight"])
            decision_label = policy_res["decision"]
        else:
            decision_label = "HYSTERESIS_MAINTAIN"
            
        return {
            "allocated_cpu": self.current_allocation,
            "decision": decision_label,
            "is_fallback": False,
            "predicted_cpu": predicted_cpu,
            "confidence": confidence,
            "safety_reason": "SAFE"
        }

    def reset(self):
        super().reset()
        self.history_buffer.clear()
        self.last_predicted = None
        self.confidence_estimator.reset()
        self.drift_detector.reset()
        self.safety_guard.reset()
        self.hysteresis.reset()
        self.actuator.reset()
        self.fallback_scheduler.reset()
        self.is_currently_fallback = False
        self.fallback_reason = "NONE"
