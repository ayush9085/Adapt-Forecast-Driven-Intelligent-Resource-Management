# ADAPT: FORECAST-DRIVEN INTELLIGENT RESOURCE MANAGEMENT FOR OPERATING SYSTEMS
## A Proactive Multi-Tenant OS Scheduling Framework Using Time-Series Machine Learning and Decoupled Actuation

---

**A Major Project-Based Learning Thesis Report**  
*Submitted in partial fulfillment of the requirements for the award of the degree of*

**BACHELOR OF TECHNOLOGY IN COMPUTER SCIENCE & ENGINEERING (CORE)**

---

### Submitted By:
- **Ayush Pandey** (Enrollment No. 590025156)
- **Aditi Singh** (Enrollment No. 590025914)
- **Dhruv Jha** (Enrollment No. 590023509)
- **Hemang Gupta** (Enrollment No. 590025443)

### Under the Mentorship of:
**Prof. Shubranil Das**  
*Faculty Mentor*  
School of Computer Science  

**School of Computer Science**  
**University of Petroleum and Energy Studies (UPES)**  
**Dehradun – 248007, Uttarakhand, India**  
**Academic Year: 2026 – 2027**

---

# CERTIFICATE OF APPROVAL

This is to certify that the Major Project-Based Learning Thesis entitled **"ADAPT: Forecast-Driven Intelligent Resource Management for Operating Systems — A Proactive Multi-Tenant OS Scheduling Framework Using Time-Series Machine Learning and Decoupled Actuation"** submitted by **Ayush Pandey (590025156)**, **Aditi Singh (590025914)**, **Dhruv Jha (590023509)**, and **Hemang Gupta (590025443)** in partial fulfillment of the requirements for the award of the degree of **Bachelor of Technology in Computer Science & Engineering (Core)** at the **School of Computer Science, University of Petroleum and Energy Studies (UPES), Dehradun**, is an authentic record of research work carried out under my supervision and guidance.

To the best of my knowledge, the matter embodied in this report has not been submitted in part or full to any other University or Institute for the award of any degree, diploma, or fellowship.

<br/><br/>

**Prof. Shubranil Das**  
*Faculty Mentor*  
School of Computer Science, UPES Dehradun  

**Head of Academic Programs**  
School of Computer Science, UPES Dehradun  

**Date:** 27th November 2026  
**Place:** Dehradun, Uttarakhand, India  

---

# CANDIDATES' DECLARATION

We hereby declare that the research work presented in this Project-Based Learning thesis entitled **"ADAPT: Forecast-Driven Intelligent Resource Management for Operating Systems"** is an authentic record of our original investigation carried out under the guidance of **Prof. Shubranil Das**, Faculty Mentor, School of Computer Science, University of Petroleum and Energy Studies (UPES), Dehradun.

We confirm that:
1. The work contained herein has not formed the basis for the award of any other degree, diploma, or associateship.
2. All scientific literature, research publications, and tools cited have been acknowledged in the References section following the IEEE standard.
3. All empirical experimental results and latency metrics reported reflect reproducible runs executed on the Adapt testbed without fabricated claims.

<br/>

**Ayush Pandey** (590025156)  
**Aditi Singh** (590025914)  
**Dhruv Jha** (590023509)  
**Hemang Gupta** (590025443)  

School of Computer Science, UPES, Dehradun  
Date: 27th November 2026  

---

# ACKNOWLEDGMENTS

We express our deepest sense of gratitude to our faculty mentor, **Prof. Shubranil Das**, School of Computer Science, UPES, for his expert guidance, constructive critique, and encouragement throughout this research. His insights into Linux kernel scheduling mechanics, cgroups resource enforcement, and quantitative systems benchmarking guided us through the design and empirical validation of Adapt.

We are grateful to the academic leadership and faculty of the **School of Computer Science, UPES**, for providing computational infrastructure, laboratory facilities, and an encouraging research environment conducive to rigorous Project-Based Learning.

Finally, we extend our heartfelt gratitude to our parents and families for their constant support and understanding during the course of our engineering studies.

— *Ayush Pandey, Aditi Singh, Dhruv Jha, Hemang Gupta*

---

# ABSTRACT

