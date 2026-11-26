# Presentation Demonstration Guide
## Adapt: Live PBL Evaluation Walkthrough

### 1. Starting the Platform
```bash
streamlit run app.py
```

### 2. Walkthrough Sequence for PBL Presentation

1. **System Overview (Page 1)**:
   - Introduce the central thesis: *Linux CPU schedulers are reactive. Adapt predicts near-future demand in user space and allocates resources proactively.*
   - Point to the KPI cards showing P95 latency improvement and zero SLA violations.

2. **Live Adapt Demo (Page 2)**:
   - Select the **"Presentation Demo"** scenario.
   - Run **"Adapt (Proactive ML)"**: Point out that at $t \approx 54\text{s}$, the forecaster identifies upward momentum and proactively raises CPU quota *before* the burst hits at $t=60\text{s}$.
   - Switch scheduler to **"Reactive Daemon"**: Observe the delay in scaling up, causing queue buildup and latency spikes crossing the $45\text{ms}$ SLA threshold.

3. **Scheduler Comparison (Page 4)**:
   - Click **"Run Comparative Suite Across 4 Schedulers"**.
   - Show the summary table proving fair evaluation: CFS-like, Static Quota, Reactive Daemon, and Adapt tested on identical inputs.

4. **Safety & Drift (Page 6)**:
   - Showcase the **Concept Drift Stress Test**: Explain how Adapt gracefully detects distribution shifts and immediately falls back to the safe reactive baseline without crashing.
