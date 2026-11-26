from collections import deque
import numpy as np
from typing import List, Optional

class SlidingBuffer:
    """
    Fixed-size rolling observation buffer for real-time telemetry streaming.
    """
    def __init__(self, capacity: int = 12):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)

    def append(self, telemetry_point: float):
        self.buffer.append(float(telemetry_point))

    def is_ready(self) -> bool:
        return len(self.buffer) >= self.capacity

    def get_window(self) -> np.ndarray:
        return np.array(self.buffer, dtype=np.float32)

    def clear(self):
        self.buffer.clear()
