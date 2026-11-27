# ADAPT OS — FINAL PBL DEFENSE PRESENTATION SCRIPT
## 15-Minute Defense Script for 4 Presenters (18 Slides)

**Team Members:**
1. **Ayush Pandey (590025156)** — *Lead Presenter: Introduction, Motivation, Core Problem & Literature Review* (Slides 1–5, ~3.5 mins)
2. **Aditi Singh (590025914)** — *System Architecture, Telemetry Pipeline & ML Forecasting Engine* (Slides 6–9, ~3.5 mins)
3. **Dhruv Jha (590023509)** — *Policy Engine, Safety Guard State Machine & Core OS Benchmarks* (Slides 10–13, ~3.5 mins)
4. **Hemang Gupta (590025443)** — *Dynamic Trace Timeline, Ablation, XAI, Feasibility & Conclusion* (Slides 14–18, ~4.0 mins)

**Faculty Mentor:** Prof. Shubranil Das  
**Institution:** School of Computer Science, UPES Dehradun  
**Total Target Time:** 14:00 – 14:30 minutes (Leaving 30–60 seconds buffer for transition to Q&A)

---

## SECTION 1: INTRODUCTION, MOTIVATION & RESEARCH GAP
### Speaker 1: Ayush Pandey (SAP ID: 590025156)
*Target Duration: 0:00 – 3:45 (Slides 1 to 5)*

---

### [Slide 1: Title Slide & Team Roster] (Time: 0:00 – 0:40)
> **[Ayush Pandey]:**  
> "A very good morning to our respected faculty mentor, Prof. Shubranil Das, and esteemed jury members.  
> 
> My name is **Ayush Pandey**, and alongside my teammates **Aditi Singh**, **Dhruv Jha**, and **Hemang Gupta**, we are proud to present our final Project-Based Learning defense on:  
> **'Adapt: Forecast-Driven Intelligent Resource Management for Operating Systems.'**  
> 
> In modern multi-tenant cloud servers and containerized microservices, resource allocation is governed by Linux kernel scheduling primitives. Today, we demonstrate how our decoupled two-tier machine learning architecture solves one of the oldest systemic challenges in operating systems: the **Reactive Latency Tax**."

---

### [Slide 2: Executive Summary & Project Highlights] (Time: 0:40 – 1:30)
> **[Ayush Pandey]:**  
> "To begin with a high-level overview of our contributions:  
> Traditional operating system resource controllers—such as the Linux Completely Fair Scheduler (CFS) paired with Cgroups v2 `cpu.max` quotas—operate reactively. By the time a sudden demand spike is observed through CPU saturation thresholds, the application has already suffered from queue buildup and severe request throttling.  
> 
> To solve this, we built **Adapt**, a proactive resource allocator that forecasts future tenant demand using multi-step machine learning and dynamically resizes Cgroups v2 quotas *before* demand arrives.  
> 
> Over the course of our empirical benchmarking across multi-tenant trace environments, Adapt achieved four breakthrough results:  
> 1. A **99.2% reduction in tail queuing latency**, dropping P95 latency from over 1,000 milliseconds down to just 8.4 milliseconds.  
> 2. Complete elimination of SLA breaches, maintaining **0.0% SLA violations** compared to over 41% in reactive controllers.  
> 3. An **87.2% reduction in CFS throttling duration**, slashing cumulative throttling from 39 seconds down to 5 seconds.  
> 4. And critically, a **sub-0.15 millisecond execution overhead**, proving that our user-space daemon consumes less than 0.015% of the 1-second scheduling epoch."

---

### [Slide 3: Problem Statement: The 'Reactive Latency Tax'] (Time: 1:30 – 2:20)
> **[Ayush Pandey]:**  
> "Let us look at why current operating systems struggle with bursty workloads, as shown in this timeline figure.  
> 
> Under Linux CFS bandwidth control, a container is given a fixed runtime quota per period—for example, 200 milliseconds every 100 milliseconds. When an unexpected traffic surge arrives at time $t = 45$, the container exhausts its quota in the first 15 milliseconds. The kernel's `cfs_bandwidth` timer immediately puts the entire cgroup to sleep for the remaining 85 milliseconds.  
> 
> Standard reactive auto-scalers and monitoring daemons only sample utilization periodically. They detect saturation at epoch 46, calculate a new quota, and actuate at epoch 47.  
> 
> This creates a 2-epoch **allocation deficit**. During this window, thousands of incoming client requests pile up in the OS runqueue. Even after CPU quota is finally expanded, the server spends seconds draining the queued backlog. This is the **'Reactive Latency Tax.'**  
> 
> Our key insight: **If you wait until utilization crosses 80% to react, you have already lost.** Resource scaling must be proactive."

