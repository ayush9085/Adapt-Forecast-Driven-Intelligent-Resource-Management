from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseScheduler(ABC):
    """
    Abstract Scheduler interface for comparative evaluation.
    Evaluates demand telemetry and produces next allocation decisions.
    """
    def __init__(self, name: str):
        self.name = name
        self.current_allocation: float = 50.0
        self.allocation_changes: int = 0
        self.fallback_count: int = 0

    @abstractmethod
    def schedule(self, current_demand: float, epoch: int, **kwargs) -> Dict[str, Any]:
        """
        Receives current epoch telemetry.
        Returns dict with keys:
          'allocated_cpu': float,
          'decision': str,
          'is_fallback': bool,
          'predicted_cpu': Optional[float]
        """
        pass

    def reset(self):
        self.current_allocation = 50.0
        self.allocation_changes = 0
        self.fallback_count = 0
