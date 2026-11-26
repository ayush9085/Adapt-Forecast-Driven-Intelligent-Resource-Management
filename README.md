# Adapt: Forecast-Driven Intelligent Resource Management for Operating Systems

**Subtitle**: *A Proactive Multi-Tenant OS Scheduling Framework Using Time-Series ML and Decoupled Actuation*

---

## 1. Problem Statement & Motivation
Operating system resource controllers (such as cgroup CPU bandwidth managers and autoscalers) are inherently **reactive**. Adjustments occur only *after*:
- Workload demand surges
- CPU run-queues accumulate excess runnable threads
- CFS throttling thresholds are triggered
- User-facing tail latency ($P95/P99$) spikes have already degraded service quality

**Adapt** investigates whether near-future workload forecasting can drive **proactive** resource allocations via standard Linux cgroups v2 (`cpu.max`, `cpu.weight`) *before* demand bursts arrive, without destabilizing the operating system.

---

## 2. Two-Tier Decoupled Architecture
A foundational operating systems principle: **Machine learning never executes inside the Linux kernel scheduling hot path.**
- **Tier 1 (User Space)**: High-resolution telemetry ingestion, rolling sliding window buffers, multivariate ML models (LSTM, GRU, ARIMA, Exponential Smoothing, Moving Average), confidence estimation heuristics, streaming concept drift detection, deterministic safety guards, and policy formulation.
- **Tier 2 (Linux Kernel)**: Unmodified kernel resource control via sysfs interfaces (`/sys/fs/cgroup/adapt.slice/cpu.max`, `cpu.weight`, `nice`).

---

## 3. Key Concepts & Terminology Clarification
- **CFS-Like Reactive Resource-Control Baseline**: Models reactive user-space resource-control surrounding fair CPU scheduling; it does not claim to reproduce every internal micro-state or vruntime tree traversal of the in-kernel Linux Completely Fair Scheduler.
- **Fair Scientific Comparison**: All 4 schedulers (CFS-Like Reactive, Static Quota, Reactive Daemon, and Adapt Proactive ML) are tested against **the exact same immutable workload trace** in every benchmark run.
- **No Manufactured Evidence**: All metrics, graphs, and performance deltas are computed dynamically. Under workloads where Adapt regresses against baselines, regressions are explicitly reported.

---

## 4. Quickstart & Installation

```bash
# 1. Clone/enter workspace
cd "OS PBL"

# 2. Install dependencies (Python 3.10+)
pip install -r requirements.txt

# 3. Run automated test suite
pytest

# 4. Launch the Streamlit Dashboard
streamlit run app.py
```

---

## 5. CLI Commands

```bash
# Generate synthetic workloads & scenario library
python3 scripts/generate_dataset.py

# Train & evaluate all 6 time-series models with dynamic ranking
python3 scripts/train_models.py --duration 180 --epochs 10

# Run complete official benchmark battery (TC-01, TC-02, TC-03, TC-04)
python3 scripts/run_benchmarks.py --scenario ALL

# Run single scenario benchmark
python3 scripts/run_benchmarks.py --scenario "Step Contention"

# Run live user-space daemon (dry-run safe by default)
python3 scripts/run_live_daemon.py --max_epochs 5
```

---

## 6. Project Directory Structure
```
adapt-os/
├── README.md
├── requirements.txt
├── pyproject.toml
├── config.yaml
├── app.py                      # 10-page Streamlit Dashboard
│
├── adapt/
│   ├── telemetry/              # Simulated & Linux /proc collectors
│   ├── forecasting/            # 6 models (Naive, MA, Holt-Winters, ARIMA, LSTM, GRU)
│   ├── policy/                 # Policy engine, Hysteresis, Safety guard, Drift detector
│   ├── actuator/               # Simulated, cgroups v2 (dry-run safe), Nice controller
│   ├── scheduler/              # CFS-like, Static Quota, Reactive Daemon, Adapt
│   ├── simulation/             # Discrete-time queue simulator & scenario library
│   ├── datasets/               # Chronological sliding window & synthetic generator
│   └── evaluation/             # Benchmark battery (TC-01 to TC-04), Metrics, Logger
│
├── docs/
│   ├── ARCHITECTURE.md         # Two-tier decoupled architecture diagram & latency physics
│   ├── METHODOLOGY.md          # Formal PBL methodology, hypotheses & formulas
│   ├── SRS.md                  # Software Requirements Specification
│   ├── DEMO.md                 # PBL viva evaluation walkthrough
│   └── RESULTS.md              # Empirical benchmark tables & analysis
│
├── scripts/                    # CLI execution entry points
├── tests/                      # 16 automated unit tests
└── models/metadata/            # Empirical model comparison & ranking metadata
```

---

## 7. Research Integrity Declarations
- **Source Labels**: All simulation outputs are explicitly marked **SIMULATED**. Host measurements are marked **HOST_SYSTEM_PROFILED**.
- **Confidence Heuristic**: Confidence scores represent empirical residual variance heuristics, not Bayesian posterior probabilities.
- **Safety Fallback**: If confidence drops below threshold or concept drift occurs, Adapt drops to safe baseline resource control.
