import numpy as np
import pandas as pd
from typing import Optional

def generate_synthetic_workload(
    duration_seconds: int = 120,
    seed: int = 42,
    base_cpu: float = 35.0,
    burst_start: int = 60,
    burst_duration: int = 30,
    burst_height: float = 55.0,
    noise_std: float = 3.0,
    tenant_id: str = "tenant_latency_sensitive"
) -> pd.DataFrame:
    """
    Generates synthetic OS workload telemetry with periodic cycles, gradual drift,
    burst contention, memory, IO, and task metrics.
    """
    np.random.seed(seed)
    timestamps = np.arange(0, duration_seconds)
    
    # 1. Base periodic workload (sine wave diurnal pattern)
    period = 40.0
    periodic_component = 12.0 * np.sin(2 * np.pi * timestamps / period)
    
    # 2. Burst component
    burst = np.zeros(duration_seconds)
    burst_mask = (timestamps >= burst_start) & (timestamps < burst_start + burst_duration)
    burst[burst_mask] = burst_height
    
    # Smooth transition for burst
    if burst_start > 2 and burst_start + burst_duration < duration_seconds - 2:
        for idx in range(burst_start - 2, burst_start):
            burst[idx] = burst_height * (idx - burst_start + 3) / 3.0
    
    # 3. Random noise
    noise = np.random.normal(0, noise_std, duration_seconds)
    
    # 4. Total CPU demand
    cpu_util = base_cpu + periodic_component + burst + noise
    cpu_util = np.clip(cpu_util, 5.0, 99.0)
    
    # Correlated metrics:
    # Memory: smoother, rises with CPU
    memory_util = 40.0 + 0.3 * cpu_util + np.random.normal(0, 1.5, duration_seconds)
    memory_util = np.clip(memory_util, 10.0, 95.0)
    
    # IO rate (ops/sec)
    io_rate = 50.0 + 2.0 * cpu_util + np.random.exponential(15.0, duration_seconds)
    
    # Task count
    task_count = 10 + (cpu_util // 8).astype(int) + np.random.randint(-1, 2, duration_seconds)
    task_count = np.clip(task_count, 4, 30)
    
    # Request rate (req/s)
    request_rate = 100.0 + 15.0 * cpu_util + np.random.normal(0, 20.0, duration_seconds)
    request_rate = np.clip(request_rate, 20.0, 2500.0)
    
    # Baseline latency estimate (ms) without queueing
    base_latency = 5.0 + 0.1 * cpu_util + np.random.normal(0, 1.0, duration_seconds)
    base_latency = np.clip(base_latency, 2.0, 50.0)
    
    df = pd.DataFrame({
        "timestamp": timestamps,
        "tenant_id": tenant_id,
        "cpu_utilization": np.round(cpu_util, 2),
        "memory_utilization": np.round(memory_util, 2),
        "io_rate": np.round(io_rate, 2),
        "task_count": task_count,
        "request_rate": np.round(request_rate, 2),
        "latency_ms": np.round(base_latency, 2)
    })
    return df

def generate_multi_tenant_workloads(
    duration_seconds: int = 120,
    seed: int = 42
) -> dict[str, pd.DataFrame]:
    """Generates 3 realistic competing tenants."""
    # Tenant A: Latency-sensitive web microservice (bursty + periodic)
    tA = generate_synthetic_workload(
        duration_seconds=duration_seconds,
        seed=seed,
        base_cpu=30.0,
        burst_start=45,
        burst_duration=25,
        burst_height=50.0,
        tenant_id="tenant_A_latency_sensitive"
    )
    
    # Tenant B: Batch processing (step surge at t=70)
    tB = generate_synthetic_workload(
        duration_seconds=duration_seconds,
        seed=seed + 10,
        base_cpu=20.0,
        burst_start=70,
        burst_duration=40,
        burst_height=40.0,
        noise_std=1.5,
        tenant_id="tenant_B_batch"
    )
    
    # Tenant C: Background maintenance (low, predictable)
    tC = generate_synthetic_workload(
        duration_seconds=duration_seconds,
        seed=seed + 20,
        base_cpu=15.0,
        burst_start=15,
        burst_duration=10,
        burst_height=15.0,
        noise_std=1.0,
        tenant_id="tenant_C_background"
    )
    return {
        "tenant_A": tA,
        "tenant_B": tB,
        "tenant_C": tC
    }