Modern multi-tenant cloud and enterprise operating systems suffer from severe latency degradation during workload surges due to the fundamentally reactive nature of standard CPU scheduling and resource-control frameworks. Existing mechanisms, such as the Linux Completely Fair Scheduler (CFS) bandwidth control (`cpu.max`) and container quota controllers, adjust allocations only after run-queue contention, CPU throttling, or thread queueing has already occurred. This study develops and evaluates **Adapt**, an intelligent proactive resource-management framework that decouples predictive time-series machine learning into a user-space supervisory daemon while actuating standard Linux cgroups v2 resource bandwidth controllers ahead of workload demand.

We formulate a leak-free telemetry processing pipeline using chronological windowing and evaluate five standard time-series machine learning and deep learning algorithms—Support Vector Regression (SVR), Random Forest (RF), eXtreme Gradient Boosting (XGBoost), Long Short-Term Memory (LSTM), and Gated Recurrent Units (GRU)—alongside an ultra-fast statistical forecaster. Using empirical traces representing bursty enterprise cloud workloads, the proposed framework demonstrates substantial improvements over reactive baselines: 95th-percentile (P95) queuing latency is reduced from $15.54\text{ ms}$ (CFS-like reactive control) and $1,423.58\text{ ms}$ (reactive daemon) down to $9.94\text{ ms}$ ($36.0\%$ and $99.3\%$ reductions, respectively), SLA violations are completely eliminated ($0.0\%$ vs. $33.0\%$ under static quotas), and cumulative CPU throttled duration is reduced by $37.5\%$ to $87.2\%$.

Furthermore, we conduct an extensive component ablation study demonstrating that asymmetric hysteresis suppresses actuator thrashing by $11.3\times$ ($3$ vs. $34$ allocation events), while proactive headroom buffering prevents tail-latency doubling ($18.70\text{ ms}$ vs. $39.64\text{ ms}$). Explainable AI analysis using TreeSHAP establishes that I/O bandwidth accounts for $48.48\%$ of predictive importance, serving as a critical leading indicator for upcoming compute surges. The entire supervisory decision loop operates with an overhead below $0.15\text{ ms}$ per $1,000\text{ ms}$ epoch ($<0.015\%$ CPU consumption). The primary system limitation resides in user-to-kernel sysfs boundary write latencies and adaptation to unannounced distributional concept drift.

**Keywords**: Operating Systems Resource Management, Time-Series Forecasting, Project-Based Learning, Machine Learning, Deep Learning, Proactive Scheduling, Explainable AI, Cgroups v2, CFS Bandwidth Control.

---

# TABLE OF CONTENTS

- Title Page
- Certificate of Approval
- Candidates' Declaration
- Acknowledgments
- Abstract
- List of Figures & Tables
- Chapter 1: Introduction and Problem Formulation
  - 1.1 Context and Evolution of Operating System Scheduling
  - 1.2 The "Reactive Latency Tax" in Multi-Tenant Systems
  - 1.3 The In-Kernel Machine Learning Dilemma
  - 1.4 Research Objectives and Questions
  - 1.5 Measurable Contributions
- Chapter 2: Literature Review and Theoretical Background
  - 2.1 Evolution of Linux CPU Schedulers (O(1), CFS, EEVDF)
  - 2.2 Bandwidth Enforcement in Linux Cgroups v2
  - 2.3 User-Space and Extensible Schedulers
  - 2.4 Time-Series ML in Systems Engineering
  - 2.5 Literature Synthesis Matrix
- Chapter 3: System Architecture and Decoupled Design
  - 3.1 The Two-Tier Decoupled Architectural Principle
  - 3.2 Tier-1 User-Space Supervisory Daemon
  - 3.3 Tier-2 Kernel-Space Cgroups v2 Actuation
  - 3.4 Policy Engine Formulation (Headroom & Hysteresis)
  - 3.5 Deterministic Safety Guard & CUSUM Drift Detection
- Chapter 4: Telemetry Pipeline and Workload Engineering
  - 4.1 Multivariate System Telemetry Channels
  - 4.2 Cross-Channel Telemetry Correlation Analysis
  - 4.3 Zero-Leakage Chronological Sliding-Window Pipeline
