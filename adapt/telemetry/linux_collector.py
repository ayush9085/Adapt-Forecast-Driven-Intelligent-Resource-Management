import os
import time
import psutil
from typing import Dict, Any
from adapt.telemetry.collector import BaseTelemetryCollector
from adapt.utils.platform import is_linux

class LinuxTelemetryCollector(BaseTelemetryCollector):
    """
    Live Linux OS Telemetry Collector.
    Reads real host CPU from psutil, /proc/stat, and /proc/loadavg.
    Cross-platform safe: falls back to psutil system sampling when on macOS/BSD.
    """
    def __init__(self, sample_interval: float = 0.1):
        super().__init__(name="LinuxCollector")
        self.sample_interval = sample_interval

    def sample(self) -> Dict[str, Any]:
        cpu_util = psutil.cpu_percent(interval=self.sample_interval)
        mem = psutil.virtual_memory()
        
        load_avg = 0.0
        if hasattr(os, "getloadavg"):
            load_avg = os.getloadavg()[0]
            
        task_count = len(psutil.pids())
        
        return {
            "timestamp": int(time.time()),
            "cpu_utilization": float(cpu_util),
            "memory_utilization": float(mem.percent),
            "task_count": task_count,
            "io_rate": 0.0,
            "load_avg_1m": float(load_avg)
        }
