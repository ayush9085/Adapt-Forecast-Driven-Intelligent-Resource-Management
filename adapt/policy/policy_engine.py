from typing import Dict, Any, Tuple
import numpy as np

class PolicyEngine:
    """
    Tier-1 User-Space OS Policy Engine.
    Maps current utilization, predicted demand, headroom factors, and priority
    into bounded CPU quotas (percentage of core bandwidth) and cgroup weights.
    """
    def __init__(
        self,
        low_threshold: float = 35.0,
        high_threshold: float = 70.0,
        critical_threshold: float = 85.0,
        headroom_factor: float = 1.15,
        min_quota: float = 15.0,
        max_quota: float = 100.0
    ):
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
        self.critical_threshold = critical_threshold
        self.headroom_factor = headroom_factor
        self.min_quota = min_quota
        self.max_quota = max_quota

    def decide_allocation(
        self,
        current_cpu: float,
        predicted_cpu: float,
        current_quota: float,
        tenant_priority: int = 100
    ) -> Dict[str, Any]:
        """
        Determines target CPU quota, weight, and decision classification.
        """
        # Determine whether predicted workload signals an impending surge
        # We provision based on max(current, predicted) plus proactive headroom
        target_demand = max(current_cpu, predicted_cpu)
        proactive_quota = target_demand * self.headroom_factor
        
        # Determine category & reason
        if predicted_cpu >= self.critical_threshold:
            decision = "PROACTIVE_CRITICAL_BOOST"
            target_quota = max(proactive_quota, 90.0)
            target_weight = 200
            is_critical = True
        elif predicted_cpu >= self.high_threshold:
            decision = "PROACTIVE_SCALE_UP"
            target_quota = proactive_quota
            target_weight = 150
            is_critical = False
        elif predicted_cpu <= self.low_threshold and current_cpu <= self.low_threshold:
            decision = "PROACTIVE_SCALE_DOWN"
            target_quota = max(self.min_quota, proactive_quota)
            target_weight = 50
            is_critical = False
        else:
            decision = "MAINTAIN_NORMAL"
            target_quota = proactive_quota
            target_weight = 100
            is_critical = False
            
        # Priority scaling
        if tenant_priority > 100:
            target_quota *= (tenant_priority / 100.0)
            
        target_quota = float(np.clip(target_quota, self.min_quota, self.max_quota))
        
        return {
            "target_quota": round(target_quota, 2),
            "target_weight": int(target_weight),
            "decision": decision,
            "is_critical": is_critical,
            "proactive_delta": round(target_quota - current_quota, 2)
        }