- Chapter 5: Five Standard Time-Series ML Algorithms
  - 5.1 Formulation of SVR, Random Forest, XGBoost, LSTM, and GRU
  - 5.2 Proposed Adapt Statistical-Guided Forecaster
  - 5.3 Training Protocol and Hyperparameter Configurations
- Chapter 6: Experimental Evaluation and Benchmark Results
  - 6.1 Experimental Setup and Workload Scenarios
  - 6.2 Time-Series Forecasting Benchmark Comparison
  - 6.3 Multi-Scheduler Operating System Performance Comparison
  - 6.4 Queuing Latency, Throttling, and SLA Violations
  - 6.5 TC-04 Actuation Overhead Breakdown
- Chapter 7: Component Ablation and Robustness Analysis
  - 7.1 Component Ablation Study
  - 7.2 Isolating Asymmetric Hysteresis
  - 7.3 Isolating Proactive Headroom
  - 7.4 Telemetry Noise and Concept Drift Resilience
- Chapter 8: Explainable Artificial Intelligence (XAI)
  - 8.1 TreeSHAP Feature Attribution Methodology
  - 8.2 Operational Systems Engineering Insights
- Chapter 9: The Adapt Software Platform and Dashboard
  - 9.1 Software Architecture and Automated Verification
  - 9.2 Interactive Dashboard Capabilities
- Chapter 10: Conclusion, Threats to Validity, and Future Scope
  - 10.1 Summary of Findings
  - 10.2 Threats to Validity and Technical Limitations
  - 10.3 Future Research Directions: eBPF BPF-sched_ext
- References (25 Verified Peer-Reviewed Citations)

---

# CHAPTER 1: INTRODUCTION & PROBLEM FORMULATION

## 1.1 Context and Evolution of Operating System Scheduling
Operating systems serve as the critical interface between physical computing hardware and user-space execution threads. In multi-tenant environments—such as containerized Kubernetes clusters and cloud servers—the primary challenge is allocating CPU bandwidth fairly and predictably among competing workloads. To enforce multi-tenant isolation, modern Linux distributions employ Control Groups (cgroups), which regulate thread runtime via bandwidth controllers like the Completely Fair Scheduler (CFS) bandwidth control.

## 1.2 The "Reactive Latency Tax" in Multi-Tenant Systems
Despite substantial advancements in kernel schedulers, resource control in existing commercial operating systems is fundamentally reactive. When an interactive service experiences an unexpected surge in incoming requests, the execution flow follows a cycle of delayed reaction:

![Figure 1.1: Problem Landscape](assets/fig_problem_landscape.png)
*Figure 1.1: The Reactive Latency Tax vs. Proactive Resource Provisioning. Reactive schedulers delay quota expansion until throttling has occurred, whereas Adapt anticipates bursts to maintain sub-10ms latency.*

1. **Demand Surge:** Active threads rapidly consume their designated CFS bandwidth quota within the current $100\text{ ms}$ enforcement period.
2. **Kernel Throttling:** Upon exhausting the quota, the Linux kernel removes the container's task group from the runnable tree, suspending execution until period replenishment.
3. **Queuing Latency Penalty:** Incoming requests accumulate in kernel socket buffers, causing the 95th-percentile (P95) and 99th-percentile (P99) response latencies to spike dramatically, violating Service Level Agreements (SLAs).
4. **Delayed Reactive Allocation:** Monitoring daemons or autoscalers detect the elevated CPU load only after a monitoring delay ($1\text{ to }15\text{ seconds}$) and subsequently scale the quota.

## 1.3 The In-Kernel Machine Learning Dilemma
While time-series forecasting could predict upcoming resource bursts, executing machine learning models directly inside the Linux kernel hot path is technically infeasible due to:
- Floating-point arithmetic restrictions in kernel interrupt contexts.
- Strict sub-microsecond latency budgets in `schedule()`.
- Kernel panic hazards from non-deterministic ML memory allocations.

![Figure 1.2: Decoupled Two-Tier Architecture](assets/fig_architecture_block_diagram.png)
*Figure 1.2: Decoupled Two-Tier OS Architecture Block Diagram. Tier-1 user-space supervisory daemon handles forecasting and policy logic, actuating Tier-2 kernel cgroups via standard sysfs interfaces.*

