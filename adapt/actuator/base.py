from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseActuator(ABC):
    """
    Abstract interface for OS resource actuators.
    Decoupled Tier-2 actuation layer.
    """
    def __init__(self, name: str = "BaseActuator"):
        self.name = name
        self.current_quota: float = 50.0
        self.current_weight: int = 100
        self.current_nice: int = 0
        self.actuation_count: int = 0

    @abstractmethod
    def set_cpu_quota(self, quota_percent: float) -> bool:
        """Sets CPU bandwidth limit (e.g., cpu.max in cgroups)."""
        pass

    @abstractmethod
    def set_cpu_weight(self, weight: int) -> bool:
        """Sets CPU share weight (e.g., cpu.weight 1-10000 in cgroups)."""
        pass

    @abstractmethod
    def set_nice(self, nice_val: int) -> bool:
        """Sets process nice priority (-20 to 19)."""
        pass

    def reset(self) -> bool:
        self.current_quota = 50.0
        self.current_weight = 100
        self.current_nice = 0
        self.actuation_count = 0
        return True

    def get_state(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "current_quota": self.current_quota,
            "current_weight": self.current_weight,
            "current_nice": self.current_nice,
            "actuations": self.actuation_count
        }
