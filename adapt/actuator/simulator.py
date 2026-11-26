from adapt.actuator.base import BaseActuator
from adapt.utils.logger import get_logger

logger = get_logger("actuator_simulator")

class SimulatedActuator(BaseActuator):
    """
    Safe cross-platform virtual actuator for simulation and dry-run execution.
    Works seamlessly on macOS, Windows, and Linux without root privileges.
    """
    def __init__(self):
        super().__init__(name="SimulatedActuator")

    def set_cpu_quota(self, quota_percent: float) -> bool:
        self.current_quota = float(quota_percent)
        self.actuation_count += 1
        return True

    def set_cpu_weight(self, weight: int) -> bool:
        self.current_weight = int(weight)
        return True

    def set_nice(self, nice_val: int) -> bool:
        self.current_nice = int(nice_val)
        return True
