# System Architecture Document
## Adapt: Two-Tier Decoupled Scheduling Architecture

### 1. Tier Separation
```
+-------------------------------------------------------------+
|                      USER SPACE (Tier 1)                    |
|                                                             |
|   Telemetry Ingest -> Sliding Buffer -> ML Forecaster       |
|                               |                             |
|                               v                             |
|                    Confidence & Drift Check                 |
|                               |                             |
|                               v                             |
|                      Deterministic Safety Guard             |
|                               |                             |
|                               v                             |
|                    Policy Engine + Hysteresis               |
+-------------------------------|-----------------------------+
                                | sysfs cgroups v2 write
                                v
+-------------------------------------------------------------+
|                     KERNEL SPACE (Tier 2)                   |
|                                                             |
|   /sys/fs/cgroup/adapt.slice/cpu.max (Bandwidth Limit)      |
|   /sys/fs/cgroup/adapt.slice/cpu.weight (Proportional)      |
|   Linux CFS / EEVDF Hot-Path Scheduling                     |
+-------------------------------------------------------------+
```

### 2. Mathematical Latency Model
When workload CPU demand $D(t)$ exceeds allocated quota $A(t)$:
$$\text{Deficit}(t) = \max(0, D(t) - A(t))$$
$$\text{Queue}(t) = \max(0, \text{Queue}(t-1) \times \gamma + \text{Deficit}(t))$$
$$\text{Latency}(t) = L_{\text{base}} + \left(\frac{\text{Queue}(t)}{\max(A(t), 10.0)}\right) \times S_{\text{latency}}$$
Where $\gamma = 0.5$ is queue drain decay and $S_{\text{latency}} = 65.0\text{ ms}$.
When $A(t)$ is proactively provisioned prior to a demand surge, the deficit remains zero, preventing queue buildup and tail latency spikes.
