import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os

from adapt.datasets.synthetic import generate_synthetic_workload
from adapt.simulation.scenarios import get_scenario
from adapt.forecasting.naive import NaivePersistenceForecaster
from adapt.forecasting.moving_average import MovingAverageForecaster
from adapt.forecasting.exponential_smoothing import ExponentialSmoothingForecaster
from adapt.forecasting.arima_model import ARIMAForecaster
from adapt.forecasting.svr_model import SVRForecaster
from adapt.forecasting.rf_model import RandomForestForecaster
from adapt.forecasting.xgboost_model import XGBoostForecaster
from adapt.forecasting.lstm_model import LSTMForecaster
from adapt.forecasting.gru_model import GRUForecaster
from adapt.policy.policy_engine import PolicyEngine
from adapt.policy.safety_guard import SafetyGuard
from adapt.policy.drift_detector import ConceptDriftDetector
from adapt.policy.hysteresis import HysteresisController
from adapt.scheduler.cfs_baseline import CFSBaselineScheduler
from adapt.scheduler.static_quota import StaticQuotaScheduler
from adapt.scheduler.reactive_scheduler import ReactiveScheduler
from adapt.scheduler.adapt_scheduler import AdaptScheduler
from adapt.simulation.simulator import SimulationEngine
from adapt.evaluation.benchmark import BenchmarkEngine
from adapt.evaluation.experiments import ExperimentLogger
from adapt.evaluation.ablation import AblationStudyEngine
from adapt.datasets.loader import validate_and_normalize_trace

