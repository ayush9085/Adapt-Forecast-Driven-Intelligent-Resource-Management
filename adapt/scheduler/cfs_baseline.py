from adapt.scheduler.base import BaseScheduler
from collections import deque

class CFSBaselineScheduler(BaseScheduler):
    """
    Baseline A: CFS-Like Reactive Resource-Control Baseline.
    
    IMPORTANT SCIENTIFIC DISTINCTION:
    The Linux Completely Fair Scheduler (CFS/EEVDF) performs thread-level fair scheduling
    in the kernel hot-path based on virtual runtime (vruntime). Outside the kernel, user-space
    controllers (or orchestration managers) configure cgroup bandwidth limits (cpu.max)
    or weights (cpu.weight) reactively.
    
    This simulation baseline models reactive resource-control surrounding fair CPU sharing:
    - Resource allocation responds strictly AFTER utilization is observed.
    - An observation & actuation control delay (default: 2 epochs) exists between when
      demand changes and when reactive quota adjustment takes effect.
    - Quota adjusts toward the moving window of observed past demand rather than
      clairvoyantly matching instantaneous future demand.
    """
    def __init__(
        self,
        default_quota: float = 50.0,
        control_interval_ticks: int = 2,
        min_quota: float = 20.0,
        max_quota: float = 100.0,
        step_size: float = 25.0
    ):
        super().__init__(name="CFS-Like Reactive Resource-Control")
        self.default_quota = default_quota
        self.current_allocation = default_quota
        self.control_interval_ticks = control_interval_ticks
        self.min_quota = min_quota
        self.max_quota = max_quota
        self.step_size = step_size
        
        self.recent_demands = deque(maxlen=control_interval_ticks)
        self.ticks_since_evaluation = 0

    def schedule(self, current_demand: float, epoch: int, **kwargs):
        self.recent_demands.append(current_demand)
        self.ticks_since_evaluation += 1
        
        prev = self.current_allocation
        decision = "MAINTAIN_OBSERVING"
        
        # Reactive adjustment occurs periodically after observation window
        if self.ticks_since_evaluation >= self.control_interval_ticks:
            self.ticks_since_evaluation = 0
            # Target is the observed recent demand plus fair-share buffer
            observed_avg = sum(self.recent_demands) / len(self.recent_demands)
            
            # Reactive rate-limited adjustment (cannot teleport to 100% instantly)
            if observed_avg > self.current_allocation:
                self.current_allocation = min(self.max_quota, self.current_allocation + self.step_size)
                decision = "REACTIVE_QUOTA_INCREASE"
            elif observed_avg < self.current_allocation - 15.0:
                self.current_allocation = max(self.min_quota, self.current_allocation - self.step_size * 0.5)
                decision = "REACTIVE_QUOTA_DECREASE"
            else:
                decision = "REACTIVE_STABLE"
                
        if abs(self.current_allocation - prev) > 0.5:
            self.allocation_changes += 1
            
        return {
            "allocated_cpu": self.current_allocation,
            "decision": decision,
            "is_fallback": False,
            "predicted_cpu": None
        }

    def reset(self):
        super().reset()
        self.current_allocation = self.default_quota
        self.recent_demands.clear()
        self.ticks_since_evaluation = 0
