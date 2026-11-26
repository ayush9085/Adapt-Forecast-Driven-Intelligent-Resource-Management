# Methodology Document
## Adapt: Forecast-Driven Intelligent Resource Management for Operating Systems

### 1. Research Question
Can near-future resource demand forecasting drive proactive OS scheduling allocations that reduce latency spikes and CPU throttling compared with reactive scheduling, without destabilizing the system or introducing excessive telemetry/inference overhead?

### 2. Hypotheses
- **H1 (Proactive Allocation)**: Pre-provisioning CPU bandwidth $k$ epochs in advance of a predictable demand surge reduces $P95$ and $P99$ tail queuing latency and eliminates SLA violations compared to reactive control.
- **H2 (Decoupled Safety)**: Decoupling forecasting into Tier-1 user space with deterministic safety guards prevents OS thrashing and ensures graceful fallback to standard reactive resource control during concept drift or prediction degradation.
- **H3 (Minimal Overhead)**: Lightweight time-series models (Moving Average, Exponential Smoothing, compact GRU) introduce sub-millisecond inference latency, satisfying soft real-time user-space control loop deadlines ($<50\text{ ms}$).

### 3. Variables
- **Independent Variables**: Scheduling policy (CFS-Like Reactive Resource-Control, Static Quota, Reactive Daemon, Adapt Proactive ML), Forecasting model (Naive, MA, Holt-Winters, ARIMA, LSTM, GRU), Prediction Horizon $k \in [1, 6]$.
- **Dependent Variables**: Average latency, $P50/P90/P95/P99$ latency, SLA violation count & rate, total throttling duration, resource efficiency percentage, allocation change count, control response lag, and inference latency.
- **Controlled Variables**: Workload demand trace sequence (immutable seed), CPU capacity ($100\%$), SLA threshold ($45.0\text{ ms}$), sampling period ($1.0\text{ s}$).

---

### 4. Mathematical Models & Metrics

#### 4.1 Chronological Split (No Lookahead Leakage)
Workload telemetry sequences are partitioned strictly chronologically:
$$T_{\text{train}} = [0, \lfloor 0.70 \cdot N \rfloor), \quad T_{\text{val}} = [\lfloor 0.70 \cdot N \rfloor, \lfloor 0.85 \cdot N \rfloor), \quad T_{\text{test}} = [\lfloor 0.85 \cdot N \rfloor, N)$$
Feature scaling (StandardScaler) is fitted **strictly on $T_{\text{train}}$** and applied to validation/test sets without lookahead bias.

#### 4.2 Latency and Queue Physics (Simulation Engine)
For epoch $t$, with workload demand $D(t)$ and allocated capacity $A(t)$:
$$\text{Deficit}(t) = \max(0.0, D(t) - A(t))$$
$$\text{Queue}(t) = \max\left(0.0, \text{Queue}(t-1) \cdot \gamma + \text{Deficit}(t)\right)$$
$$\text{Latency}(t) = L_{\text{base}} + \left(\frac{\text{Queue}(t)}{\max(A(t), 10.0)}\right) \cdot S_{\text{latency}}$$
Where:
- $L_{\text{base}} = 8.0\text{ ms}$ (baseline execution/context switch latency)
- $\gamma = 0.5$ (drain decay rate)
- $S_{\text{latency}} = 65.0\text{ ms}$ (queuing delay penalty multiplier)

#### 4.3 Resource Efficiency
Reflects useful served workload relative to reserved allocation, capturing both under-provisioning starvation and over-provisioning waste:
$$\text{Efficiency} = \frac{1}{N} \sum_{t=1}^{N} \left( \frac{\min(D(t), A(t))}{\max(A(t), 1.0)} \right) \times 100\%$$

#### 4.4 Event-Associated Control Response Lag
The control response lag evaluates how rapidly or proactively a scheduler adapts to a specific, detected workload surge event.

