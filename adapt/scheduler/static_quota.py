from adapt.scheduler.base import BaseScheduler

class StaticQuotaScheduler(BaseScheduler):
    """
    Baseline B: Static Resource Reservation.
    Represents standard container quota provisioning (e.g., fixed K8s CPU limits).
    """
    def __init__(self, fixed_quota: float = 65.0):
        super().__init__(name="Static Quota")
        self.fixed_quota = fixed_quota
        self.current_allocation = fixed_quota

    def schedule(self, current_demand: float, epoch: int, **kwargs):
        return {
            "allocated_cpu": self.fixed_quota,
            "decision": "STATIC_RESERVATION",
            "is_fallback": False,
            "predicted_cpu": None
        }
