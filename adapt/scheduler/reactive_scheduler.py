from adapt.scheduler.base import BaseScheduler

class ReactiveScheduler(BaseScheduler):
    """
    Baseline C: Reactive Threshold Daemon.
    Responds only AFTER high utilization is observed across consecutive epochs.
    Classic reactive autoscaler / quota manager pattern.
    """
    def __init__(
        self,
        scale_up_threshold: float = 75.0,
        scale_down_threshold: float = 35.0,
        consecutive_epochs: int = 2,
        boost_step: float = 30.0,
        throttle_step: float = 15.0,
        initial_quota: float = 50.0
    ):
        super().__init__(name="Reactive Daemon")
        self.scale_up_threshold = scale_up_threshold
        self.scale_down_threshold = scale_down_threshold
        self.consecutive_epochs = consecutive_epochs
        self.boost_step = boost_step
        self.throttle_step = throttle_step
        self.current_allocation = initial_quota
        
        self.consecutive_high: int = 0
        self.consecutive_low: int = 0

    def schedule(self, current_demand: float, epoch: int, **kwargs):
        prev = self.current_allocation
        decision = "MAINTAIN"
        
        if current_demand >= self.scale_up_threshold:
            self.consecutive_high += 1
            self.consecutive_low = 0
            if self.consecutive_high >= self.consecutive_epochs:
                self.current_allocation = min(100.0, self.current_allocation + self.boost_step)
                decision = "REACTIVE_SCALE_UP"
        elif current_demand <= self.scale_down_threshold:
            self.consecutive_low += 1
            self.consecutive_high = 0
            if self.consecutive_low >= self.consecutive_epochs:
                self.current_allocation = max(20.0, self.current_allocation - self.throttle_step)
                decision = "REACTIVE_SCALE_DOWN"
        else:
            self.consecutive_high = 0
            self.consecutive_low = 0

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
        self.consecutive_high = 0
        self.consecutive_low = 0