---

### [Slide 4: Architectural Dilemma: Why In-Kernel ML is Infeasible] (Time: 2:20 – 3:00)
> **[Ayush Pandey]:**  
> "A natural question arises: *Why not embed a machine learning model directly inside the Linux kernel's `schedule()` function?*  
> 
> As systems researchers, we recognized three strict kernel design constraints that make in-kernel ML impossible:  
> 1. **FPU Prohibitions:** The Linux kernel scheduler executes in atomic context where Floating-Point Unit (FPU) registers are disabled to avoid massive context-switch save/restore overhead.  
> 2. **Sub-Microsecond Budget:** The kernel's `pick_next_task()` function must execute within 500 nanoseconds to 1 microsecond. Neural network tensor operations take anywhere from 80 microseconds to 15 milliseconds—exceeding the kernel's dispatch budget by up to four orders of magnitude!  
> 3. **Kernel Panic Risk:** Any memory leak, division by zero, or unhandled exception in kernel space results in a fatal kernel panic and host crash.  
> 
> Therefore, we designed a **Decoupled Two-Tier Architecture**: We leave the kernel's microsecond-level dispatching untouched, and host the ML intelligence in an asynchronous, non-blocking user-space daemon."

---

### [Slide 5: Literature Review & Research Gap Analysis] (Time: 3:00 – 3:45)
> **[Ayush Pandey]:**  
> "In our survey of prior literature shown in this comparison table:  
> * Google's **Autopilot** (EuroSys '20) operates on multi-hour historical windows, making it too slow for sub-minute bursts.  
> * Stanford's **Quasar** (ASPLOS '14) performs coarse-grained black-box core allocation at workload admission, but cannot dynamically tune fine-grained quotas during runtime.  
> * Systems like **FIRM** (OSDI '20) leverage Reinforcement Learning, but suffer from high exploration penalties and convergence instability that can destabilize production clusters.  
> * MIT's **Caladan** (OSDI '20) shifts dedicated cores at millisecond scales, but requires dedicated CPU core pinning, making it impractical for dense multi-tenant cgroups.  
> 
> **Our Research Gap:** Prior systems either operate at multi-minute intervals or rely on reactive threshold feedback. Adapt bridges this gap by coupling fine-grained 1-second supervised forecasting with deterministic OS safety guards.  
> 
> Now, I hand over to **Aditi Singh**, who will explain our two-tier system architecture and machine learning pipeline."

---

## SECTION 2: ARCHITECTURE, TELEMETRY & ML ENGINE
### Speaker 2: Aditi Singh (SAP ID: 590025914)
*Target Duration: 3:45 – 7:15 (Slides 6 to 9)*

---

### [Slide 6: Proposed System Architecture: Two-Tier Decoupled Design] (Time: 3:45 – 4:35)
> **[Aditi Singh]:**  
> "Thank you, Ayush.  
> 
> Moving to the structural design of **Adapt**, as illustrated in our architecture block diagram:  
> 
> Adapt separates the problem into two distinct execution tiers:  
> **Tier 1 — The User-Space Intelligence Daemon (`adapt-daemon`):**  
> Every 1-second epoch, the daemon samples non-blocking telemetry counters from `/proc` and `/sys/fs/cgroup`. The telemetry is fed into our inference engine, where a trained time-series model projects workload demand 3 steps into the future. This forecast passes through our Policy Engine and Deterministic Safety Guard, which outputs a safe, smoothed CPU quota.  
> 
> **Tier 2 — The Linux Kernel Enforcement:**  
> The daemon applies the quota through the standard Linux Cgroups v2 virtual file system by writing to `/sys/fs/cgroup/<group>/cpu.max`.  
> Inside the kernel, the native Completely Fair Scheduler handles thread runqueues, red-black tree dispatching, and timeslice allocation at full native speed.  
> 
> Crucially, **Adapt requires zero kernel modifications or custom patches.** It runs on standard, unmodified mainline Linux (kernels 5.x through 6.x) with complete backward compatibility."

---

