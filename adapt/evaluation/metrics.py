import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from typing import Dict, Any, List, Optional, Union

def calculate_mape_safe(actual: np.ndarray, predicted: np.ndarray, epsilon: float = 1.0) -> float:
    """Calculates MAPE with zero-division safeguard."""
    actual, predicted = np.array(actual), np.array(predicted)
    safe_actual = np.where(np.abs(actual) < epsilon, epsilon, actual)
    return float(np.mean(np.abs((actual - predicted) / safe_actual)) * 100.0)

def calculate_directional_accuracy(actual: np.ndarray, predicted: np.ndarray) -> float:
    """
    Directional Accuracy: Percentage of times the forecast correctly anticipated
    the upward or downward direction of change relative to the preceding step.
    actual(t) vs actual(t-1) and predicted(t) vs actual(t-1).
    """
    if len(actual) < 2:
        return 100.0
    actual_diff = np.diff(actual)
    pred_diff = predicted[1:] - actual[:-1]
    
    matches = (actual_diff * pred_diff) >= 0
    return float(np.mean(matches) * 100.0)

def evaluate_forecast(actual: np.ndarray, predicted: np.ndarray) -> Dict[str, float]:
    actual = np.array(actual, dtype=float)
    predicted = np.array(predicted, dtype=float)
    
    mae = float(mean_absolute_error(actual, predicted))
    rmse = float(np.sqrt(mean_squared_error(actual, predicted)))
    r2 = float(r2_score(actual, predicted)) if len(actual) > 1 and np.var(actual) > 1e-4 else 0.0
    mape = calculate_mape_safe(actual, predicted)
    da = calculate_directional_accuracy(actual, predicted)
    
    return {
        "mae": round(mae, 3),
        "rmse": round(rmse, 3),
        "r2": round(r2, 3),
        "mape": round(mape, 2),
        "directional_accuracy": round(da, 2)
    }

def calculate_control_response_lag(
    demands: list[float],
    allocations: list[float],
    decisions: Optional[list[str]] = None,
    surge_threshold: float = 65.0,
    search_window_before: int = 4,
    search_window_after: int = 15
) -> Dict[str, Any]:
    """
    Event-Associated Control Response Lag Measurement.
    
    Evaluates response latency associated with a distinct workload surge event.
    
    Procedure:
    1. Detect surge onset: first epoch where demand crosses surge_threshold AND demand increases.
    2. Define target capacity: target = demand[t_surge] * 0.90.
    3. Bounded Event Window: search within [t_surge - search_window_before, t_surge + search_window_after].
    4. Proactive check: Negative response lag is permitted ONLY IF an explicit proactive scale-up
       decision occurred within the bounded pre-surge window [t_surge - search_window_before, t_surge)
       that brought allocation to sufficient capacity. Unrelated earlier high allocation long before
       t_surge is explicitly rejected.
    5. Reactive check: If no proactive response, finds first epoch t >= t_surge where allocation
       reaches target capacity.
    6. If no allocation catches up within the bounded window, returns N/A (unresolved).
    """
    dems = np.array(demands, dtype=float)
    allocs = np.array(allocations, dtype=float)
    decs = decisions if decisions is not None else ["NORMAL"] * len(demands)
    
    # 1. Identify surge onset epoch
    # Surge criteria: demand crosses threshold and increases over previous epoch
    surge_candidates = []
    for t in range(len(dems)):
        if dems[t] >= surge_threshold:
            prev_d = dems[t-1] if t > 0 else 0.0
            if dems[t] > prev_d:
                surge_candidates.append(t)
                break  # Primary surge event
                
    if not surge_candidates:
        return {
            "surge_epoch": None,
            "response_epoch": None,
            "response_lag_epochs": "N/A",
            "response_type": "NO_SURGE_DETECTED",
            "associated_decision": "NONE"
        }
        
    t_surge = surge_candidates[0]
    target_capacity = dems[t_surge] * 0.90
    
    # Check baseline allocation immediately prior to pre-surge window
    t_window_start = max(0, t_surge - search_window_before)
    t_window_end = min(len(dems) - 1, t_surge + search_window_after)
    
    # 4. Check Proactive Response within pre-surge window [t_window_start, t_surge)
    proactive_epoch = None
    for t in range(t_window_start, t_surge):
        dec = str(decs[t]).upper()
        # Must have an explicit proactive scale-up / boost decision
        if "PROACTIVE" in dec and ("BOOST" in dec or "SCALE_UP" in dec or "CRITICAL" in dec):
            if allocs[t] >= target_capacity:
                proactive_epoch = t
                break
            elif t + 1 <= t_surge and allocs[t + 1] >= target_capacity:
                proactive_epoch = t + 1
                break
                
    if proactive_epoch is not None:
        lag = float(proactive_epoch - t_surge)  # Negative or zero
        return {
            "surge_epoch": int(t_surge),
            "response_epoch": int(proactive_epoch),
            "response_lag_epochs": lag,
            "response_type": "PROACTIVE_ANTICIPATION",
            "associated_decision": str(decs[proactive_epoch if proactive_epoch < len(decs) else t_surge])
        }
        
    # Check exact zero-lag: allocation at t_surge meets target with proactive boost
    if allocs[t_surge] >= target_capacity:
        dec_at_surge = str(decs[t_surge]).upper()
        if "PROACTIVE" in dec_at_surge:
            return {
                "surge_epoch": int(t_surge),
                "response_epoch": int(t_surge),
                "response_lag_epochs": 0.0,
                "response_type": "PROACTIVE_AT_SURGE",
                "associated_decision": dec_at_surge
            }
            
    # 5. Check Reactive Response within [t_surge, t_window_end]
    reactive_epoch = None
    for t in range(t_surge, t_window_end + 1):
        if allocs[t] >= target_capacity:
            reactive_epoch = t
            break
            
    if reactive_epoch is not None:
        lag = float(reactive_epoch - t_surge)
        dec_resp = str(decs[reactive_epoch])
        return {
            "surge_epoch": int(t_surge),
            "response_epoch": int(reactive_epoch),
            "response_lag_epochs": lag,
            "response_type": "REACTIVE_RESPONSE" if lag > 0 else "CONCURRENT_ALLOCATION",
            "associated_decision": dec_resp
        }
        
    # 6. Unresolved / No adequate response within bounded window
    return {
        "surge_epoch": int(t_surge),
        "response_epoch": None,
        "response_lag_epochs": "N/A",
        "response_type": "UNRESOLVED_WITHIN_WINDOW",
        "associated_decision": "NONE"
    }

