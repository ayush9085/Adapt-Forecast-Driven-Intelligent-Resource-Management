import time
import psutil
from typing import Dict, Any
from adapt.telemetry.collector import BaseTelemetryCollector

class SimulatedTelemetryCollector(BaseTelemetryCollector):
    """
    Simulated Collector: Steps through an in-memory or generated workload sequence.
    """
    def __init__(self, workload_sequence: list[float] = None):
        super().__init__(name="SimulatedCollector")
        self.sequence = workload_sequence or [30.0, 32.0, 35.0, 40.0, 75.0, 85.0, 90.0]
        self.index = 0

    def sample(self) -> Dict[str, Any]:
        val = self.sequence[self.index % len(self.sequence)]
        self.index += 1
        return {
            "timestamp": int(time.time()),
            "cpu_utilization": float(val),
            "memory_utilization": 45.0 + 0.2 * val,
            "task_count": 12,
            "io_rate": 60.0,
            "load_avg_1m": val / 100.0 * 4.0
        }

    def reset(self):
        self.index = 0
