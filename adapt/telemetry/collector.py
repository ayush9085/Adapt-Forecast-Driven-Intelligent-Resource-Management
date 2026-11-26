from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseTelemetryCollector(ABC):
    """
    Abstract interface for OS telemetry collection.
    """
    def __init__(self, name: str = "BaseCollector"):
        self.name = name

    @abstractmethod
    def sample(self) -> Dict[str, Any]:
        """
        Samples system metrics.
        Returns dict with keys:
          'cpu_utilization': float,
          'memory_utilization': float,
          'task_count': int,
          'io_rate': float,
          'load_avg_1m': float
        """
        pass