**Formal Procedure:**
1. **Surge Onset Detection ($t_{\text{surge}}$)**: The first epoch where demand crosses the surge threshold ($\ge 65\%$) and increases over the preceding epoch ($D(t) > D(t-1)$).
2. **Target Headroom Capacity**: Target capacity required to sustain the surge without queuing is defined as:
   $$\text{Target} = D(t_{\text{surge}}) \times 0.90$$
3. **Bounded Search Window**: Evaluation is constrained strictly to the event window $[t_{\text{surge}} - W_{\text{before}}, t_{\text{surge}} + W_{\text{after}}]$, where $W_{\text{before}}=4$ and $W_{\text{after}}=15$ epochs.
4. **Proactive Anticipation ($\text{Response Lag} \le 0$)**: Permitted **only if** an explicit proactive scale-up decision (`PROACTIVE_SCALE_UP` or `PROACTIVE_CRITICAL_BOOST`) occurred within the bounded pre-surge interval $[t_{\text{surge}} - W_{\text{before}}, t_{\text{surge}}]$ that brought allocation to $\ge \text{Target}$. Unrelated high allocation long before the surge cannot produce negative lag.
5. **Reactive Response ($\text{Response Lag} > 0$)**: The first epoch $t \in [t_{\text{surge}}, t_{\text{surge}} + W_{\text{after}}]$ where allocation catches up to $\ge \text{Target}$.
   $$\text{Response Lag} = t_{\text{response}} - t_{\text{surge}}$$
6. **Unresolved / No Response**: If allocation fails to reach target capacity within $W_{\text{after}}$ epochs (e.g., rigid static quota), response lag is reported as **`N/A`** rather than an unbounded or misleading integer.

#### 4.5 Confidence Heuristic
$$\text{Confidence}(t) = \max\left(0.0, 1.0 - \frac{\overline{\text{MAE}}_{\text{recent}}}{E_{\text{tolerated}}}\right) \times \left(0.5 + 0.5 \cdot \text{DirAcc}_{\text{recent}}\right)$$
*Note: This is an empirical engineering heuristic based on residual variance, not a calibrated Bayesian probability.*

#### 4.6 Streaming Concept Drift
$$\text{Drift Triggered} \iff \frac{\text{RMSE}_{\text{recent}}}{\max(\text{RMSE}_{\text{reference}}, E_{\text{baseline\_min}})} > M_{\text{drift}}$$

---

### 5. Official Experiment Battery Definitions
- **TC-01 (Step Contention Test)**: Injects sudden workload step surge. Measures event-associated response lag, queue buildup, throttling duration, and P95/P99 latency.
- **TC-02 (Periodic Load Test)**: Sinusoidal diurnal workload. Measures forecast tracking accuracy and resource efficiency.
- **TC-03 (Concept Drift & Noise Test)**: Sudden variance and mean distribution shift. Measures drift detection speed, fallback trigger, and stability.
- **TC-04 (Overhead Profile)**: Host-level microbenchmark profiling of inference latency, policy decision latency, dry-run actuator call duration, process RSS memory, and CPU utilization.
- **Presentation Demo**: Independent multi-phase demonstration scenario showing stable baseline, upward ramp, major burst, decline, and noisy jitter.

---

### 6. Limitations & Threats to Validity
1. **Simulation vs. Real Linux CFS**: The simulation models user-space reactive resource-control behavior surrounding fair CPU scheduling; it does not emulate kernel context-switch runqueues down to the nanosecond vruntime granularity.
2. **Synthetic Telemetry**: Synthetic sinusoidal and step bursts represent idealized server traces; production deployments may exhibit heavy-tailed fractal burstiness.
3. **Platform Boundary**: macOS runs the high-fidelity discrete-time simulation; native cgroups v2 require a Linux environment with systemd/cgroupfs v2 mount.
4. **TC-04 Scope**: The isolated inference/policy/dry-run control functions execute well below the control interval in this host microbenchmark; end-to-end live Linux daemon overhead requires separate live-system measurement.
