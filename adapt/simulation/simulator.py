import numpy as np
import pandas as pd
from typing import Dict, Any, List
from adapt.scheduler.base import BaseScheduler
from adapt.evaluation.metrics import calculate_scheduler_metrics

class SimulationEngine:
    """
    Discrete-Time Operating System Resource Simulator.
    Models CPU bandwidth allocation, queue pressure, throttling events,
    and simulated queuing latency.
    
    LATENCY MATHEMATICAL MODEL:
    When CPU demand exceeds allocated capacity:
       Excess(t) = max(0.0, demand(t) - allocated_capacity(t))
       Run-queue accumulates excess: Q(t) = max(0.0, Q(t-1) * queue_drain_rate + Excess(t))
       Throttling occurs: throttled_sec = 1.0 (full epoch)
       Simulated Latency:
          L(t) = Base_Latency + (Q(t) / max(allocated_capacity(t), 10.0)) * Latency_Scale
    When allocated capacity >= demand:
       Run-queue drains naturally and latency returns toward baseline.
    """
    def __init__(
        self,
        base_latency_ms: float = 8.0,
        latency_scale: float = 65.0,
        queue_drain_rate: float = 0.5,
        sla_threshold_ms: float = 45.0,
        surge_threshold: float = 65.0
    ):
        self.base_latency_ms = base_latency_ms
        self.latency_scale = latency_scale
        self.queue_drain_rate = queue_drain_rate
        self.sla_threshold_ms = sla_threshold_ms
        self.surge_threshold = surge_threshold

    def run(
        self,
        scheduler: BaseScheduler,
        workload_df: pd.DataFrame
    ) -> Dict[str, Any]:
        scheduler.reset()
        records = []
        
        queue_size = 0.0
        
        for epoch, row in workload_df.iterrows():
            demand = float(row["cpu_utilization"])
            
            # Step 1: Scheduler decides allocation for current epoch
            sched_res = scheduler.schedule(demand, int(epoch))
            allocated_cpu = float(sched_res["allocated_cpu"])
            decision = sched_res.get("decision", "NORMAL")
            is_fallback = sched_res.get("is_fallback", False)
            predicted_cpu = sched_res.get("predicted_cpu", None)
            confidence = sched_res.get("confidence", 1.0)
            safety_reason = sched_res.get("safety_reason", "SAFE")
            
            # Step 2: Served CPU and Queue physics
            served_cpu = min(demand, allocated_cpu)
            deficit = max(0.0, demand - allocated_cpu)
            
            if deficit > 0:
                throttled_sec = 1.0
                throttled_demand = deficit
                queue_size += deficit
            else:
                throttled_sec = 0.0
                throttled_demand = 0.0
                queue_size = max(0.0, queue_size * self.queue_drain_rate)
                
            # Step 3: Latency computation (SIMULATED)
            queue_delay = (queue_size / max(allocated_cpu, 10.0)) * self.latency_scale
            latency_ms = self.base_latency_ms + queue_delay
            
            records.append({
                "timestamp": int(row.get("timestamp", epoch)),
                "demand_cpu": round(demand, 2),
                "allocated_cpu": round(allocated_cpu, 2),
                "served_cpu": round(served_cpu, 2),
                "queue_size": round(queue_size, 2),
                "throttled_sec": throttled_sec,
                "throttled_demand": round(throttled_demand, 2),
                "latency_ms": round(latency_ms, 2),
                "predicted_cpu": round(predicted_cpu, 2) if predicted_cpu is not None else np.nan,
                "confidence": round(confidence, 3) if confidence is not None else 1.0,
                "decision": decision,
                "is_fallback": is_fallback,
                "safety_reason": safety_reason
            })
            
        timeseries_df = pd.DataFrame(records)
        
        # Calculate summary metrics with event-associated decisions
        fallback_ticks = int(timeseries_df["is_fallback"].sum())
        fallback_events = getattr(scheduler, "fallback_count", 0)
        
        metrics = calculate_scheduler_metrics(
            latencies=timeseries_df["latency_ms"].tolist(),
            throttling_durations=timeseries_df["throttled_sec"].tolist(),
            throttled_demands=timeseries_df["throttled_demand"].tolist(),
            allocations=timeseries_df["allocated_cpu"].tolist(),
            demands=timeseries_df["demand_cpu"].tolist(),
            decisions=timeseries_df["decision"].tolist(),
            sla_threshold=self.sla_threshold_ms,
            allocation_change_events=scheduler.allocation_changes,
            fallback_events=fallback_events,
            fallback_ticks=fallback_ticks,
            surge_threshold=self.surge_threshold
        )
        
        return {
            "scheduler_name": scheduler.name,
            "metrics": metrics,
            "timeseries": timeseries_df
        }