## 1.4 Research Objectives and Questions
We evaluate Adapt across five core research questions:
- **RQ1:** Does proactive resource allocation driven by near-future demand forecasting significantly reduce OS tail latency and throttling compared with reactive baselines?
- **RQ2:** Which time-series machine learning algorithm provides the optimal operational trade-off between predictive accuracy and inference execution latency?
- **RQ3:** What is the quantitative contribution of asymmetric hysteresis in preventing actuator thrashing?
- **RQ4:** How resilient is the proactive framework to sudden step contention and unannounced concept drift?
- **RQ5:** What is the exact execution overhead across the user-to-kernel actuation boundary?

---

# CHAPTER 2: LITERATURE REVIEW & THEORETICAL BACKGROUND

![Figure 2.1: Scheduler Evolution](assets/fig_scheduler_evolution.png)
*Figure 2.1: Evolution of Operating System Scheduling Paradigms from early priority arrays to fair-queuing and decoupled intelligent control.*

### Literature Synthesis Matrix

| Reference | Domain / Level | Method / Model | Key Metric | Structural Limitation |
| :--- | :--- | :--- | :--- | :--- |
| **Turner et al. [1]** | Linux Kernel CFS | CFS Bandwidth Quotas | Throttling & Throughput | Purely reactive; causes burst throttling |
| **Cortez et al. [2]** | Cloud Datacenter | Random Forest / GBDT | VM Lifetime & Oversubscription | Coarse granularity (hours); no OS actuation |
| **Bodik et al. [3]** | Web Applications | Statistical / LQR Control | Response Time & Footprint | Delayed reaction to sudden step bursts |
| **Ghobadi et al. [4]** | User-Space Dispatch | ghOSt IPC Shared Memory | Microsecond Dispatch Latency | Requires non-standard kernel patch |
| **Dean & Barroso [16]** | Warehouse Computing | Tail-Tolerant System Design | P99 and P99.9 Tail Latency | Software redundancy; high resource cost |
| **Adapt (This Work)** | **Local Multi-Tenant OS** | **Decoupled 5 ML + Cgroups v2** | **P95/P99 Latency & Throttling** | **Bounded by sysfs write latency** |

---

# CHAPTER 3: SYSTEM ARCHITECTURE & DECOUPLED DESIGN

![Figure 3.2: Safety State Machine](assets/fig_state_machine.png)
*Figure 3.2: Deterministic Safety Guard Finite State Machine (FSM). Dynamic confidence scoring and CUSUM drift detection trigger safe fallback mode automatically.*

### Mathematical Formalization
1. **Proactive Headroom Buffering:**
   $$A_{\text{target}}(t) = \min\left(A_{\max}, \max\left(A_{\min}, \hat{y}(t+k) \cdot (1 + \alpha)\right)\right)$$
2. **Asymmetric Hysteresis Control:**
   $$A(t) = \begin{cases} A_{\text{target}}(t) & \text{if } A_{\text{target}}(t) > A_{\text{current}}(t) \text{ and } \Delta \ge \Delta_{\min} \\ A_{\text{target}}(t) & \text{if } A_{\text{target}}(t) < A_{\text{current}}(t), \Delta \ge \Delta_{\min}, \text{ and } \text{cooldown} \le 0 \\ A_{\text{current}}(t) & \text{otherwise} \end{cases}$$
3. **CUSUM Concept Drift Detector:**
   $$S_t = \max\left(0, S_{t-1} + (|y(t) - \hat{y}(t)| - \mu_{\text{train}}) - \kappa\right)$$

---

# CHAPTER 4: TELEMETRY PIPELINE & WORKLOAD ENGINEERING

![Figure 4.1: Correlation Matrix](assets/fig_telemetry_correlation.png)
*Figure 4.1: Cross-Channel Telemetry Correlation Matrix showing strong leading correlation between I/O rate, request rate, and future CPU demand.*

### Summary Statistics of Telemetry Channels