st.set_page_config(
    page_title="Adapt: Forecast-Driven OS Scheduling",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Styling
st.markdown("""
<style>
    .kpi-card {
        background-color: #1E232F;
        border: 1px solid #2D3748;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        margin-bottom: 12px;
    }
    .kpi-title {
        color: #A0AEC0;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .kpi-value {
        color: #63B3ED;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .badge-adapt {
        background-color: #2B6CB0;
        color: white;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: bold;
    }
    .badge-fallback {
        background-color: #C53030;
        color: white;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Navigation
page = st.sidebar.radio(
    "Navigation",
    [
        "1. System Overview",
        "2. Live Adapt Demo",
        "3. Forecasting Models",
        "4. Scheduler Comparison",
        "5. Experiment Lab",
        "6. Safety & Drift",
        "7. Multi-Tenant Mode",
        "8. Architecture",
        "9. Results & Export",
        "10. About Project"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("⚡ **Adapt OS Research Platform**")
st.sidebar.caption("Two-Tier Decoupled Scheduling Architecture")
st.sidebar.caption("Experiment Type: **SIMULATION (Safe Mode)**")

def get_forecaster(model_name: str, horizon: int = 3):
    if model_name == "Naive Persistence":
        return NaivePersistenceForecaster(horizon=horizon)
    elif model_name == "Moving Average":
        return MovingAverageForecaster(horizon=horizon)
    elif model_name == "Exponential Smoothing":
        return ExponentialSmoothingForecaster(horizon=horizon)
    elif model_name == "ARIMA":
        return ARIMAForecaster(horizon=horizon)
    elif model_name == "Support Vector Regression (SVR)":
        return SVRForecaster(horizon=horizon)
    elif model_name == "Random Forest":
        return RandomForestForecaster(horizon=horizon)
    elif model_name == "XGBoost":
        return XGBoostForecaster(horizon=horizon)
    elif model_name == "LSTM":
        return LSTMForecaster(horizon=horizon, epochs=5)
    elif model_name == "GRU":
        return GRUForecaster(horizon=horizon, epochs=5)
    return MovingAverageForecaster(horizon=horizon)

# -------------------------------------------------------------
# PAGE 1: SYSTEM OVERVIEW
# -------------------------------------------------------------
if page == "1. System Overview":
    st.title("⚡ Adapt: Forecast-Driven Intelligent Resource Management")
    st.subheader("A Proactive Multi-Tenant OS Scheduling Framework Using Time-Series ML and Decoupled Actuation")
    
    st.info("📌 **Scientific Note**: Simulator models reactive resource-control behavior surrounding fair CPU scheduling; it does not claim to reproduce every internal micro-state of Linux CFS.")

    st.markdown("""
    **Core OS Thesis**: Conventional resource-control policies are **reactive**: allocation adjustments occur *after* observed contention, run-queue buildup, and tail-latency spikes.
    **Adapt** decouples scheduling policy into a Tier-1 User-Space forecasting daemon that anticipates impending demand surges and proactively provisions CPU bandwidth via standard **cgroups v2** quotas *before* contention manifests.
    """)
    
    # Run dynamic comparison to compute live KPI delta rather than hardcoding
    workload = get_scenario("Presentation Demo", duration=100, seed=42)
    sim = SimulationEngine()
    forecaster = MovingAverageForecaster(horizon=3)
    
    adapt_sched = AdaptScheduler(forecaster=forecaster)
    react_sched = ReactiveScheduler()
    
    res_adapt = sim.run(adapt_sched, workload)
    res_react = sim.run(react_sched, workload)
    
    ts = res_adapt["timeseries"]
    metrics = res_adapt["metrics"]
    react_m = res_react["metrics"]
    
    # Dynamic Delta calculation (never hard-coded)
    p95_diff = round(metrics['p95_latency'] - react_m['p95_latency'], 2)
    p95_delta_str = f"{p95_diff} ms vs Reactive"
    sla_delta_str = f"{round(metrics['sla_violation_rate'] - react_m['sla_violation_rate'], 1)}% vs Reactive"
    
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Active Scheduler", "Adapt (Proactive)")
    c2.metric("P95 Latency", f"{metrics['p95_latency']} ms", p95_delta_str, delta_color="inverse")
    c3.metric("SLA Violation Rate", f"{metrics['sla_violation_rate']}%", sla_delta_str, delta_color="inverse")
    c4.metric("Resource Efficiency", f"{metrics['resource_efficiency']}%")
    c5.metric("Fallback Episodes", f"{metrics['fallback_events']}")

    st.markdown("### Workload Telemetry vs. Proactive Resource Allocation")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ts["timestamp"], y=ts["demand_cpu"], name="Workload Demand CPU %", line=dict(color="#4299E1", width=2)))
    fig.add_trace(go.Scatter(x=ts["timestamp"], y=ts["allocated_cpu"], name="Adapt Allocated CPU Quota %", line=dict(color="#48BB78", width=2, dash="dash")))
    fig.add_trace(go.Scatter(x=ts["timestamp"], y=ts["predicted_cpu"], name="Predicted Demand (t+3)", line=dict(color="#ECC94B", width=1.5, dash="dot")))
    
    # DATA-DRIVEN ANNOTATIONS: Derived from actual scheduler log events
    scale_up_events = ts[ts["decision"].str.contains("PROACTIVE", na=False)]
    for _, row in scale_up_events.iterrows():
        fig.add_annotation(
            x=row["timestamp"],
            y=row["allocated_cpu"],
            text=f"⚡ {row['decision']}",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#ECC94B"
        )
        
    fig.update_layout(title="Adapt Resource Provisioning Timeline (Data-Driven Events)", xaxis_title="Time Epoch (s)", yaxis_title="CPU Percentage (%)", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    c_left, c_right = st.columns(2)
    with c_left:
        fig_lat = px.line(ts, x="timestamp", y="latency_ms", title="Queuing & Service Latency Response (ms) [SIMULATED]", color_discrete_sequence=["#F56565"], template="plotly_dark")
        fig_lat.add_hline(y=45.0, line_dash="dot", line_color="orange", annotation_text="SLA Threshold (45ms)")
        st.plotly_chart(fig_lat, use_container_width=True)
    with c_right:
        fig_q = px.area(ts, x="timestamp", y="queue_size", title="OS Run-Queue Buildup [SIMULATED]", color_discrete_sequence=["#ED8936"], template="plotly_dark")
        st.plotly_chart(fig_q, use_container_width=True)

# -------------------------------------------------------------
# PAGE 2: LIVE ADAPT DEMO
# -------------------------------------------------------------
elif page == "2. Live Adapt Demo":
    st.title("🎯 Live Adapt Scheduling Demonstration")
    st.caption("Visually inspect how near-future ML forecasting prevents scheduling latency spikes.")

    colA, colB, colC = st.columns([1, 1, 1])
    with colA:
        scenario_choice = st.selectbox("Select Workload Scenario", [
            "Presentation Demo", "Step Contention", "Periodic / Diurnal", "Bursty Traffic", "Concept Drift", "Noisy / Unpredictable"
        ])
        scheduler_choice = st.selectbox("Select Operating Scheduler", [
            "Adapt (Proactive ML)", "Reactive Daemon", "CFS-Like Reactive Resource-Control", "Static Quota"
        ])
    with colB:
        model_choice = st.selectbox("Forecasting Model (for Adapt)", [
            "Moving Average", "Exponential Smoothing", "ARIMA", "Naive Persistence", "LSTM"
        ])
        horizon = st.slider("Prediction Horizon (epochs)", 1, 6, 3)
    with colC:
        enable_safety = st.checkbox("Enable Deterministic Safety Guard", value=True)
        enable_drift = st.checkbox("Enable Concept Drift Detector", value=True)
        run_demo_btn = st.button("▶ Run Live Demonstration", type="primary", use_container_width=True)

    if run_demo_btn or "last_demo_run" in st.session_state:
        st.session_state["last_demo_run"] = True
        workload_df = get_scenario(scenario_choice, duration=100, seed=42)
        sim = SimulationEngine()
        
        forecaster = get_forecaster(model_choice, horizon=horizon)
        if model_choice == "LSTM":
            X_w, y_w = workload_df["cpu_utilization"].values[:60], workload_df["cpu_utilization"].values[:60]
            forecaster.fit(X_w, y_w)
            
        guard = SafetyGuard(enabled=enable_safety)
        drift = ConceptDriftDetector() if enable_drift else None
        
        if scheduler_choice == "Adapt (Proactive ML)":
            sched = AdaptScheduler(forecaster=forecaster, safety_guard=guard, drift_detector=drift)
        elif scheduler_choice == "Reactive Daemon":
            sched = ReactiveScheduler()
        elif scheduler_choice == "Static Quota":
            sched = StaticQuotaScheduler(fixed_quota=65.0)
        else:
            sched = CFSBaselineScheduler()

        res = sim.run(sched, workload_df)
        ts = res["timeseries"]
        m = res["metrics"]

        # Status Banner
        if scheduler_choice == "Adapt (Proactive ML)":
            if sched.is_currently_fallback:
                st.error(f"⚠️ STATUS: SAFETY FALLBACK ENGAGED → REASON: {sched.fallback_reason}")
            else:
                st.success("⚡ STATUS: ADAPT ACTIVE (Proactive ML Control Engaged)")

        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("P95 Latency", f"{m['p95_latency']} ms")
        k2.metric("P99 Latency", f"{m['p99_latency']} ms")
        k3.metric("SLA Violations", f"{m['sla_violations']} ({m['sla_violation_rate']}%)")
        k4.metric("Resource Efficiency", f"{m['resource_efficiency']}%")
        k5.metric("Response Lag", f"{m['response_lag_epochs']} epochs")

        st.markdown("#### Demand vs. Allocation & Forecast")
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=ts["timestamp"], y=ts["demand_cpu"], name="Actual CPU Demand", line=dict(color="#4299E1", width=2)))
        fig1.add_trace(go.Scatter(x=ts["timestamp"], y=ts["allocated_cpu"], name="Allocated CPU Quota", line=dict(color="#48BB78", width=2, dash="dash")))
        if "predicted_cpu" in ts.columns and not ts["predicted_cpu"].isna().all():
            fig1.add_trace(go.Scatter(x=ts["timestamp"], y=ts["predicted_cpu"], name="Predicted Demand (t+k)", line=dict(color="#ECC94B", width=1.5, dash="dot")))
        fig1.update_layout(height=380, template="plotly_dark", xaxis_title="Time Epoch", yaxis_title="CPU (%)")
        st.plotly_chart(fig1, use_container_width=True)

        col_l, col_r = st.columns(2)
        with col_l:
            fig2 = px.line(ts, x="timestamp", y="latency_ms", title="Latency Profile (ms) [SIMULATED]", color_discrete_sequence=["#E53E3E"], template="plotly_dark")
            fig2.add_hline(y=45.0, line_dash="dot", line_color="orange")
            st.plotly_chart(fig2, use_container_width=True)
        with col_r:
            fig3 = px.line(ts, x="timestamp", y="confidence", title="Forecast Confidence Tracking", color_discrete_sequence=["#38B2AC"], template="plotly_dark")
            fig3.update_layout(yaxis_range=[0, 1.05])
            st.plotly_chart(fig3, use_container_width=True)

# -------------------------------------------------------------
# PAGE 3: FORECASTING MODELS
# -------------------------------------------------------------
elif page == "3. Forecasting Models":
    st.title("📈 Time-Series Resource Forecasting Comparative Analysis")
    st.caption("Benchmark 5 standard ML/DL forecasting algorithms (SVR, RF, XGBoost, LSTM, GRU) against the proposed Adapt statistical forecaster.")
    
    meta_path = "models/metadata/model_comparison.json"
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        cmp_df = pd.DataFrame(meta["results"])
        
        st.markdown("### Dynamic Rankings (Measured Empirically)")
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Lowest RMSE Model", meta.get("best_rmse_model", "N/A"))
        r2.metric("Lowest MAE Model", meta.get("best_mae_model", "N/A"))
        r3.metric("Fastest Model", meta.get("fastest_model", "N/A"))
        r4.metric("Best Directional Acc.", meta.get("best_directional_accuracy_model", "N/A"))

        st.markdown("### Empirical Benchmark Comparison")
        st.dataframe(cmp_df, use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1:
            fig_mae = px.bar(cmp_df, x="model", y="mae", title="Mean Absolute Error (MAE - Lower is Better)", color="mae", template="plotly_dark")
            st.plotly_chart(fig_mae, use_container_width=True)
        with c2:
            fig_lat = px.bar(cmp_df, x="model", y="inference_latency_ms", title="Inference Latency (ms - Lower is Better)", color="inference_latency_ms", template="plotly_dark")
            st.plotly_chart(fig_lat, use_container_width=True)

        # Explainable AI (SHAP) Section
        st.markdown("---")
        st.subheader("🔍 Explainable AI (XAI): SHAP Feature Attribution")
        st.caption("SHAP (SHapley Additive exPlanations) values computed on TreeSHAP model isolating individual telemetry feature contributions to future CPU demand predictions.")
        xai_summary = meta.get("xai_shap_summary", {})
        if "feature_shap_importance" in xai_summary:
            shap_data = xai_summary["feature_shap_importance"]
            shap_df = pd.DataFrame({
                "Feature": list(shap_data.keys()),
                "Mean |SHAP Value| (Importance)": list(shap_data.values())
            }).sort_values(by="Mean |SHAP Value| (Importance)", ascending=False)
            
            c_shap1, c_shap2 = st.columns([1, 1])
            with c_shap1:
                st.dataframe(shap_df, use_container_width=True)
            with c_shap2:
                fig_shap = px.bar(shap_df, x="Mean |SHAP Value| (Importance)", y="Feature", orientation="h",
                                  title="Feature Importance Ranking via SHAP", color="Mean |SHAP Value| (Importance)",
                                  template="plotly_dark")
                fig_shap.update_layout(yaxis=dict(autorange="reversed"))
                st.plotly_chart(fig_shap, use_container_width=True)

        # Component Ablation Study Section
        st.markdown("---")
        st.subheader("🔬 Component Ablation Study")
        st.caption("Evaluates system performance when isolating individual architectural components (Hysteresis, Safety Guard, Headroom Buffer).")
        if st.button("▶ Run Live Ablation Study Benchmark", type="secondary"):
            ablation_engine = AblationStudyEngine()
            ablation_df = ablation_engine.run_ablation(duration=100)
            st.dataframe(ablation_df, use_container_width=True)
            
            col_ab1, col_ab2 = st.columns(2)
            with col_ab1:
                fig_ab_lat = px.bar(ablation_df, x="Configuration", y="P99 Latency (ms)", title="P99 Latency Impact Across Ablation Variants", color="P99 Latency (ms)", template="plotly_dark")
                st.plotly_chart(fig_ab_lat, use_container_width=True)
            with col_ab2:
                fig_ab_thr = px.bar(ablation_df, x="Configuration", y="Allocation Changes (Thrash)", title="Actuator Thrashing (Allocation Changes)", color="Allocation Changes (Thrash)", template="plotly_dark")
                st.plotly_chart(fig_ab_thr, use_container_width=True)
    else:
        st.info("Run `python3 scripts/train_models.py` to train models and generate the dynamic ranking metadata.")

# -------------------------------------------------------------
# PAGE 4: SCHEDULER COMPARISON
# -------------------------------------------------------------
elif page == "4. Scheduler Comparison":
    st.title("⚖️ Comprehensive Multi-Scheduler Benchmark Comparison")
    st.markdown("Fair scientific comparison: all 4 schedulers are subjected to the **exact same workload trace**.")

    sc_name = st.selectbox("Select Benchmark Scenario for Comparison", [
        "Presentation Demo", "Step Contention", "Periodic / Diurnal", "Concept Drift", "Bursty Traffic"
    ])
    
    if st.button("⚡ Run Comparative Suite Across 4 Schedulers", type="primary"):
        workload = get_scenario(sc_name, duration=100, seed=42)
        forecaster = MovingAverageForecaster(horizon=3)
        bench = BenchmarkEngine()
        bench_out = bench.run_comparative_benchmark(workload, forecaster=forecaster)
        
        st.markdown("### Comparative Results Table")
        st.dataframe(bench_out["summary_table"], use_container_width=True)
        
        fig_comp = go.Figure()
        for name, data in bench_out["results"].items():
            ts = data["timeseries"]
            fig_comp.add_trace(go.Scatter(x=ts["timestamp"], y=ts["latency_ms"], name=f"{name} Latency", mode="lines"))
        fig_comp.add_hline(y=45.0, line_dash="dot", line_color="orange", annotation_text="SLA Bound (45ms)")
        fig_comp.update_layout(title="Latency Comparison Across Schedulers (ms) [SIMULATED]", template="plotly_dark", yaxis_title="Latency (ms)", xaxis_title="Epoch (s)")
        st.plotly_chart(fig_comp, use_container_width=True)

# -------------------------------------------------------------
# PAGE 5: EXPERIMENT LAB
# -------------------------------------------------------------
elif page == "5. Experiment Lab":
    st.title("🔬 Experiment Lab & CSV Import")
    st.caption("Upload arbitrary custom traces or parameterize controlled experiments.")

    uploaded_file = st.file_uploader("Upload Workload Trace (CSV)", type=["csv"])
    if uploaded_file is not None:
        try:
            raw_df = pd.read_csv(uploaded_file)
            trace_df = validate_and_normalize_trace(raw_df)
            st.success(f"Successfully loaded and validated CSV trace ({len(trace_df)} rows).")
            st.line_chart(trace_df["cpu_utilization"])
        except Exception as e:
            st.error(f"Error parsing uploaded trace: {e}")

    st.markdown("### Run Controlled Experiment")
    col1, col2 = st.columns(2)
    with col1:
        exp_scenario = st.selectbox("Scenario", ["Step Contention", "Periodic / Diurnal", "Presentation Demo", "Concept Drift"])
        exp_duration = st.slider("Duration (seconds)", 60, 240, 100)
    with col2:
        exp_model = st.selectbox("Model", ["Moving Average", "Exponential Smoothing", "Naive Persistence", "ARIMA"])
        exp_notes = st.text_input("Experiment Notes", "Controlled test")

    if st.button("Save & Run Experiment"):
        workload = get_scenario(exp_scenario, duration=exp_duration)
        forecaster = get_forecaster(exp_model)
        sim = SimulationEngine()
        adapt_sched = AdaptScheduler(forecaster=forecaster)
        out = sim.run(adapt_sched, workload)
        
        logger = ExperimentLogger()
        import uuid
        exp_id = f"EXP_{uuid.uuid4().hex[:6].upper()}"
        saved_dir = logger.save_experiment(
            exp_id=exp_id,
            config={"scenario": exp_scenario, "duration": exp_duration, "model": exp_model, "scheduler": "Adapt", "result_source": "SIMULATION"},
            scheduler_metrics=out["metrics"],
            timeseries_df=out["timeseries"],
            notes=exp_notes
        )
        st.success(f"Experiment saved to `{saved_dir}`!")
        st.json(out["metrics"])

# -------------------------------------------------------------
# PAGE 6: SAFETY & DRIFT
# -------------------------------------------------------------
elif page == "6. Safety & Drift":
    st.title("🛡️ Safety Guard & Concept Drift Monitor")
    st.markdown("""
    Adapt guarantees OS stability by treating machine learning strictly as an advisory user-space signal.
    Deterministic safety rules trigger **immediate fallback to standard reactive baseline** whenever:
    - Model Confidence < Threshold (default 0.60)
    - Concept Drift detected (residual variance surge > 2.2x)
    - Inference latency times out (> 50ms)
    - Prediction produces NaN, Inf, or invalid out-of-range bounds
    """)

    drift_workload = get_scenario("Concept Drift", duration=100, seed=42)
    sim = SimulationEngine()
    forecaster = MovingAverageForecaster(horizon=3)
    guard = SafetyGuard(confidence_threshold=0.6)
    drift = ConceptDriftDetector(drift_multiplier=2.0)
    adapt_sched = AdaptScheduler(forecaster=forecaster, safety_guard=guard, drift_detector=drift)
    
    out = sim.run(adapt_sched, drift_workload)
    ts = out["timeseries"]

    st.markdown("### Concept Drift Stress Test Timeline")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ts["timestamp"], y=ts["demand_cpu"], name="Workload Demand", line=dict(color="#4299E1")))
    fig.add_trace(go.Scatter(x=ts["timestamp"], y=ts["allocated_cpu"], name="Quota Allocation", line=dict(color="#48BB78", dash="dash")))
    
    fallback_points = ts[ts["is_fallback"] == True]
    if not fallback_points.empty:
        fig.add_trace(go.Scatter(
            x=fallback_points["timestamp"],
            y=fallback_points["allocated_cpu"],
            mode="markers",
            name="Fallback Active (Safety Triggered)",
            marker=dict(color="red", size=8, symbol="x")
        ))
    fig.update_layout(template="plotly_dark", title="Automatic Fallback Activation During Distribution Shift")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------------
# PAGE 7: MULTI-TENANT MODE
# -------------------------------------------------------------
elif page == "7. Multi-Tenant Mode":
    st.title("👥 Multi-Tenant Resource Contention")
    st.markdown("""
    Proportional fair allocation across competing tenants sharing finite CPU bandwidth:
    - **Tenant A**: Latency-sensitive microservice (High SLA priority)
    - **Tenant B**: Batch processing job (Medium priority)
    - **Tenant C**: Background maintenance worker (Low priority)
    """)
    from adapt.datasets.synthetic import generate_multi_tenant_workloads
    mt = generate_multi_tenant_workloads(duration_seconds=100)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=mt["tenant_A"]["timestamp"], y=mt["tenant_A"]["cpu_utilization"], name="Tenant A (Latency-Sensitive)", line=dict(color="#63B3ED")))
    fig.add_trace(go.Scatter(x=mt["tenant_B"]["timestamp"], y=mt["tenant_B"]["cpu_utilization"], name="Tenant B (Batch)", line=dict(color="#F6AD55")))
    fig.add_trace(go.Scatter(x=mt["tenant_C"]["timestamp"], y=mt["tenant_C"]["cpu_utilization"], name="Tenant C (Background)", line=dict(color="#9AE6B4")))
    fig.update_layout(template="plotly_dark", title="Simultaneous Multi-Tenant CPU Demand Profiles", yaxis_title="Demand (%)", xaxis_title="Epoch (s)")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------------
# PAGE 8: ARCHITECTURE
# -------------------------------------------------------------
elif page == "8. Architecture":
    st.title("🏛️ Two-Tier Decoupled Architecture")
    st.markdown("""
    ```
    +-------------------------------------------------------------------------------+
    |                           TIER 1 - USER-SPACE DAEMON                         |
    |                                                                               |
    |   [Telemetry Collector]                                                       |
    |            |                                                                  |
    |            v                                                                  |
    |   [Sliding Window Buffer] (e.g., 12 epochs)                                   |
    |            |                                                                  |
    |            v                                                                  |
    |   [Time-Series Forecaster] (LSTM / GRU / ARIMA / Moving Average)             |
    |            |                                                                  |
    |            +-----------------------+                                          |
    |            |                       |                                          |
    |            v                       v                                          |
    |   [Predicted Demand t+k]   [Confidence & Drift Evaluator]                     |
    |            |                       |                                          |
    |            +-----------+-----------+                                          |
    |                        |                                                      |
    |                        v                                                      |
    |               [Deterministic Safety Guard] ---> (If unsafe: Engage Fallback)  |
    |                        |                                                      |
    |                        v                                                      |
    |               [OS Policy Engine & Hysteresis Controller]                      |
    +------------------------|------------------------------------------------------+
                             | Standard Linux cgroup sysfs calls (cpu.max, cpu.weight)
                             v
    +-------------------------------------------------------------------------------+
    |                           TIER 2 - LINUX KERNEL                               |
    |                                                                               |
    |   [cgroups v2 Controller: /sys/fs/cgroup/adapt.slice/cpu.max]                |
    |            |                                                                  |
    |            v                                                                  |
    |   [Linux CFS / EEVDF Hot-Path Scheduler]                                      |
    |            |                                                                  |
    |            v                                                                  |
    |   [Hardware CPU Cores Execution]                                              |
    +-------------------------------------------------------------------------------+
    ```
    """)

# -------------------------------------------------------------
# PAGE 9: RESULTS & EXPORT
# -------------------------------------------------------------
elif page == "9. Results & Export":
    st.title("📊 Results & Artifact Export")
    st.markdown("Download reproducible benchmark data and experiment summaries.")
    
    workload = get_scenario("Presentation Demo", duration=100, seed=42)
    forecaster = MovingAverageForecaster(horizon=3)
    bench = BenchmarkEngine()
    bench_out = bench.run_comparative_benchmark(workload, forecaster=forecaster)
    summary_df = bench_out["summary_table"]
    
    st.dataframe(summary_df, use_container_width=True)
    csv_bytes = summary_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Benchmark Table (CSV)", csv_bytes, "adapt_benchmark_results.csv", "text/csv")
    
    st.markdown("### TC-04 Overhead Profiling")
    if st.button("Run Live Host Overhead Profile"):
        prof = bench.run_tc04_overhead_profile(forecaster=forecaster)
        st.json(prof)

# -------------------------------------------------------------
# PAGE 10: ABOUT PROJECT
# -------------------------------------------------------------
elif page == "10. About Project":
    st.title("ℹ️ About Adapt")
    st.markdown("""
    ### Project Title
    **Adapt: Forecast-Driven Intelligent Resource Management for Operating Systems**
    
    *Subtitle: A Proactive Multi-Tenant OS Scheduling Framework Using Time-Series ML and Decoupled Actuation*

    ### Academic & Engineering Objective
    This university Project-Based Learning (PBL) research prototype bridges Operating Systems, Resource Management, and Time-Series Machine Learning.
    
    ### Research Integrity Declarations
    - All simulation outputs are explicitly labeled **SIMULATED**.
    - Fair comparison guarantee: Schedulers execute on identical trace sequences.
    - Confidence scores represent empirical engineering heuristics, not Bayesian posterior probabilities.
    - Results and metrics are calculated dynamically without hard-coded numbers.
    """)
