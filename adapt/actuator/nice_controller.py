import os
import psutil
from adapt.actuator.base import BaseActuator
from adapt.utils.logger import get_logger

logger = get_logger("nice_controller")

class NiceController(BaseActuator):
    """
    Secondary actuator: adjusts Linux process nice priority (-20 to 19).
    Restricted strictly to configured child / target processes.
    """
    def __init__(self, target_pid: int = None, dry_run: bool = True):
        super().__init__(name="NiceController")
        self.target_pid = target_pid
        self.dry_run = dry_run

    def set_cpu_quota(self, quota_percent: float) -> bool:
        self.current_quota = quota_percent
        return True

    def set_cpu_weight(self, weight: int) -> bool:
        self.current_weight = weight
        return True

    def set_nice(self, nice_val: int) -> bool:
        self.current_nice = int(max(-20, min(19, nice_val)))
        if self.dry_run or self.target_pid is None:
            logger.debug(f"[DRY RUN] Process {self.target_pid} nice -> {self.current_nice}")
            return True
            
        try:
            p = psutil.Process(self.target_pid)
            p.nice(self.current_nice)
            return True
        except Exception as e:
            logger.warning(f"Could not set nice for PID {self.target_pid}: {e}")
            return False