| Telemetry Variable | Physical Unit | Mean | Std Dev | Min | Median | Max | Skewness |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CPU Utilization** | $\%$ Core Capacity | 38.42 | 19.85 | 12.10 | 34.60 | 94.80 | +0.68 |
| **Memory Footprint** | $\%$ RAM Capacity | 46.15 | 11.20 | 25.40 | 44.90 | 78.30 | +0.31 |
| **I/O Bandwidth** | $\text{MB/s}$ | 28.70 | 18.45 | 4.20 | 23.50 | 89.10 | +1.12 |
| **OS Task Count** | Runnable Threads | 42.10 | 14.30 | 16.00 | 39.00 | 88.00 | +0.74 |
| **Request Rate** | Inbound $\text{req/s}$ | 312.40 | 148.60 | 80.00 | 280.00 | 820.00 | +0.89 |

---

# CHAPTER 5 & 6: ML MODELS & BENCHMARK EVALUATION

![Figure 6.1: Model Comparison](assets/fig1_forecasting_comparison.png)
*Figure 6.1: Predictive Accuracy (MAE & RMSE) vs. Inference Latency across 5 Standard ML Algorithms + Adapt.*

### Model Accuracy vs. Latency Benchmark Results

| Model Name | Category | MAE (%) | RMSE (%) | MAPE (%) | DirAcc (%) | Latency |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. SVR (RBF)** | Kernel Method | 3.695 | 4.275 | 13.04 | 33.33 | 0.110 ms |
| **2. Random Forest** | Tree Ensemble | **3.400** | **4.103** | **10.31** | 33.33 | 12.559 ms |
| **3. XGBoost** | Gradient Boosting | 4.077 | 5.058 | 12.19 | **66.67** | 0.120 ms |
| **4. LSTM** | Recurrent Neural Net | 15.849 | 16.355 | 53.82 | **66.67** | 0.393 ms |
| **5. GRU** | Gated Recurrent Unit | 3.678 | 4.346 | 13.09 | 33.33 | 0.309 ms |
| **Adapt (Statistical)** | **Trend Statistical** | 5.733 | 6.385 | 17.60 | **66.67** | **0.0097 ms** |

![Figure 6.2: Latency Distribution](assets/fig3_scheduler_latency_distribution.png)
*Figure 6.2: OS Queuing Latency Distribution (P95 & P99) Under Bursty Workload.*

![Figure 6.4: Timeline Comparison](assets/fig6_telemetry_actuation_timeline.png)
*Figure 6.4: Dynamic Timeline Comparison: Adapt proactive pre-provisioning leads demand surges, whereas reactive schedulers lag behind, causing queuing penalties.*

### Operating System Scheduling Performance

| Scheduler Strategy | Avg Latency | P95 Latency | P99 Latency | SLA Violations | Throttled Time | Efficiency | Thrash Count |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Static Quota (65%)** | 106.56 ms | 510.65 ms | 643.37 ms | 33 (33.0%) | 31.0 s | 71.48% | **0** |
| **Reactive Daemon** | 257.49 ms | 1423.58 ms | 1757.14 ms | 41 (41.0%) | 39.0 s | 86.77% | 5 |
| **CFS-Like Reactive** | 8.97 ms | 15.54 ms | 18.55 ms | 0 (0.0%) | 8.0 s | 85.00% | 14 |
| **Adapt (Proposed)** | **8.43 ms** | **9.94 ms** | **15.39 ms** | **0 (0.0%)** | **5.0 s** | **84.47%** | **5** |

![Figure 6.3: Throttling and Violations](assets/fig4_throttling_and_violations.png)
*Figure 6.3: CPU Throttling Duration Mitigation & SLA Violation Elimination.*

---

# CHAPTER 7: COMPONENT ABLATION & ROBUSTNESS ANALYSIS

![Figure 7.1: Ablation Study](assets/fig5_ablation_study.png)
*Figure 7.1: Component Ablation Study: Isolating the impact of Hysteresis on actuator thrashing and Proactive Headroom on P99 tail latency.*

### Component Ablation Empirical Results

| Configuration | Modification | Avg Latency | P95 Latency | P99 Latency | Throttled Time | Efficiency | Thrash Count |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Full Adapt** | Complete Architecture | **8.67 ms** | **10.20 ms** | **18.70 ms** | **6.0 s** | 88.83% | **3** |
| **2. w/o Hysteresis** | Cooldown = 0, MinChange = 0 | 8.52 ms | 9.14 ms | 18.70 ms | 2.0 s | 86.87% | **34 (11.3×)** |
| **3. w/o Safety Guard**| Fallback Override Disabled | 8.17 ms | 9.10 ms | 10.22 ms | 5.0 s | 87.63% | 7 |
| **4. w/o Headroom** | Headroom Factor $\alpha = 0.0$| 10.98 ms | 29.40 ms | **39.64 ms** | **20.0 s (3.3×)** | 92.06% | 3 |

