import pytest
import numpy as np
import pandas as pd
import os

from adapt.datasets.sliding_window import create_sliding_windows, train_val_test_split_chronological
from adapt.datasets.synthetic import generate_synthetic_workload
from adapt.forecasting.naive import NaivePersistenceForecaster
from adapt.forecasting.moving_average import MovingAverageForecaster
from adapt.forecasting.exponential_smoothing import ExponentialSmoothingForecaster
from adapt.forecasting.arima_model import ARIMAForecaster
from adapt.forecasting.lstm_model import LSTMForecaster
from adapt.forecasting.gru_model import GRUForecaster
from adapt.forecasting.confidence import ConfidenceEstimator
from adapt.policy.policy_engine import PolicyEngine
from adapt.policy.safety_guard import SafetyGuard
from adapt.policy.drift_detector import ConceptDriftDetector
from adapt.policy.hysteresis import HysteresisController
from adapt.actuator.simulator import SimulatedActuator
from adapt.actuator.cgroups_v2 import CgroupsV2Actuator
from adapt.scheduler.cfs_baseline import CFSBaselineScheduler
from adapt.scheduler.static_quota import StaticQuotaScheduler
from adapt.scheduler.reactive_scheduler import ReactiveScheduler
from adapt.scheduler.adapt_scheduler import AdaptScheduler
from adapt.simulation.simulator import SimulationEngine
from adapt.simulation.scenarios import get_scenario
from adapt.evaluation.benchmark import BenchmarkEngine
from adapt.evaluation.metrics import evaluate_forecast, calculate_scheduler_metrics, calculate_control_response_lag
from adapt.evaluation.experiments import ExperimentLogger

def test_sliding_window_no_leakage():
    data = np.arange(20, dtype=float)
    X, y = create_sliding_windows(data, data, window_size=5, horizon=2)
    assert X[0].tolist() == [0.0, 1.0, 2.0, 3.0, 4.0]
    assert y[0] == 6.0
    assert X.shape == (14, 5)

def test_multivariate_sliding_window_shape():
    features = np.random.randn(50, 4)
    target = np.random.randn(50)
    X, y = create_sliding_windows(features, target, window_size=6, horizon=3)
    assert X.shape == (50 - 6 - 3 + 1, 6, 4)
    assert len(y) == X.shape[0]

def test_chronological_split():
    df = pd.DataFrame({"timestamp": np.arange(100), "cpu_utilization": np.arange(100)})
    train, val, test = train_val_test_split_chronological(df, 0.7, 0.15)
    assert len(train) == 70
    assert len(val) == 15
    assert len(test) == 15
    assert train["timestamp"].max() < val["timestamp"].min()
    assert val["timestamp"].max() < test["timestamp"].min()

def test_forecasting_models_output():
    window = np.array([30.0, 32.0, 35.0, 38.0, 42.0])
    naive = NaivePersistenceForecaster(horizon=2)
    assert naive.predict(window) == 42.0
    
    ma = MovingAverageForecaster(horizon=2, ma_window=3)
    assert abs(ma.predict(window) - np.mean([35.0, 38.0, 42.0])) < 1e-4

def test_confidence_estimator_heuristics():
    conf_est = ConfidenceEstimator(window_size=5, max_tolerated_error=20.0)
    assert conf_est.get_confidence() == 0.75
    
    for _ in range(5):
        conf_est.record_outcome(predicted=50.0, actual=51.0, previous_actual=48.0)
    assert conf_est.get_confidence() > 0.85
    
    for _ in range(5):
        conf_est.record_outcome(predicted=20.0, actual=80.0, previous_actual=20.0)
    assert conf_est.get_confidence() < 0.50

def test_concept_drift_detector():
    detector = ConceptDriftDetector(baseline_window=15, recent_window=4, drift_multiplier=2.0)
    for _ in range(12):
        detector.update(predicted=50.0, actual=52.0)
    assert detector.drift_detected is False
    
    for _ in range(5):
        detector.update(predicted=30.0, actual=95.0)
    assert detector.drift_detected is True