### [Slide 7: Multidimensional Telemetry & Feature Engineering] (Time: 4:35 – 5:25)
> **[Aditi Singh]:**  
> "High-accuracy forecasting depends on rich physical telemetry. Rather than relying solely on historical CPU utilization, Adapt ingests **5 multidimensional telemetry channels**:  
> 1. Current CPU utilization percentage.  
> 2. Memory Resident Set Size (RSS in Megabytes).  
> 3. Disk I/O operations per second (IOPS).  
> 4. Active task and thread count from `/proc/loadavg`.  
> 5. Ingress network request inflow rate.  
> 
> We construct a strict **zero-leakage chronological sliding window** using $W = 12$ history steps (representing the past 12 seconds) to forecast $H = 3$ horizon steps ahead.  
> 
> As revealed by our correlation heatmap on the right, I/O rates and task counts exhibit a strong positive correlation ($r = +0.84$) with future CPU demand. In web and database workloads, disk reads and incoming network packets occur *before* the application begins heavy CPU computation. This physical property allows our model to detect workload surges before CPU counters even begin to spike!"

---

### [Slide 8: Five Standard Time-Series ML Models Evaluated] (Time: 5:25 – 6:15)
> **[Aditi Singh]:**  
> "To identify the optimal model for low-latency operating systems control, we implemented and evaluated **five standard ML/DL architectures** alongside a statistical baseline under strictly identical training and validation splits:  
> 1. **Support Vector Regression (SVR):** Using a non-linear Radial Basis Function (RBF) kernel with $C = 100.0$ and $\epsilon = 0.05$.  
> 2. **Random Forest Regressor:** An ensemble of 100 decorrelated decision trees with a maximum depth of 12.  
> 3. **XGBoost Regressor:** A gradient-boosted tree model with 80 estimators, learning rate $\eta = 0.08$, and tree depth 5.  
> 4. **Long Short-Term Memory (LSTM):** A 2-layer stacked recurrent neural network with 64 units and dropout regularization of 0.20.  
> 5. **Gated Recurrent Unit (GRU):** A 2-layer network with 48 units designed for faster temporal parameter convergence.  
> 6. And an **Exponentially Weighted Moving Average (EWMA)** statistical forecaster serving as a non-learning baseline."

---

### [Slide 9: Forecasting Model Evaluation: Accuracy vs. Inference Latency] (Time: 6:15 – 7:15)
> **[Aditi Singh]:**  
> "This brings us to our empirical model evaluation table and trade-off scatter plot.  
> 
> In an operating systems daemon, forecasting accuracy is useless if inference takes too long.  
> * Deep learning models like LSTM and GRU achieved excellent accuracy—LSTM recorded an MAE of 4.05% and a Directional Accuracy of 94.6%. However, LSTM required **14.82 milliseconds of inference latency**, which imposes an unacceptably heavy compute footprint on a host daemon.  
> * Conversely, **XGBoost achieved an MAE of 4.12% and 94.2% Directional Accuracy—virtually identical to LSTM—while executing in just 0.082 milliseconds (82 microseconds)!**  
> 
> XGBoost is **180 times faster than LSTM** because its decision tree splits can be traversed with branch-predicted cache-aligned CPU instructions.  
> 
> With a 94.2% directional accuracy, XGBoost almost never misses an upcoming burst. We selected XGBoost as Adapt’s production engine.  
> 
> I now invite **Dhruv Jha** to explain how these forecasts are transformed into safe kernel control policies."

---

## SECTION 3: POLICY ENGINE, SAFETY & CORE BENCHMARKS
### Speaker 3: Dhruv Jha (SAP ID: 590023509)
*Target Duration: 7:15 – 10:45 (Slides 10 to 13)*

---

### [Slide 10: Policy Engine & Mathematical Control Formalization] (Time: 7:15 – 8:05)
> **[Dhruv Jha]:**  
> "Thank you, Aditi.  
> 
> Having an accurate forecast is only half the battle. If a daemon directly sets CPU quota to raw predicted demand, sudden micro-bursts will cause clipping, and noise will cause quota thrashing. Our **Policy Engine** formalizes resource allocation through three mathematical mechanisms:  
> 
> **1. Proactive Headroom Scaling:**  
> $$\text{Alloc}_{\text{target}}(t+1) = \hat{D}(t+1) \cdot (1 + \alpha_{\text{headroom}})$$  
> We incorporate a 15% safety headroom ($\alpha = 0.15$). This buffer absorbs instantaneous micro-spikes between 1-second sampling boundaries.  
> 
> **2. Asymmetric Hysteresis Damping:**  
> When demand surges ($\Delta > 5\%$), we scale quota **immediately** to protect queuing latency. However, when demand recedes, we enforce a **damped decay** requiring 3 consecutive low-utilization epochs before releasing quota. This completely suppresses rapid quota flapping.  
> 
> **3. Bounded Clamping Invariant:**  
> Quotas are strictly clamped between a tenant minimum ($0.2$ cores) and host maximum ($4.0$ cores), guaranteeing tenant isolation."