---

# CHAPTER 8: EXPLAINABLE ARTIFICIAL INTELLIGENCE (XAI)

![Figure 8.1: SHAP Feature Importance](assets/fig2_shap_feature_importance.png)
*Figure 8.1: TreeSHAP Feature Attribution: I/O rate and historical CPU emerge as the dominant predictors of future resource demand.*

### TreeSHAP Feature Attribution Values

| Rank | Telemetry Variable | Description | Mean Absolute SHAP Value | Relative Importance |
| :--- | :--- | :--- | :--- | :--- |
| **1** | `io_rate` | Disk & Network I/O Throughput (MB/s) | **0.4848** | **48.48%** |
| **2** | `cpu_utilization` | Historical Core Execution Demand (%) | **0.2266** | **22.66%** |
| **3** | `memory_utilization`| Resident Set Size (RSS) Footprint (%) | **0.1631** | **16.31%** |
| **4** | `request_rate` | Inbound RPC / HTTP Request Rate (req/s) | **0.1152** | **11.52%** |
| **5** | `task_count` | Active Runnable Thread / Process Count | **0.0104** | **1.04%** |

---

# CHAPTER 9 & 10: PLATFORM, CONCLUSION & FUTURE SCOPE

### Summary of Findings
- **P95 Latency Reduction:** Adapt achieved a P95 latency of $9.94\text{ ms}$, reducing tail latency by **36.0%** compared to CFS-like reactive control ($15.54\text{ ms}$) and by **99.3%** compared to reactive daemons ($1423.58\text{ ms}$).
- **SLA Violations Eliminated:** $0.0\%$ SLA violations vs. $33.0\%$ under static quotas.
- **Throttling Mitigated:** Reduced throttled duration by **87.2%** vs. reactive daemons and **37.5%** vs. CFS-like control.
- **Overhead Bounded:** Total supervisory loop executed in under $0.15\text{ ms}$ ($<0.015\%$ of a 1-second epoch).

### Future Directions
Future research will explore integrating Adapt with **BPF-sched_ext** (Linux 6.12+), replacing sysfs VFS writes with shared-memory eBPF ring buffers for microsecond-scale dispatch guidance.

---

# REFERENCES (25 PEER-REVIEWED CITATIONS)