def test_policy_bounds_and_decisions():
    policy = PolicyEngine(low_threshold=30.0, high_threshold=70.0, critical_threshold=85.0)
    res = policy.decide_allocation(current_cpu=50.0, predicted_cpu=90.0, current_quota=50.0)
    assert res["is_critical"] is True
    assert res["decision"] == "PROACTIVE_CRITICAL_BOOST"
    assert res["target_quota"] >= 90.0
    assert res["target_quota"] <= 100.0

def test_safety_guard_fallback_episode_accounting():
    guard = SafetyGuard(confidence_threshold=0.6)
    safe, _ = guard.evaluate(predicted_cpu=60.0, confidence=0.85, drift_detected=False)
    assert safe is True
    assert guard.fallback_episodes == 0
    assert guard.fallback_ticks == 0
    
    safe, _ = guard.evaluate(predicted_cpu=60.0, confidence=0.40, drift_detected=False)
    assert safe is False
    assert guard.fallback_episodes == 1
    assert guard.fallback_ticks == 1
    
    safe, _ = guard.evaluate(predicted_cpu=60.0, confidence=0.35, drift_detected=False)
    assert safe is False
    assert guard.fallback_episodes == 1
    assert guard.fallback_ticks == 2
    
    safe, _ = guard.evaluate(predicted_cpu=60.0, confidence=0.80, drift_detected=False)
    assert safe is True
    assert guard.is_in_fallback is False

def test_hysteresis_suppresses_oscillation():
    hyst = HysteresisController(cooldown_ticks=3, minimum_change=8.0)
    assert hyst.should_apply_change(target_quota=70.0, current_quota=50.0) is True
    assert hyst.should_apply_change(target_quota=75.0, current_quota=70.0) is False
    assert hyst.should_apply_change(target_quota=75.0, current_quota=70.0) is False

def test_schedulers_identical_workload_comparability():
    df = get_scenario("Presentation Demo", duration=60, seed=42)
    bench = BenchmarkEngine()
    forecaster = MovingAverageForecaster(horizon=3)
    out = bench.run_comparative_benchmark(df, forecaster=forecaster)
    
    assert len(out["results"]) == 4
    for s_name, res in out["results"].items():
        assert len(res["timeseries"]) == 60
        assert np.allclose(res["timeseries"]["demand_cpu"], df["cpu_utilization"].values, atol=0.05)

# --- RESPONSE LAG TESTS (Point 1 requirements) ---

def test_control_response_lag_reactive_positive():
    # Workload surges at epoch 3 (demand jumps to 90)
    # Reactive scheduler increases allocation at epoch 5
    demands = [30.0, 30.0, 30.0, 90.0, 90.0, 90.0]
    allocations = [30.0, 30.0, 30.0, 30.0, 30.0, 90.0]
    decisions = ["NORMAL", "NORMAL", "NORMAL", "REACTIVE", "REACTIVE", "REACTIVE_QUOTA_INCREASE"]
    
    res = calculate_control_response_lag(demands, allocations, decisions=decisions, surge_threshold=70.0)
    assert res["surge_epoch"] == 3
    assert res["response_epoch"] == 5
    assert res["response_lag_epochs"] == 2.0
    assert res["response_type"] == "REACTIVE_RESPONSE"

def test_control_response_lag_proactive_negative():
    # Workload surges at epoch 5 (demand jumps to 90)
    # Adapt predicts burst at epoch 3 and pre-allocates headroom at epoch 4
    demands = [30.0, 30.0, 30.0, 40.0, 45.0, 90.0, 90.0]
    allocations = [30.0, 30.0, 30.0, 30.0, 90.0, 90.0, 90.0]
    decisions = ["NORMAL", "NORMAL", "NORMAL", "NORMAL", "PROACTIVE_SCALE_UP", "MAINTAIN", "MAINTAIN"]
    
    res = calculate_control_response_lag(demands, allocations, decisions=decisions, surge_threshold=70.0)
    assert res["surge_epoch"] == 5
    assert res["response_epoch"] == 4
    assert res["response_lag_epochs"] == -1.0
    assert res["response_type"] == "PROACTIVE_ANTICIPATION"