---

### [Slide 11: Deterministic Safety Guard & CUSUM Concept Drift] (Time: 8:05 – 8:55)
> **[Dhruv Jha]:**  
> "In systems engineering, production software must be fault-tolerant. What happens if the workload pattern shifts dramatically, or a telemetry sensor fails?  
> 
> As detailed in our **Safety State Machine**, Adapt implements two autonomous safeguards:  
> 1. **Dynamic Confidence Scoring:**  
> We compute a real-time confidence score $C(t)$ based on the relative error of recent predictions. If $C(t) \ge 0.70$, the system operates in `NORMAL_PROACTIVE` mode. If confidence dips between $0.40$ and $0.70$, the system enters `DEGRADED_HEADROOM` mode, automatically doubling headroom to 30%.  
> 2. **CUSUM Residual Drift Detector:**  
> We track cumulative model drift using a Page-Hinkley CUSUM algorithm:  
> $$S_t = \max(0, S_{t-1} + e_t - k)$$  
> If cumulative residuals cross a threshold ($S_t > 50$), an anomaly is declared, and the system transitions to `FALLBACK_REACTIVE` mode, safely defaulting to proportional feedback control until the model recovers.  
> 
> Under no circumstance can a model failure compromise operating system stability."

---

### [Slide 12: OS Scheduling Benchmark: Queuing Latency Distribution] (Time: 8:55 – 9:50)
> **[Dhruv Jha]:**  
> "Now let us examine the experimental benchmarks. We evaluated Adapt against three industry-standard baselines under identical bursty trace workloads:  
> 1. A **Static Quota Allocation** (fixed at 2.0 cores).  
> 2. A **Reactive Threshold Daemon** (standard 80% watermark rule).  
> 3. And a **CFS-like Reactive Resource-Control Baseline** that models reactive quota feedback with observation lag.  
> 
> As displayed in our latency distribution graph:  
> * Static allocation suffered an intolerable P95 latency of **1,020 milliseconds** and P99 of **2,150 milliseconds** during 3.5-core bursts.  
> * The CFS-like Reactive baseline recorded a P95 of **520 milliseconds** and P99 of **1,240 milliseconds** due to reactive allocation lag.  
> * **Adapt compressed P50 latency to 2.1 milliseconds, P95 to 8.4 milliseconds, and P99 to 18.2 milliseconds!**  
> 
> This represents a **99.2% reduction in tail queuing latency** over static quotas and a **98.4% reduction** over reactive baselines."

---

### [Slide 13: SLA Violations & CPU Throttling Mitigation] (Time: 9:50 – 10:45)
> **[Dhruv Jha]:**  
> "Tail latency directly determines Service Level Agreements (SLAs). In our benchmark, we defined an SLA breach as any request taking longer than 50 milliseconds to complete.  
> 
> As shown on the left chart:  
> * The Reactive Threshold daemon breached SLAs for **41.2%** of the entire execution runtime.  
> * The CFS-like baseline violated SLAs for **33.4%** of the run.  
> * **Adapt achieved exactly 0.0% SLA violations across the entire benchmark.**  
> 
> Looking at the right chart, we see why: Adapt reduced total CFS throttling duration from **39.0 seconds down to 5.0 seconds**—an **87.2% reduction**.  
> 
> By pre-allocating quota into the cgroup bandwidth bucket 1 epoch before bursts arrive, runnable tasks find the quota ready and execute without ever hitting the kernel throttling wall.  
> 
> I now hand over to **Hemang Gupta**, who will walk us through the dynamic trace timeline, ablation study, model explainability, and concluding remarks."

---

## SECTION 4: TIMELINE, ABLATION, XAI & CONCLUSION
### Speaker 4: Hemang Gupta (SAP ID: 590025443)
*Target Duration: 10:45 – 14:30 (Slides 14 to 18)*

---

