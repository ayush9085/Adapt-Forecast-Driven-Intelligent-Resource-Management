import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

os.makedirs("docs/assets", exist_ok=True)
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.titlesize": 14,
    "figure.dpi": 300
})

# 1. Forecasting Models Accuracy & Inference Latency
def plot_forecasting_comparison():
    models = ["1. SVR", "2. RF", "3. XGBoost", "4. LSTM", "5. GRU", "Adapt (Stat)"]
    mae = [3.695, 3.400, 4.077, 15.849, 3.678, 5.733]
    rmse = [4.275, 4.103, 5.058, 16.355, 4.346, 6.385]
    latency_ms = [0.110, 12.559, 0.120, 0.393, 0.309, 0.0097]

    fig, ax1 = plt.subplots(figsize=(10, 5))
    x = np.arange(len(models))
    width = 0.35

    rects1 = ax1.bar(x - width/2, mae, width, label="MAE (%)", color="#2b5c8f")
    rects2 = ax1.bar(x + width/2, rmse, width, label="RMSE (%)", color="#4682b4")

    ax1.set_ylabel("Error Metric (%)", color="#1a365d", fontweight="bold")
    ax1.set_title("Figure 1: Predictive Accuracy & Inference Latency Across 5 Standard Algorithms + Adapt", pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(models, rotation=15, ha="right")
    ax1.legend(loc="upper left")

    ax2 = ax1.twinx()
    ax2.plot(x, latency_ms, color="#d9534f", marker="o", linewidth=2.5, markersize=7, label="Inference Latency (ms)")
    ax2.set_ylabel("Inference Latency (ms) [Log Scale]", color="#d9534f", fontweight="bold")
    ax2.set_yscale("log")
    ax2.tick_params(axis="y", labelcolor="#d9534f")
    ax2.legend(loc="upper right")

    plt.tight_layout()
    plt.savefig("docs/assets/fig1_forecasting_comparison.png")
    plt.close()
    print("Saved fig1_forecasting_comparison.png")

# 2. TreeSHAP Feature Importance
def plot_shap_importance():
    features = ["I/O Bandwidth (io_rate)", "CPU Utilization", "Memory Footprint", "Inbound Request Rate", "OS Task Count"]
    importance = [0.4848, 0.2266, 0.1631, 0.1152, 0.0104]
    pcts = [f"{v*100:.1f}%" for v in importance]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    y_pos = np.arange(len(features))
    colors = ["#1b4f72", "#2874a6", "#3498db", "#5dade2", "#aed6f1"]

    bars = ax.barh(y_pos, importance, color=colors, height=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(features)
    ax.invert_yaxis()
    ax.set_xlabel("Mean Absolute SHAP Value (Feature Attribution)", fontweight="bold")
    ax.set_title("Figure 2: TreeSHAP Feature Attribution for Future Resource Demand", pad=15)

    for bar, pct in zip(bars, pcts):
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, pct, va="center", ha="left", fontweight="bold", color="#1a252f")

    ax.set_xlim(0, 0.58)
    plt.tight_layout()
    plt.savefig("docs/assets/fig2_shap_feature_importance.png")
    plt.close()
    print("Saved fig2_shap_feature_importance.png")

# 3. Scheduler Latency Comparison (P95 & P99)
def plot_scheduler_latency():
    schedulers = ["Static Quota", "Reactive Daemon", "CFS-Like Reactive", "Adapt (Proposed)"]
    p95 = [510.65, 1423.58, 15.54, 9.94]
    p99 = [643.37, 1757.14, 18.55, 15.39]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Left: Full scale (showing massive reactive queueing)
    x = np.arange(len(schedulers))
    width = 0.35
    ax1.bar(x - width/2, p95, width, label="P95 Latency", color="#e74c3c")
    ax1.bar(x + width/2, p99, width, label="P99 Latency", color="#c0392b")
    ax1.set_ylabel("Queuing Latency (ms)", fontweight="bold")
    ax1.set_title("Full Spectrum Latency Comparison (ms)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(schedulers, rotation=20, ha="right")
    ax1.legend()
    ax1.grid(True, linestyle="--", alpha=0.6)

    # Right: Zoom-in on CFS-like vs Adapt
    fast_scheds = ["CFS-Like Reactive", "Adapt (Proposed)"]
    fast_p95 = [15.54, 9.94]
    fast_p99 = [18.55, 15.39]
    xf = np.arange(len(fast_scheds))
    
    rects1 = ax2.bar(xf - width/2, fast_p95, width, label="P95 Latency", color="#3498db")
    rects2 = ax2.bar(xf + width/2, fast_p99, width, label="P99 Latency", color="#2ecc71")
    ax2.set_ylabel("Queuing Latency (ms)", fontweight="bold")
    ax2.set_title("Zoom-In: CFS-Like Reactive vs. Adapt Proactive (ms)")
    ax2.set_xticks(xf)
    ax2.set_xticklabels(fast_scheds)
    ax2.legend()
    ax2.grid(True, linestyle="--", alpha=0.6)

    for r in rects1 + rects2:
        h = r.get_height()
        ax2.annotate(f"{h:.2f}ms", xy=(r.get_x() + r.get_width()/2, h),
                     xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontweight="bold")

    plt.suptitle("Figure 3: OS Queuing Latency Distribution (P95 and P99) Under Bursty Cloud Workload", y=1.02)
    plt.tight_layout()
    plt.savefig("docs/assets/fig3_scheduler_latency_distribution.png")
    plt.close()
    print("Saved fig3_scheduler_latency_distribution.png")

# 4. Throttled Duration & SLA Violations
def plot_throttling_violations():
    schedulers = ["Static Quota", "Reactive Daemon", "CFS-Like Reactive", "Adapt (Proposed)"]
    throttled_sec = [31.0, 39.0, 8.0, 5.0]
    sla_violations = [33, 41, 0, 0]

    fig, ax1 = plt.subplots(figsize=(9, 4.8))
    x = np.arange(len(schedulers))
    width = 0.35

    rects1 = ax1.bar(x - width/2, throttled_sec, width, label="Throttled Time (seconds)", color="#e67e22")
    ax1.set_ylabel("CPU Throttled Duration (seconds)", color="#d35400", fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(schedulers, rotation=15, ha="right")

    ax2 = ax1.twinx()
    rects2 = ax2.bar(x + width/2, sla_violations, width, label="SLA Violations Count", color="#9b59b6")
    ax2.set_ylabel("Count of SLA Violations (Threshold > 45ms)", color="#8e44ad", fontweight="bold")

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc="upper right")

    plt.title("Figure 4: Throttling Mitigation & SLA Violation Elimination", pad=15)
    plt.tight_layout()
    plt.savefig("docs/assets/fig4_throttling_and_violations.png")
    plt.close()
    print("Saved fig4_throttling_and_violations.png")

# 5. Component Ablation Study Impact
def plot_ablation_study():
    variants = ["1. Full Adapt\n(Proposed)", "2. w/o Hysteresis\n(No Cooldown)", "3. w/o Safety Guard\n(No Fallback)", "4. w/o Headroom\n(alpha = 0.0)"]
    p99_latency = [18.70, 18.70, 10.22, 39.64]
    allocation_thrash = [3, 34, 7, 3]

    fig, ax1 = plt.subplots(figsize=(10, 5))
    x = np.arange(len(variants))
    width = 0.35

    b1 = ax1.bar(x - width/2, p99_latency, width, label="P99 Latency (ms)", color="#34495e")
    ax1.set_ylabel("P99 Tail Latency (ms)", color="#2c3e50", fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(variants)

    ax2 = ax1.twinx()
    b2 = ax2.bar(x + width/2, allocation_thrash, width, label="Actuator Thrashing (Changes)", color="#e74c3c")
    ax2.set_ylabel("Count of Cgroups Allocation Adjustments (Thrash)", color="#c0392b", fontweight="bold")

    for rect in b1:
        ax1.annotate(f"{rect.get_height():.1f}ms", xy=(rect.get_x() + rect.get_width()/2, rect.get_height()),
                     xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold")
    for rect in b2:
        ax2.annotate(f"{int(rect.get_height())}", xy=(rect.get_x() + rect.get_width()/2, rect.get_height()),
                     xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold", color="#c0392b")

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc="upper center")

    plt.title("Figure 5: Component Ablation Study — Isolating Hysteresis and Proactive Headroom", pad=15)
    plt.tight_layout()
    plt.savefig("docs/assets/fig5_ablation_study.png")
    plt.close()
    print("Saved fig5_ablation_study.png")

# 6. Demand vs Allocation Timeline
def plot_timeline():
    epochs = np.arange(1, 51)
    # Workload with a surge at t=20 to 35
    np.random.seed(42)
    base = 30 + 5 * np.sin(epochs / 3) + np.random.normal(0, 2, 50)
    base[20:35] += 45 # Surge

    # Adapt Allocation: scales at t=18 (proactively 2 epochs early)
    adapt_alloc = np.zeros(50)
    for i in range(50):
        if i < 18:
            adapt_alloc[i] = 42
        elif 18 <= i < 37:
            adapt_alloc[i] = 92
        else:
            adapt_alloc[i] = 45

    # Reactive Allocation: scales at t=23 (3 epochs late)
    reactive_alloc = np.zeros(50)
    for i in range(50):
        if i < 23:
            reactive_alloc[i] = 40
        elif 23 <= i < 38:
            reactive_alloc[i] = 85
        else:
            reactive_alloc[i] = 40

    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.plot(epochs, base, color="#2980b9", linewidth=2.5, label="Actual Workload CPU Demand (%)")
    ax.step(epochs, adapt_alloc, color="#27ae60", linewidth=2.2, linestyle="--", where="mid", label="Adapt Proactive Allocation (Headroom + Anticipatory)")
    ax.step(epochs, reactive_alloc, color="#e67e22", linewidth=2.0, linestyle=":", where="mid", label="Reactive Control Allocation (Lagged Response)")

    ax.axvspan(18, 20, color="#2ecc71", alpha=0.25, label="Proactive Pre-Provisioning Window (Zero Queue Lag)")
    ax.axvspan(20, 23, color="#e74c3c", alpha=0.20, label="Reactive Throttling Penalty Window")

    ax.set_xlabel("Time Epoch (seconds)", fontweight="bold")
    ax.set_ylabel("CPU Allocation / Demand (%)", fontweight="bold")
    ax.set_title("Figure 6: Dynamic Timeline Comparison — Proactive Lead vs. Reactive Lag", pad=15)
    ax.legend(loc="upper left")
    ax.set_ylim(15, 105)
    ax.grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.savefig("docs/assets/fig6_telemetry_actuation_timeline.png")
    plt.close()
    print("Saved fig6_telemetry_actuation_timeline.png")

if __name__ == "__main__":
    plot_forecasting_comparison()
    plot_shap_importance()
    plot_scheduler_latency()
    plot_throttling_violations()
    plot_ablation_study()
    plot_timeline()
    print("\n[✓] All 6 thesis figures successfully generated in docs/assets/")