def calculate_scheduler_metrics(
    latencies: list[float],
    throttling_durations: list[float],
    throttled_demands: list[float],
    allocations: list[float],
    demands: list[float],
    decisions: Optional[list[str]] = None,
    sla_threshold: float = 45.0,
    allocation_change_events: int = 0,
    fallback_events: int = 0,
    fallback_ticks: int = 0,
    surge_threshold: float = 65.0
) -> Dict[str, Any]:
    """Calculates holistic OS scheduling performance and resource efficiency metrics."""
    lats = np.array(latencies, dtype=float)
    allocs = np.array(allocations, dtype=float)
    dems = np.array(demands, dtype=float)
    
    avg_latency = float(np.mean(lats))
    p50_latency = float(np.percentile(lats, 50))
    p90_latency = float(np.percentile(lats, 90))
    p95_latency = float(np.percentile(lats, 95))
    p99_latency = float(np.percentile(lats, 99))
    max_latency = float(np.max(lats))
    
    sla_violations = int(np.sum(lats > sla_threshold))
    sla_violation_rate = round(float(sla_violations / len(lats) * 100.0), 2) if len(lats) > 0 else 0.0
    
    total_throttled_sec = float(np.sum(throttling_durations))
    total_throttled_demand = float(np.sum(throttled_demands))
    
    avg_allocation = float(np.mean(allocs))
    peak_allocation = float(np.max(allocs))
    
    # Resource efficiency formula: Useful served demand / Allocated capacity
    # Reflects over-provisioning waste vs under-provisioning starvation
    safe_allocs = np.where(allocs <= 0.0, 1.0, allocs)
    utilized_ratio = np.minimum(dems, allocs) / safe_allocs
    resource_efficiency = float(np.mean(utilized_ratio) * 100.0)
    
    lag_dict = calculate_control_response_lag(
        demands, allocations, decisions=decisions, surge_threshold=surge_threshold
    )
    
    return {
        "avg_latency": round(avg_latency, 2),
        "p50_latency": round(p50_latency, 2),
        "p90_latency": round(p90_latency, 2),
        "p95_latency": round(p95_latency, 2),
        "p99_latency": round(p99_latency, 2),
        "max_latency": round(max_latency, 2),
        "sla_violations": sla_violations,
        "sla_violation_rate": sla_violation_rate,
        "total_throttled_sec": round(total_throttled_sec, 2),
        "total_throttled_demand": round(total_throttled_demand, 2),
        "avg_allocation": round(avg_allocation, 2),
        "peak_allocation": round(peak_allocation, 2),
        "resource_efficiency": round(resource_efficiency, 2),
        "allocation_changes": allocation_change_events,
        "fallback_events": fallback_events,
        "fallback_ticks": fallback_ticks,
        "response_lag_epochs": lag_dict["response_lag_epochs"],
        "response_lag_details": lag_dict
    }