### [Slide 14: Dynamic Timeline: Proactive Lead vs. Reactive Deficit] (Time: 10:45 – 11:35)
> **[Hemang Gupta]:**  
> "Thank you, Dhruv.  
> 
> To understand the exact physical mechanics driving these gains, let us inspect this epoch-by-epoch execution timeline between epochs 40 and 60.  
> 
> At epoch $t = 44$, our XGBoost model anticipates that upcoming demand will spike from 1.5 cores to 3.2 cores at epoch 45.  
> * Within 140 microseconds, Adapt proactively raises the Cgroups v2 `cpu.max` allocation to 3.68 cores.  
> * When the workload burst lands at $t = 45$, sufficient CPU bandwidth is already available. The tasks execute without delay, and queuing latency remains below 5 milliseconds.  
> 
> In contrast, observe the CFS-like reactive baseline in orange:  
> At $t = 45$, it is trapped at 2.0 cores. It exhausts its quota within 15 milliseconds, throttles the application, and only increases allocation at $t = 47$. By then, an enormous queue has formed.  
> 
> This trace provides definitive empirical proof: **Adapt demonstrates a proactive response window that eliminates the reactive deficit.**"

---

### [Slide 15: Component Ablation Study: Isolating Core Mechanisms] (Time: 11:35 – 12:20)
> **[Hemang Gupta]:**  
> "To prove that our improvements stem from sound architectural engineering rather than incidental tuning, we conducted a rigorous **Component Ablation Study (TC-03)**:  
> 
> 1. **Full Adapt:** Achieves 8.4 ms P95 latency with only 18 quota transitions.  
> 2. **Ablating Hysteresis (Adapt w/o Hysteresis):** Without damping, quota transitions exploded from 18 to **204 transitions**—an **11.3x increase in quota thrashing**. This caused severe lock contention in the kernel's virtual file system.  
> 3. **Ablating Headroom (Adapt w/o Headroom, $\alpha = 0$):** P95 tail latency jumped from 8.4 ms to **17.8 ms**—a **2.1x spike**—because unpredicted micro-spikes clipped against exact demand.  
> 4. **Ablating ML (Static EWMA):** Reverted directly to reactive behavior, failing to predict burst onsets.  
> 
> This ablation proves that **both Headroom and Hysteresis are mathematically necessary** for kernel stability and tail latency containment."

---

### [Slide 16: Explainable AI (XAI) via TreeSHAP Interpretability] (Time: 12:20 – 13:05)
> **[Hemang Gupta]:**  
> "In operating systems, a controller cannot be a complete black box; system administrators require deterministic guarantees and explainability.  
> 
> We applied **TreeSHAP** to our trained XGBoost model to compute exact Shapley feature attributions for every scheduling decision:  
> * **I/O Request Rate** emerged as the single largest contributor, accounting for **48.5% of total model attribution**. This makes complete physical sense: in modern Linux storage and network stacks, kernel I/O interrupts and buffer cache operations immediately precede CPU-intensive user-space computation.  
> * **Active Task Count** contributed **28.2%**, serving as an explicit arrival indicator for process thread creation.  
> * **Historical CPU Usage** provided the **15.4%** baseline.  
> 
> TreeSHAP proves that our machine learning model is learning **genuine physical causality in Linux workload behavior**, rather than spurious statistical correlations."

---

### [Slide 17: Actuator Overhead & Real-World Feasibility (TC-04)] (Time: 13:05 – 13:50)
> **[Hemang Gupta]:**  
> "A critical concern in OS research is daemon overhead. Can a system run an ML model without robbing compute from tenant workloads?  
> 
> In Benchmark TC-04, we conducted microbenchmarks of every execution phase:  
> * Feature extraction and XGBoost inference took **82.4 microseconds**.  
> * Policy and safety guard execution took **18.1 microseconds**.  
> * Simulated dry-run actuator calls took **4.2 microseconds**.  
> * Real Linux Cgroups v2 sysfs VFS writes to `cpu.max` took **41.6 microseconds**.  
> 
> The **total daemon execution pipeline completes in just 146.3 microseconds (0.146 ms)**.  
> In a 1-second control epoch, the Adapt daemon runs for 0.015% of the time and sleeps for **99.985% of the epoch**. Furthermore, the daemon's Resident Set Size (RSS) remains strictly under 38 Megabytes.  
> 
> Our automated test suite of 20 unit tests passes in 5.3 seconds, verifying all invariants, clamping bounds, and safety fallback triggers."

---

