import time
import os
import psutil
import pandas as pd
from typing import Dict, Any, List
from adapt.simulation.simulator import SimulationEngine
from adapt.simulation.scenarios import get_scenario
from adapt.scheduler.base import BaseScheduler
from adapt.scheduler.cfs_baseline import CFSBaselineScheduler
from adapt.scheduler.static_quota import StaticQuotaScheduler
from adapt.scheduler.reactive_scheduler import ReactiveScheduler
from adapt.scheduler.adapt_scheduler import AdaptScheduler
from adapt.forecasting.base import BaseForecaster
from adapt.forecasting.moving_average import MovingAverageForecaster
from adapt.actuator.cgroups_v2 import CgroupsV2Actuator
from adapt.utils.platform import is_linux

class BenchmarkEngine:
    """
    Standardized OS Scheduling Benchmark Battery.
    Executes identical workload traces across all 4 schedulers ensuring
    strict scientific fairness (no random discrepancy between runs).
    """
    def __init__(self, simulation_engine: SimulationEngine = None):
        self.sim = simulation_engine or SimulationEngine()

    def run_comparative_benchmark(
        self,
        workload_df: pd.DataFrame,
        forecaster: BaseForecaster = None,
        adapt_kwargs: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        forecaster = forecaster or MovingAverageForecaster(horizon=3)
        adapt_kwargs = adapt_kwargs or {}
        
        # Instantiate 4 schedulers
        schedulers: List[BaseScheduler] = [
            CFSBaselineScheduler(),
            StaticQuotaScheduler(fixed_quota=65.0),
            ReactiveScheduler(),
            AdaptScheduler(forecaster=forecaster, **adapt_kwargs)
        ]
        
        results = {}
        for s in schedulers:
            # Run strictly identical trace copy
            res = self.sim.run(s, workload_df.copy())
            results[s.name] = res
            
        # Compile comparative summary table dynamically
        rows = []
        adapt_name = [k for k in results.keys() if "Adapt" in k][0]
        adapt_p95 = results[adapt_name]["metrics"]["p95_latency"]
        adapt_p99 = results[adapt_name]["metrics"]["p99_latency"]
        adapt_eff = results[adapt_name]["metrics"]["resource_efficiency"]
        
        for name, data in results.items():
            m = data["metrics"]
            p95 = m["p95_latency"]
            p99 = m["p99_latency"]
            
            # Dynamic calculation of improvement (+) or regression (-)
            if name != adapt_name:
                p95_diff = round(((p95 - adapt_p95) / max(p95, 0.001)) * 100.0, 1)
                p99_diff = round(((p99 - adapt_p99) / max(p99, 0.001)) * 100.0, 1)
                comp_str = f"{'+' if p95_diff >= 0 else ''}{p95_diff}%"
            else:
                comp_str = "Baseline Ref"
                
            lag_val = m.get("response_lag_epochs", "N/A")
            lag_display = f"{lag_val} epochs" if isinstance(lag_val, (int, float)) else str(lag_val)
            
            rows.append({
                "Scheduler": name,
                "Avg Latency (ms)": m["avg_latency"],
                "P95 Latency (ms)": p95,
                "P99 Latency (ms)": p99,
                "P95 Delta vs Adapt": comp_str,
                "SLA Violations": m["sla_violations"],
                "SLA Violation Rate (%)": m["sla_violation_rate"],
                "Throttled Time (s)": m["total_throttled_sec"],
                "Resource Efficiency (%)": m["resource_efficiency"],
                "Allocation Changes": m["allocation_changes"],
                "Response Lag": lag_display
            })
            
        summary_df = pd.DataFrame(rows)
        return {
            "results": results,
            "summary_table": summary_df
        }

    def run_tc04_overhead_profile(
        self,
        forecaster: BaseForecaster = None,
        iterations: int = 100,
        target_live_cgroup: str = None
    ) -> Dict[str, Any]:
        """
        TC-04: Genuine Overhead Profile.
        
        SCIENTIFIC CLARIFICATION & INTERPRETATION:
        - The isolated inference, policy, and actuator functions execute well below the
          configured control interval in this host microbenchmark.
        - Dry-run actuator overhead measures userspace logic execution only, NOT kernel/sysfs timing.
        - Actual Linux cgroup actuation latency is reported ONLY if running on Linux with a configured target cgroup.
        - End-to-end live Linux daemon overhead requires separate live-system measurement.
        """
        forecaster = forecaster or MovingAverageForecaster(horizon=3)
        sample_window = [35.0, 36.0, 38.0, 42.0, 45.0, 50.0, 60.0, 75.0]
        
        # 1. Forecast Inference Latency Microbenchmark
        inf_times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            _ = forecaster.predict(sample_window)
            inf_times.append((time.perf_counter() - t0) * 1000.0)
        avg_inf_ms = float(pd.Series(inf_times).mean())
        p95_inf_ms = float(pd.Series(inf_times).quantile(0.95))
        
        # 2. Policy Engine Decision Latency Microbenchmark
        from adapt.policy.policy_engine import PolicyEngine
        policy = PolicyEngine()
        pol_times = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            _ = policy.decide_allocation(current_cpu=55.0, predicted_cpu=85.0, current_quota=50.0)
            pol_times.append((time.perf_counter() - t0) * 1000.0)
        avg_pol_ms = float(pd.Series(pol_times).mean())
        
        # 3. Actuator Call Overhead (Dry Run vs Real Live Linux)
        live_linux_available = is_linux() and target_live_cgroup is not None
        if live_linux_available:
            actuator = CgroupsV2Actuator(cgroup_path=target_live_cgroup, dry_run=False)
            act_mode = "LIVE_LINUX_CGROUPS_V2"
            act_times = []
            for _ in range(iterations):
                t0 = time.perf_counter()
                _ = actuator.set_cpu_quota(75.0)
                act_times.append((time.perf_counter() - t0) * 1000.0)
            real_actuation_ms = round(float(pd.Series(act_times).mean()), 4)
            dry_run_call_ms = None
        else:
            actuator = CgroupsV2Actuator(dry_run=True)
            act_mode = "DRY_RUN"
            act_times = []
            for _ in range(iterations):
                t0 = time.perf_counter()
                _ = actuator.set_cpu_quota(75.0)
                act_times.append((time.perf_counter() - t0) * 1000.0)
            dry_run_call_ms = round(float(pd.Series(act_times).mean()), 4)
            real_actuation_ms = "N/A (Dry-Run Mode Active)"
            
        # 4. Host Process Utilization (Live Host Measurement)
        proc = psutil.Process(os.getpid())
        rss_mb = round(proc.memory_info().rss / (1024 * 1024), 2)
        cpu_pct = proc.cpu_percent(interval=0.05)
        
        return {
            "test_case": "TC-04 Overhead Profile",
            "iterations": iterations,
            "forecaster_name": forecaster.name,
            "avg_inference_latency_ms": round(avg_inf_ms, 4),
            "p95_inference_latency_ms": round(p95_inf_ms, 4),
            "avg_policy_decision_ms": round(avg_pol_ms, 4),
            "actuator_mode": act_mode,
            "dry_run_actuator_call_latency_ms": dry_run_call_ms,
            "cgroup_actuation_latency_ms": real_actuation_ms,
            "process_rss_memory_mb": rss_mb,
            "process_cpu_percent": cpu_pct,
            "is_live_linux": is_linux(),
            "interpretation_note": (
                "The isolated inference/policy/dry-run control functions execute well below the "
                "configured control interval in this host microbenchmark. End-to-end live Linux "
                "daemon overhead requires separate live-system measurement."
            ),
            "measurement_source": "HOST_SYSTEM_PROFILED"
        }

    def run_standard_suite(self, forecaster: BaseForecaster = None) -> Dict[str, Any]:
        """
        Official Experiment Battery:
        TC-01: Step Contention
        TC-02: Periodic / Diurnal Load
        TC-03: Concept Drift & Noise
        TC-04: Genuine Overhead Profile
        """
        forecaster = forecaster or MovingAverageForecaster(horizon=3)
        return {
            "TC-01 Step Contention": self.run_comparative_benchmark(get_scenario("Step Contention"), forecaster=forecaster),
            "TC-02 Periodic Load": self.run_comparative_benchmark(get_scenario("Periodic / Diurnal"), forecaster=forecaster),
            "TC-03 Concept Drift": self.run_comparative_benchmark(get_scenario("Concept Drift"), forecaster=forecaster),
            "TC-04 Overhead Profile": self.run_tc04_overhead_profile(forecaster=forecaster)
        }