def test_control_response_lag_zero():
    # Workload surges at epoch 4 and proactive boost matches at epoch 4 exactly
    demands = [30.0, 30.0, 30.0, 30.0, 90.0, 90.0]
    allocations = [30.0, 30.0, 30.0, 30.0, 90.0, 90.0]
    decisions = ["NORMAL", "NORMAL", "NORMAL", "NORMAL", "PROACTIVE_CRITICAL_BOOST", "MAINTAIN"]
    
    res = calculate_control_response_lag(demands, allocations, decisions=decisions, surge_threshold=70.0)
    assert res["surge_epoch"] == 4
    assert res["response_epoch"] == 4
    assert res["response_lag_epochs"] == 0.0

def test_unrelated_earlier_allocation_does_not_create_negative_lag():
    # High allocation at epoch 0 (e.g. 95%) followed by normal (30%), then surge at epoch 12.
    # The unrelated allocation at epoch 0 must NOT be treated as a proactive response to surge at epoch 12!
    demands = [30.0]*12 + [90.0, 90.0, 90.0]
    allocations = [95.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 90.0, 90.0]
    decisions = ["NORMAL"] * 15
    decisions[13] = "REACTIVE_SCALE_UP"
    
    res = calculate_control_response_lag(demands, allocations, decisions=decisions, surge_threshold=70.0, search_window_before=4)
    assert res["surge_epoch"] == 12
    # Must pick the reactive response at epoch 13, NOT epoch 0
    assert res["response_epoch"] == 13
    assert res["response_lag_epochs"] == 1.0

def test_control_response_lag_no_response():
    # Fixed static quota that never increases to meet surge
    demands = [30.0, 30.0, 30.0, 90.0, 90.0, 90.0]
    allocations = [40.0, 40.0, 40.0, 40.0, 40.0, 40.0]
    decisions = ["STATIC_RESERVATION"] * 6
    
    res = calculate_control_response_lag(demands, allocations, decisions=decisions, surge_threshold=70.0, search_window_after=5)
    assert res["surge_epoch"] == 3
    assert res["response_epoch"] is None
    assert res["response_lag_epochs"] == "N/A"
    assert res["response_type"] == "UNRESOLVED_WITHIN_WINDOW"

# --- TC-04 OVERHEAD TESTS (Point 2 & 3 requirements) ---

def test_tc04_overhead_profiling():
    bench = BenchmarkEngine()
    prof = bench.run_tc04_overhead_profile(iterations=10)
    assert prof["avg_inference_latency_ms"] >= 0.0
    assert prof["avg_policy_decision_ms"] >= 0.0
    assert prof["process_rss_memory_mb"] > 0.0
    assert prof["actuator_mode"] == "DRY_RUN"
    assert prof["dry_run_actuator_call_latency_ms"] is not None
    assert "interpretation_note" in prof
    assert prof["measurement_source"] == "HOST_SYSTEM_PROFILED"

def test_actuator_dry_run_safety():
    cgroup = CgroupsV2Actuator(cgroup_path="/sys/fs/cgroup/fake_test", dry_run=True)
    assert cgroup.dry_run is True
    assert cgroup.set_cpu_quota(60.0) is True
    assert cgroup.set_cpu_weight(150) is True
    assert cgroup.current_quota == 60.0

def test_nan_prediction_handling():
    guard = SafetyGuard()
    safe, reason = guard.evaluate(predicted_cpu=float("nan"), confidence=0.9, drift_detected=False)
    assert safe is False
    assert "NAN" in reason

def test_inference_timeout_handling():
    guard = SafetyGuard(max_inference_latency_ms=10.0)
    safe, reason = guard.evaluate(predicted_cpu=50.0, confidence=0.9, drift_detected=False, inference_latency_ms=15.0)
    assert safe is False
    assert "TIMEOUT" in reason

def test_reproducibility():
    df1 = get_scenario("Presentation Demo", duration=50, seed=123)
    df2 = get_scenario("Presentation Demo", duration=50, seed=123)
    assert np.allclose(df1["cpu_utilization"].values, df2["cpu_utilization"].values)