### [Slide 18: Conclusion, Future Roadmap & Defense] (Time: 13:50 – 14:40)
> **[Hemang Gupta]:**  
> "To conclude our defense:  
> 1. We identified and quantified the **Reactive Latency Tax** in current Linux CFS bandwidth control.  
> 2. We designed and implemented a **Two-Tier Decoupled Architecture** that safely deploys user-space ML intelligence without touching the microsecond kernel dispatch path.  
> 3. We validated that **XGBoost achieves sub-0.1ms inference with 94.2% directional accuracy**, outperforming deep recurrent neural networks in systems efficiency.  
> 4. We empirically demonstrated a **99.2% reduction in tail queuing latency, 87.2% reduction in throttling, and zero SLA violations**.  
> 
> **Future Roadmap:**  
> With the release of Linux kernel 6.12, the new **`sched_ext` (eBPF)** framework allows pluggable user-space CPU schedulers. We plan to integrate Adapt's forecasting engine directly with `sched_ext` to dynamically tune scheduling slice duration alongside multi-resource memory (`memory.high`) and I/O weights.  
> 
> We express our heartfelt gratitude to our mentor, **Prof. Shubranil Das**, and the **School of Computer Science, UPES Dehradun**, for their invaluable guidance.  
> 
> Thank you. We are now open for questions from the examination committee."

---

## SUMMARY OF SPEAKER RESPONSIBILITIES & TIMELINE CHEAT SHEET

| Speaker | SAP ID | Slides | Target Time | Key Topics Owned |
| :--- | :--- | :---: | :---: | :--- |
| **Ayush Pandey** *(Lead)* | `590025156` | 1 – 5 | 0:00 – 3:45 | Introduction, Team/Mentor welcome, Problem Statement, CFS Throttling Tax, In-kernel ML dilemma, Literature Review matrix. |
| **Aditi Singh** | `590025914` | 6 – 9 | 3:45 – 7:15 | Two-tier architecture block diagram, 5-channel telemetry pipeline, 5 ML models (SVR/RF/XGB/LSTM/GRU), Accuracy vs. Latency trade-off. |
| **Dhruv Jha** | `590023509` | 10 – 13 | 7:15 – 10:45 | Policy engine math (headroom & asymmetric hysteresis), Safety Guard State Machine & CUSUM drift, Queuing latency benchmark, SLA & Throttling elimination. |
| **Hemang Gupta** | `590025443` | 14 – 18 | 10:45 – 14:30 | Trace timeline anticipation window, Component ablation study, TreeSHAP explainability, Actuation microbenchmark overhead (<0.15ms), Conclusion & Future `sched_ext` eBPF roadmap. |

---

## COMMON JURY QUESTIONS & RECOMMENDED ANSWERS

### Q1 (For Ayush): "Why can't you just use an aggressive threshold like 70% instead of machine learning?"
> **Answer:** "A simple lower threshold increases allocation whenever utilization crosses 70%, but it remains purely reactive. Under sharp burst traffic, demand jumps from 30% to 100% in a single timeslice—crossing 70% and 100% simultaneously. Furthermore, aggressive low thresholds cause permanent over-provisioning and idle energy waste during normal operation. Machine learning gives us *predictive lead time* without permanent over-allocation."

### Q2 (For Aditi): "Why did you choose XGBoost over LSTM when LSTM had a slightly lower MAE (4.05% vs 4.12%)?"
> **Answer:** "In an operating systems daemon, latency and compute footprint are first-order design constraints. LSTM required 14.82 ms of inference time and significant CPU cycles for matrix operations, whereas XGBoost executed in 0.082 ms—180 times faster—while matching LSTM's directional accuracy at 94.2%. XGBoost leaves 99.9% of the host CPU core available for user tenant workloads."

### Q3 (For Dhruv): "What happens if your ML model predicts complete nonsense or crashes?"
> **Answer:** "That is the role of our Deterministic Safety Guard. We compute a continuous confidence score $C(t)$ and track cumulative prediction drift using a CUSUM algorithm. If drift exceeds our safety threshold ($S_t > 50$) or confidence drops below 0.40, the system automatically falls back to deterministic reactive proportional control. The kernel never blindly executes unvalidated ML output."

### Q4 (For Hemang): "How does your user-space actuation affect the kernel's actual scheduling?"
> **Answer:** "Adapt does not alter the microsecond `schedule()` function inside the kernel. Native Linux CFS continues to pick tasks from the runqueue at sub-microsecond latency. Adapt merely modulates the cgroup's `cpu.max` bandwidth boundary at 1-second intervals via sysfs, which takes only 41.6 microseconds. This cleanly decouples high-level resource policy from low-level thread dispatching."
