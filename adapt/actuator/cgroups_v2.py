import os
from adapt.actuator.base import BaseActuator
from adapt.utils.platform import is_linux, is_cgroup_v2_available
from adapt.utils.logger import get_logger

logger = get_logger("cgroups_v2_actuator")

class CgroupsV2Actuator(BaseActuator):
    """
    Production Linux cgroups v2 Actuator.
    Controls cpu.max (quota) and cpu.weight (proportional share) via standard sysfs.
    Defaults to DRY_RUN mode for safety unless explicitly enabled with write access.
    """
    def __init__(
        self,
        cgroup_path: str = "/sys/fs/cgroup/adapt.slice",
        period_us: int = 100000,
        dry_run: bool = True
    ):
        super().__init__(name="CgroupsV2Actuator")
        self.cgroup_path = cgroup_path
        self.period_us = period_us
        self.dry_run = dry_run
        self.is_supported = is_linux() and is_cgroup_v2_available()

    def set_cpu_quota(self, quota_percent: float) -> bool:
        self.current_quota = float(quota_percent)
        self.actuation_count += 1
        
        # In cgroups v2 cpu.max format: "$MAX $PERIOD" (e.g. "50000 100000" for 50%)
        if quota_percent >= 100.0:
            val_str = f"max {self.period_us}"
        else:
            quota_us = int((quota_percent / 100.0) * self.period_us)
            val_str = f"{quota_us} {self.period_us}"
            
        if self.dry_run or not self.is_supported:
            logger.debug(f"[DRY RUN] cgroups v2 cpu.max -> {val_str} ({quota_percent}%) at {self.cgroup_path}")
            return True
            
        target_file = os.path.join(self.cgroup_path, "cpu.max")
        try:
            with open(target_file, "w") as f:
                f.write(val_str)
            return True
        except PermissionError:
            logger.warning(f"Permission denied writing to {target_file}. Fallback to simulated mode.")
            return False
        except Exception as e:
            logger.error(f"Error writing to cgroup {target_file}: {e}")
            return False

    def set_cpu_weight(self, weight: int) -> bool:
        # cgroups v2 cpu.weight ranges from 1 to 10000 (default 100)
        self.current_weight = int(weight)
        w_val = int(max(1, min(10000, weight)))
        
        if self.dry_run or not self.is_supported:
            logger.debug(f"[DRY RUN] cgroups v2 cpu.weight -> {w_val} at {self.cgroup_path}")
            return True
            
        target_file = os.path.join(self.cgroup_path, "cpu.weight")
        try:
            with open(target_file, "w") as f:
                f.write(str(w_val))
            return True
        except Exception as e:
            logger.error(f"Error writing to {target_file}: {e}")
            return False

    def set_nice(self, nice_val: int) -> bool:
        self.current_nice = int(nice_val)
        return True
