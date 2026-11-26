import numpy as np
import pandas as pd
from adapt.datasets.synthetic import generate_synthetic_workload

def get_scenario(scenario_name: str, duration: int = 120, seed: int = 42) -> pd.DataFrame:
    """
    Library of benchmark workload scenarios:
    1. Stable Load
    2. Step Contention (Sudden surge)
    3. Periodic / Diurnal (Sinusoidal)
    4. Bursty Traffic
    5. Concept Drift
    6. Noisy / Unpredictable
    7. Presentation Demo (Custom multi-phase sequence)
    """
    np.random.seed(seed)
    timestamps = np.arange(0, duration)
    
    if scenario_name == "Stable Load":
        cpu = 45.0 + np.random.normal(0, 2.0, duration)
        df = generate_synthetic_workload(duration, seed, base_cpu=45.0, burst_height=0.0, noise_std=2.0)
        df["cpu_utilization"] = np.clip(cpu, 10.0, 90.0)
        return df

    elif scenario_name == "Step Contention":
        # Constant ~40% then sudden surge to 95% at t=60
        df = generate_synthetic_workload(
            duration, seed, base_cpu=40.0, burst_start=60, burst_duration=40, burst_height=52.0, noise_std=2.5
        )
        return df

    elif scenario_name == "Periodic / Diurnal":
        # Clean diurnal sine wave
        sine = 30.0 * np.sin(2 * np.pi * timestamps / 35.0)
        cpu = 50.0 + sine + np.random.normal(0, 2.0, duration)
        df = generate_synthetic_workload(duration, seed, base_cpu=50.0, burst_height=0.0, noise_std=2.0)
        df["cpu_utilization"] = np.clip(cpu, 10.0, 95.0)
        return df

    elif scenario_name == "Bursty Traffic":
        # Random sharp micro-bursts
        base = 35.0 + np.random.normal(0, 3.0, duration)
        burst_points = [20, 45, 75, 95]
        for bp in burst_points:
            if bp < duration:
                span = min(duration - bp, 8)
                base[bp : bp + span] += 45.0
        df = generate_synthetic_workload(duration, seed, base_cpu=35.0, burst_height=0.0)
        df["cpu_utilization"] = np.clip(base, 10.0, 98.0)
        return df

    elif scenario_name == "Concept Drift":
        # First half: smooth low-frequency sine around 35%
        # Second half: sudden distribution shift to chaotic high-variance load
        cpu = np.zeros(duration)
        mid = duration // 2
        cpu[:mid] = 35.0 + 10.0 * np.sin(2 * np.pi * timestamps[:mid] / 20.0) + np.random.normal(0, 1.5, mid)
        cpu[mid:] = 75.0 + np.random.exponential(12.0, duration - mid)
        df = generate_synthetic_workload(duration, seed, base_cpu=35.0, burst_height=0.0)
        df["cpu_utilization"] = np.clip(cpu, 10.0, 99.0)
        return df

    elif scenario_name == "Noisy / Unpredictable":
        # High random white noise to trigger low confidence
        cpu = 50.0 + np.random.normal(0, 18.0, duration)
        df = generate_synthetic_workload(duration, seed, base_cpu=50.0, burst_height=0.0, noise_std=18.0)
        df["cpu_utilization"] = np.clip(cpu, 10.0, 95.0)
        return df

    elif scenario_name == "Presentation Demo":
        # Custom scenario matching requirement:
        # normal load -> predictable upward trend -> major burst -> stable high -> decline -> small burst
        cpu = np.zeros(duration)
        for t in range(duration):
            if t < 25:
                # Normal baseline
                cpu[t] = 35.0 + np.random.normal(0, 2.0)
            elif t < 55:
                # Predictable upward ramp (ML forecast picks up momentum)
                ramp = (t - 25) * 1.0
                cpu[t] = 35.0 + ramp + 4.0 * np.sin(t / 3.0) + np.random.normal(0, 1.5)
            elif t < 85:
                # Major burst
                cpu[t] = 88.0 + np.random.normal(0, 3.0)
            elif t < 105:
                # Decline
                cpu[t] = max(35.0, 88.0 - (t - 85) * 2.5) + np.random.normal(0, 2.0)
            else:
                # Small noisy burst
                cpu[t] = 55.0 + np.random.normal(0, 4.0)
        df = generate_synthetic_workload(duration, seed, base_cpu=35.0, burst_height=0.0)
        df["cpu_utilization"] = np.clip(cpu, 10.0, 98.0)
        return df

    else:
        return generate_synthetic_workload(duration, seed)