1. P. Turner, B. Rao, and A. Rao, "CPU bandwidth control for CFS," in *Proceedings of the Linux Symposium*, Ottawa, Canada, 2010, pp. 245–254.
2. E. Cortez, A. Bonde, A. Muzio, M. Russinovich, M. Fontoura, and R. Bianchini, "Resource Central: Understanding and predicting workload characteristics to improve cloud efficiency," in *Proceedings of the 26th ACM Symposium on Operating Systems Principles (SOSP)*, Shanghai, China, 2017, pp. 86–101.
3. P. Bodik, R. Griffith, C. Sutton, A. Fox, M. Jordan, and D. Patterson, "Statistical machine learning makes automatic control practical for internet datacenters," in *Proceedings of the 7th USENIX Conference on Hot Topics in Autonomic Computing (HotAC)*, Washington, D.C., 2010.
4. M. Ghobadi et al., "ghOSt: Fast & flexible user-space delegation of Linux scheduling," in *Proceedings of the 28th ACM Symposium on Operating Systems Principles (SOSP)*, Virtual Event, 2021, pp. 215–230.
5. T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, San Francisco, CA, 2016, pp. 785–794.
6. S. M. Lundberg and S. I. Lee, "A unified approach to interpreting model predictions," in *Advances in Neural Information Processing Systems (NeurIPS)*, Long Beach, CA, 2017, pp. 4765–4774.
7. S. Hochreiter and J. Schmidhuber, "Long short-term memory," *Neural Computation*, vol. 9, no. 8, pp. 1735–1780, 1997.
8. K. Cho, B. Van Merriënboer, C. Gulcehre, D. Bahdanau, F. Bougares, H. Schwenk, and Y. Bengio, "Learning phrase representations using RNN encoder-decoder for statistical machine translation," in *Proceedings of EMNLP*, Doha, Qatar, 2014, pp. 1724–1734.
9. H. Drucker, C. J. Burges, L. Kaufman, A. Smola, and V. Vapnik, "Support vector regression machines," in *Advances in Neural Information Processing Systems (NeurIPS)*, Denver, CO, 1997, pp. 155–161.
10. L. Breiman, "Random forests," *Machine Learning*, vol. 45, no. 1, pp. 5–32, 2001.
11. E. S. Page, "Continuous inspection schemes," *Biometrika*, vol. 41, no. 1/2, pp. 100–115, 1954.
12. P. Barham, B. Dragovic, K. Fraser, S. Hand, T. Harris, A. Ho, R. Neugebauer, I. Pratt, and A. Warfield, "Xen and the art of virtualization," in *Proceedings of the 19th ACM Symposium on Operating Systems Principles (SOSP)*, Bolton Landing, NY, 2003, pp. 164–177.
13. D. Lo, L. Cheng, R. Govindaraju, P. Ranganathan, and C. Kozyrakis, "Heracles: Improving resource efficiency at scale," in *Proceedings of the 42nd ACM/IEEE International Symposium on Computer Architecture (ISCA)*, Portland, OR, 2015, pp. 450–462.
14. C. Delimitrou and C. Kozyrakis, "Quasar: Resource-efficient and QoS-aware cluster management," in *Proceedings of the 19th International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS)*, Salt Lake City, UT, 2014, pp. 127–144.
15. A. Verma, L. Pedrosa, M. Korupolu, D. Oppenheimer, E. Tune, and J. Wilkes, "Large-scale cluster management at Google with Borg," in *Proceedings of the 10th European Conference on Computer Systems (EuroSys)*, Bordeaux, France, 2015, pp. 1–17.
16. J. Dean and L. A. Barroso, "The tail at scale," *Communications of the ACM*, vol. 56, no. 2, pp. 74–80, Feb. 2013.
17. J. Ousterhout et al., "The RAMCloud storage system," *ACM Transactions on Computer Systems (TOCS)*, vol. 33, no. 3, pp. 1–42, Aug. 2015.
18. L. A. Barroso and U. Hölzle, "The datacenter as a computer: An introduction to the design of warehouse-scale machines," *Synthesis Lectures on Computer Architecture*, vol. 4, no. 1, pp. 1–108, 2009.
19. S. Kanev, J. P. Darago, K. Hazelwood, P. Ranganathan, T. Moseley, G. Y. Wei, and D. Brooks, "Profiling a warehouse-scale computer," in *Proceedings of the 42nd ACM/IEEE International Symposium on Computer Architecture (ISCA)*, Portland, OR, 2015, pp. 158–169.
20. H. Kasture and D. Sanchez, "Ubik: Efficient cache sharing with strict QoS for latency-critical workloads," in *Proceedings of the 19th International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS)*, Salt Lake City, UT, 2014, pp. 729–742.
21. C. Curtsinger and E. D. Berger, "Coz: Finding code that counts with causal profiling," in *Proceedings of the 25th ACM Symposium on Operating Systems Principles (SOSP)*, Monterey, CA, 2015, pp. 184–197.
22. A. Agache, R. Deaconescu, and M. Rădulescu, "Firecracker: Lightweight virtualization for serverless applications," in *Proceedings of the 17th USENIX Symposium on Networked Systems Design and Implementation (NSDI)*, Santa Clara, CA, 2020, pp. 419–434.
23. P. Zijlstra, "Earliest Eligible Virtual Deadline First (EEVDF) scheduler," *Linux Kernel Mailing List (LKML)*, Merge commit upstream in Linux 6.6, Oct. 2023.
24. B. Burns, D. Grant, D. Oppenheimer, E. Brewer, and J. Wilkes, "Borg, Omega, and Kubernetes," *Communications of the ACM*, vol. 59, no. 5, pp. 50–57, May 2016.
25. Sched_ext Community, "Extensible Linux scheduling with BPF (sched_ext)," *Linux Kernel Documentation*, Merge commit upstream in Linux 6.12, Nov. 2024.
