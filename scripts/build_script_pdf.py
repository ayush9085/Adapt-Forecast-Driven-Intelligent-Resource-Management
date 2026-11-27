#!/usr/bin/env python3
"""
Convert the 4-person PBL Defense Presentation Script into an executive, beautifully styled PDF.
Features:
- UPES NAAC A+ official branding and Great Place to Work logo
- Color-coded speaker badges for Ayush, Aditi, Dhruv, and Hemang (590025443)
- Slide-by-slide cue cards, target timestamps, verbatim speech quotes, and handover callouts
- Common Committee Q&A cheat sheet
- Output to docs/PBL_DEFENSE_SPEECH_SCRIPT.pdf and Desktop
"""

import os
import subprocess
import base64

def generate_script_pdf():
    # Read logos as base64
    upes_logo_b64 = ""
    badge_b64 = ""
    
    if os.path.exists('docs/assets/template_extracted/s1_pic_1.jpg'):
        with open('docs/assets/template_extracted/s1_pic_1.jpg', 'rb') as f:
            upes_logo_b64 = base64.b64encode(f.read()).decode('utf-8')
            
    if os.path.exists('docs/assets/template_extracted/s1_pic_0.png'):
        with open('docs/assets/template_extracted/s1_pic_0.png', 'rb') as f:
            badge_b64 = base64.b64encode(f.read()).decode('utf-8')

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Adapt OS — Final PBL Defense Presentation Script</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 18mm 18mm 20mm 18mm;
    @bottom-center {{
      content: "Adapt OS PBL Final Defense Script | School of Computer Science, UPES Dehradun | Page " counter(page);
      font-family: 'Helvetica Neue', Arial, sans-serif;
      font-size: 8pt;
      color: #64748b;
    }}
  }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    line-height: 1.55;
    font-size: 10pt;
    margin: 0;
    padding: 0;
    background-color: #ffffff;
  }}

  .header-table {{
    width: 100%;
    border-bottom: 2px solid #0b192c;
    padding-bottom: 12px;
    margin-bottom: 20px;
  }}

  .header-title {{
    font-size: 16pt;
    font-weight: 800;
    color: #0b192c;
    margin: 0 0 4px 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}

  .header-subtitle {{
    font-size: 10pt;
    font-weight: 600;
    color: #1b4f72;
    margin: 0 0 4px 0;
  }}

  .header-meta {{
    font-size: 8.5pt;
    color: #64748b;
    margin: 0;
  }}

  .logo-cell {{
    text-align: right;
    vertical-align: middle;
  }}

  .logo-img {{
    height: 48px;
    margin-left: 10px;
  }}

  .badge-img {{
    height: 44px;
  }}

  /* Schedule & Summary Table */
  .schedule-box {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 24px;
  }}

  .schedule-title {{
    font-size: 11pt;
    font-weight: 700;
    color: #0b192c;
    margin-top: 0;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}

  .schedule-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
  }}

  .schedule-table th {{
    background: #0b192c;
    color: #ffffff;
    text-align: left;
    padding: 6px 10px;
    font-weight: 600;
  }}

  .schedule-table td {{
    padding: 6px 10px;
    border-bottom: 1px solid #e2e8f0;
  }}

  .schedule-table tr:last-child td {{
    border-bottom: none;
  }}

  /* Speaker Badges */
  .badge {{
    display: inline-block;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 8pt;
    font-weight: 700;
    letter-spacing: 0.3px;
    text-transform: uppercase;
  }}
  .badge-ayush {{ background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }}
  .badge-aditi {{ background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }}
  .badge-dhruv {{ background: #f5f3ff; color: #6d28d9; border: 1px solid #ddd6fe; }}
  .badge-hemang {{ background: #fffbeb; color: #b45309; border: 1px solid #fde68a; }}

  /* Speaker Section Headers */
  .speaker-section-header {{
    background: #0b192c;
    color: #ffffff;
    padding: 8px 14px;
    border-radius: 6px;
    font-size: 11pt;
    font-weight: 700;
    margin-top: 24px;
    margin-bottom: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    page-break-after: avoid;
  }}

  .speaker-meta {{
    font-size: 8.5pt;
    font-weight: 400;
    color: #46b0fa;
  }}

  /* Cue Card for Each Slide */
  .cue-card {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #0b192c;
    border-radius: 4px;
    padding: 10px 14px;
    margin-bottom: 14px;
    page-break-inside: avoid;
  }}
  .cue-ayush {{ border-left-color: #0284c7; }}
  .cue-aditi {{ border-left-color: #059669; }}
  .cue-dhruv {{ border-left-color: #7c3aed; }}
  .cue-hemang {{ border-left-color: #d97706; }}

  .cue-header {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    border-bottom: 1px dashed #e2e8f0;
    padding-bottom: 4px;
    margin-bottom: 8px;
  }}

  .slide-title {{
    font-size: 9.5pt;
    font-weight: 700;
    color: #0b192c;
    margin: 0;
  }}

  .slide-time {{
    font-size: 8pt;
    font-weight: 600;
    color: #64748b;
  }}

  .speech-text {{
    font-size: 9.5pt;
    color: #1e293b;
    margin: 0 0 6px 0;
    text-align: justify;
    line-height: 1.5;
  }}

  .speech-text:last-child {{
    margin-bottom: 0;
  }}

  .speech-text strong {{
    color: #0f172a;
    font-weight: 600;
  }}

  .transition-box {{
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 8.5pt;
    font-style: italic;
    color: #334155;
    margin-top: 8px;
  }}

  /* Q&A Section */
  .qa-card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 10px 14px;
    margin-bottom: 10px;
    page-break-inside: avoid;
  }}

  .qa-q {{
    font-size: 9pt;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 4px;
  }}

  .qa-a {{
    font-size: 8.5pt;
    color: #334155;
    margin: 0;
    line-height: 1.45;
  }}

  .page-break {{
    page-break-before: always;
  }}
</style>
</head>
<body>

<!-- HEADER BLOCK -->
<table class="header-table">
  <tr>
    <td style="width: 65%;">
      <div class="header-title">Adapt OS — Final Defense Speech Script</div>
      <div class="header-subtitle">Project-Based Learning (PBL) Final Examination & Defense</div>
      <div class="header-meta">
        <strong>Mentor:</strong> Prof. Shubranil Das | <strong>School of Computer Science</strong>, UPES Dehradun<br>
        <strong>Allocated Presentation Duration:</strong> 15 Minutes (18 Widescreen Slides)
      </div>
    </td>
    <td class="logo-cell">
      <img src="data:image/png;base64,__BADGE_B64__" class="badge-img" alt="Badge">
      <img src="data:image/jpeg;base64,__UPES_LOGO_B64__" class="logo-img" alt="UPES Logo">
    </td>
  </tr>
</table>

<!-- SCHEDULE & SPEAKER ROSTER -->
<div class="schedule-box">
  <div class="schedule-title">Speaker Rotation & Timeline Matrix (14:30 Runtime + Q&A Buffer)</div>
  <table class="schedule-table">
    <thead>
      <tr>
        <th>Speaker</th>
        <th>SAP ID</th>
        <th>Slides</th>
        <th>Time Window</th>
        <th>Core Academic & Technical Domain</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><span class="badge badge-ayush">Ayush Pandey</span> <em>(Lead)</em></td>
        <td><strong>590025156</strong></td>
        <td>1 – 5</td>
        <td>0:00 – 3:45 (3.75 min)</td>
        <td>Introduction, Reactive Latency Tax, Kernel ML Dilemma, Literature Survey</td>
      </tr>
      <tr>
        <td><span class="badge badge-aditi">Aditi Singh</span></td>
        <td><strong>590025914</strong></td>
        <td>6 – 9</td>
        <td>3:45 – 7:15 (3.50 min)</td>
        <td>Two-Tier Architecture, 5-Channel Telemetry, 5 Time-Series ML Models, Accuracy vs Latency</td>
      </tr>
      <tr>
        <td><span class="badge badge-dhruv">Dhruv Jha</span></td>
        <td><strong>590023509</strong></td>
        <td>10 – 13</td>
        <td>7:15 – 10:45 (3.50 min)</td>
        <td>Policy Engine Math, Deterministic Safety Guard, Queuing Latency, Throttling & SLA</td>
      </tr>
      <tr>
        <td><span class="badge badge-hemang">Hemang Gupta</span></td>
        <td><strong>590025443</strong></td>
        <td>14 – 18</td>
        <td>10:45 – 14:30 (3.75 min)</td>
        <td>Dynamic Trace Timeline, Ablation Study, TreeSHAP XAI, Overhead Feasibility, Conclusion & eBPF</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- ========================================================================= -->
<!-- SECTION 1: AYUSH PANDEY -->
<!-- ========================================================================= -->
<div class="speaker-section-header">
  <span>SECTION 1: MOTIVATION, PROBLEM STATEMENT & LITERATURE SURVEY</span>
  <span class="speaker-meta">Speaker: Ayush Pandey (590025156) | Slides 1–5 | Duration: ~3.5 Mins</span>
</div>

<!-- Slide 1 -->
<div class="cue-card cue-ayush">
  <div class="cue-header">
    <span class="slide-title">Slide 1: Title Slide & Team Roster</span>
    <span class="slide-time">0:00 – 0:40 (40s)</span>
  </div>
  <p class="speech-text">
    "A very good morning to our respected faculty mentor, <strong>Prof. Shubranil Das</strong>, and esteemed members of the examination committee.
  </p>
  <p class="speech-text">
    My name is <strong>Ayush Pandey</strong>, and alongside my teammates <strong>Aditi Singh</strong>, <strong>Dhruv Jha</strong>, and <strong>Hemang Gupta</strong>, we are proud to present our final Project-Based Learning defense on: <strong>'Adapt: Forecast-Driven Intelligent Resource Management for Operating Systems.'</strong>
  </p>
  <p class="speech-text">
    In modern multi-tenant cloud servers and containerized microservices, resource allocation is governed by Linux kernel scheduling primitives. Today, we demonstrate how our decoupled two-tier machine learning architecture solves one of the oldest systemic challenges in operating systems: the <strong>Reactive Latency Tax</strong>."
  </p>
</div>

<!-- Slide 2 -->
<div class="cue-card cue-ayush">
  <div class="cue-header">
    <span class="slide-title">Slide 2: Executive Summary & Project Highlights</span>
    <span class="slide-time">0:40 – 1:30 (50s)</span>
  </div>
  <p class="speech-text">
    "To begin with an executive summary of our findings: Traditional operating system resource controllers—such as the Linux Completely Fair Scheduler (CFS) paired with Cgroups v2 <code>cpu.max</code> quotas—operate reactively. By the time a sudden demand spike is observed through CPU saturation thresholds, the application has already suffered from queue buildup and severe request throttling.
  </p>
  <p class="speech-text">
    To solve this, we built <strong>Adapt</strong>, a proactive resource allocator that forecasts future tenant demand using multi-step machine learning and dynamically resizes Cgroups v2 quotas <em>before</em> demand arrives. Over empirical benchmarking across multi-tenant trace environments, Adapt achieved four breakthrough results:
  </p>
  <p class="speech-text">
    1. A <strong>99.2% reduction in tail queuing latency</strong>, dropping P95 latency from over 1,000 milliseconds down to just 8.4 milliseconds.<br>
    2. Complete elimination of SLA breaches, maintaining <strong>0.0% SLA violations</strong> compared to over 41% in reactive controllers.<br>
    3. An <strong>87.2% reduction in CFS throttling duration</strong>, slashing cumulative throttling from 39 seconds down to 5 seconds.<br>
    4. And critically, a <strong>sub-0.15 millisecond execution overhead</strong>, proving that our user-space daemon consumes less than 0.015% of the 1-second scheduling epoch."
  </p>
</div>

<!-- Slide 3 -->
<div class="cue-card cue-ayush">
  <div class="cue-header">
    <span class="slide-title">Slide 3: Problem Statement: The 'Reactive Latency Tax'</span>
    <span class="slide-time">1:30 – 2:20 (50s)</span>
  </div>
  <p class="speech-text">
    "Let us examine why current operating systems struggle with bursty workloads, as visualized in this timeline figure.
  </p>
  <p class="speech-text">
    Under Linux CFS bandwidth control, a container is given a fixed runtime quota per period. When an unexpected traffic surge arrives at time <em>t = 45</em>, the container exhausts its quota in the first 15 milliseconds. The kernel's <code>cfs_bandwidth</code> timer immediately puts the entire cgroup to sleep for the remainder of the period.
  </p>
  <p class="speech-text">
    Standard reactive auto-scalers only sample utilization periodically. They detect saturation at epoch 46, calculate a new quota, and actuate at epoch 47. This creates a 2-epoch <strong>allocation deficit</strong>. During this window, thousands of incoming client requests pile up in the OS runqueue. Even after CPU quota is finally expanded, the server spends seconds draining the queued backlog. This is the <strong>'Reactive Latency Tax.'</strong> Our key insight: <em>If you wait until utilization crosses 80% to react, you have already lost.</em> Resource scaling must be proactive."
  </p>
</div>

<!-- Slide 4 -->
<div class="cue-card cue-ayush">
  <div class="cue-header">
    <span class="slide-title">Slide 4: Architectural Dilemma: Why In-Kernel ML is Infeasible</span>
    <span class="slide-time">2:20 – 3:00 (40s)</span>
  </div>
  <p class="speech-text">
    "A natural question arises: <em>Why not embed a machine learning model directly inside the Linux kernel's <code>schedule()</code> function?</em>
  </p>
  <p class="speech-text">
    As systems researchers, we recognized three strict kernel design constraints that make in-kernel ML impossible:
  </p>
  <p class="speech-text">
    1. <strong>FPU Prohibitions:</strong> The Linux kernel scheduler executes in atomic context where Floating-Point Unit (FPU) registers are disabled to avoid massive context-switch save/restore overhead.<br>
    2. <strong>Sub-Microsecond Budget:</strong> The kernel's <code>pick_next_task()</code> function must execute within 500 nanoseconds to 1 microsecond. Neural network tensor operations take anywhere from 80 microseconds to 15 milliseconds—exceeding the kernel's dispatch budget by up to four orders of magnitude!<br>
    3. <strong>Kernel Panic Risk:</strong> Any memory leak or unhandled exception in kernel space crashes the entire host OS node.<br>
    Therefore, we designed a <strong>Decoupled Two-Tier Architecture</strong>: We leave the kernel's microsecond-level dispatching untouched, and host the ML intelligence in an asynchronous, non-blocking user-space daemon."
  </p>
</div>

<!-- Slide 5 -->
<div class="cue-card cue-ayush">
  <div class="cue-header">
    <span class="slide-title">Slide 5: Literature Review & Research Gap Analysis</span>
    <span class="slide-time">3:00 – 3:45 (45s)</span>
  </div>
  <p class="speech-text">
    "In our survey of prior literature shown in this comparison table: Google's <strong>Autopilot</strong> (EuroSys '20) operates on multi-hour historical windows, making it too slow for sub-minute bursts. Stanford's <strong>Quasar</strong> (ASPLOS '14) performs coarse-grained black-box core allocation at admission, but cannot dynamically tune fine-grained quotas during runtime. Systems like <strong>FIRM</strong> (OSDI '20) leverage Reinforcement Learning, but suffer from high exploration penalties and convergence instability. And MIT's <strong>Caladan</strong> (OSDI '20) shifts dedicated cores at millisecond scales, but requires dedicated CPU core pinning, making it impractical for dense multi-tenant cgroups.
  </p>
  <p class="speech-text">
    <strong>Our Research Gap:</strong> Prior systems either operate at multi-minute intervals or rely on reactive threshold feedback. Adapt bridges this gap by coupling fine-grained 1-second supervised forecasting with deterministic OS safety guards.
  </p>
  <div class="transition-box">
    <strong>Handover Cue:</strong> "Now, I hand over to <strong>Aditi Singh</strong>, who will explain our two-tier system architecture and machine learning pipeline."
  </div>
</div>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- SECTION 2: ADITI SINGH -->
<!-- ========================================================================= -->
<div class="speaker-section-header" style="background: #047857;">
  <span>SECTION 2: SYSTEM ARCHITECTURE, TELEMETRY & ML ENGINE</span>
  <span class="speaker-meta">Speaker: Aditi Singh (590025914) | Slides 6–9 | Duration: ~3.5 Mins</span>
</div>

<!-- Slide 6 -->
<div class="cue-card cue-aditi">
  <div class="cue-header">
    <span class="slide-title">Slide 6: Proposed System Architecture: Two-Tier Decoupled Design</span>
    <span class="slide-time">3:45 – 4:35 (50s)</span>
  </div>
  <p class="speech-text">
    "Thank you, Ayush.
  </p>
  <p class="speech-text">
    Moving to the structural design of <strong>Adapt</strong>, as illustrated in our architecture block diagram: Adapt separates the problem into two distinct execution tiers:
  </p>
  <p class="speech-text">
    <strong>Tier 1 — The User-Space Intelligence Daemon (<code>adapt-daemon</code>):</strong><br>
    Every 1-second epoch, the daemon samples non-blocking telemetry counters from <code>/proc</code> and <code>/sys/fs/cgroup</code>. The telemetry is fed into our inference engine, where a trained time-series model projects workload demand 3 steps into the future. This forecast passes through our Policy Engine and Deterministic Safety Guard, which outputs a safe, smoothed CPU quota.
  </p>
  <p class="speech-text">
    <strong>Tier 2 — The Linux Kernel Enforcement:</strong><br>
    The daemon applies the quota through the standard Linux Cgroups v2 virtual file system by writing to <code>/sys/fs/cgroup/&lt;group&gt;/cpu.max</code>. Inside the kernel, the native Completely Fair Scheduler handles thread runqueues, red-black tree dispatching, and timeslice allocation at full native speed.
  </p>
  <p class="speech-text">
    Crucially, <strong>Adapt requires zero kernel modifications or custom patches.</strong> It runs on standard, unmodified mainline Linux with complete backward compatibility."
  </p>
</div>

<!-- Slide 7 -->
<div class="cue-card cue-aditi">
  <div class="cue-header">
    <span class="slide-title">Slide 7: Multidimensional Telemetry & Feature Engineering</span>
    <span class="slide-time">4:35 – 5:25 (50s)</span>
  </div>
  <p class="speech-text">
    "High-accuracy forecasting depends on rich physical telemetry. Rather than relying solely on historical CPU utilization, Adapt ingests <strong>5 multidimensional telemetry channels</strong>:
  </p>
  <p class="speech-text">
    1. Current CPU utilization percentage.<br>
    2. Memory Resident Set Size (RSS in Megabytes).<br>
    3. Disk I/O operations per second (IOPS).<br>
    4. Active task and thread count from <code>/proc/loadavg</code>.<br>
    5. Ingress network request inflow rate.
  </p>
  <p class="speech-text">
    We construct a strict <strong>zero-leakage chronological sliding window</strong> using <em>W = 12</em> history steps (the past 12 seconds) to forecast <em>H = 3</em> horizon steps ahead. As revealed by our correlation heatmap on the right, I/O rates and task counts exhibit a strong positive correlation (<em>r = +0.84</em>) with future CPU demand. In web and database workloads, disk reads and incoming network packets occur <em>before</em> the application begins heavy CPU computation. This physical property allows our model to detect workload surges before CPU counters even begin to spike!"
  </p>
</div>

<!-- Slide 8 -->
<div class="cue-card cue-aditi">
  <div class="cue-header">
    <span class="slide-title">Slide 8: Five Standard Time-Series ML Models Evaluated</span>
    <span class="slide-time">5:25 – 6:15 (50s)</span>
  </div>
  <p class="speech-text">
    "To identify the optimal model for low-latency operating systems control, we implemented and evaluated <strong>five standard ML/DL architectures</strong> alongside a statistical baseline under strictly identical training and validation splits:
  </p>
  <p class="speech-text">
    1. <strong>Support Vector Regression (SVR):</strong> Using a non-linear Radial Basis Function (RBF) kernel with <em>C = 100.0</em> and <em>&epsilon; = 0.05</em>.<br>
    2. <strong>Random Forest Regressor:</strong> An ensemble of 100 decorrelated decision trees with a maximum depth of 12.<br>
    3. <strong>XGBoost Regressor:</strong> A gradient-boosted tree model with 80 estimators, learning rate <em>&eta; = 0.08</em>, and tree depth 5.<br>
    4. <strong>Long Short-Term Memory (LSTM):</strong> A 2-layer stacked recurrent neural network with 64 units and dropout regularization of 0.20.<br>
    5. <strong>Gated Recurrent Unit (GRU):</strong> A 2-layer network with 48 units designed for faster temporal parameter convergence.<br>
    6. And an <strong>Exponentially Weighted Moving Average (EWMA)</strong> statistical forecaster serving as a non-learning baseline."
  </p>
</div>

<!-- Slide 9 -->
<div class="cue-card cue-aditi">
  <div class="cue-header">
    <span class="slide-title">Slide 9: Forecasting Model Evaluation: Accuracy vs. Inference Latency</span>
    <span class="slide-time">6:15 – 7:15 (60s)</span>
  </div>
  <p class="speech-text">
    "This brings us to our empirical model evaluation table and trade-off scatter plot. In an operating systems daemon, forecasting accuracy is useless if inference takes too long.
  </p>
  <p class="speech-text">
    Deep learning models like LSTM and GRU achieved excellent accuracy—LSTM recorded an MAE of 4.05% and a Directional Accuracy of 94.6%. However, LSTM required <strong>14.82 milliseconds of inference latency</strong>, which imposes an unacceptably heavy compute footprint on a host daemon.
  </p>
  <p class="speech-text">
    Conversely, <strong>XGBoost achieved an MAE of 4.12% and 94.2% Directional Accuracy—virtually identical to LSTM—while executing in just 0.082 milliseconds (82 microseconds)!</strong> XGBoost is <strong>180 times faster than LSTM</strong> because its decision tree splits can be traversed with branch-predicted cache-aligned CPU instructions. With a 94.2% directional accuracy, XGBoost almost never misses an upcoming burst. We selected XGBoost as Adapt’s production engine.
  </p>
  <div class="transition-box">
    <strong>Handover Cue:</strong> "I now invite <strong>Dhruv Jha</strong> to explain how these forecasts are transformed into safe kernel control policies."
  </div>
</div>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- SECTION 3: DHRUV JHA -->
<!-- ========================================================================= -->
<div class="speaker-section-header" style="background: #6d28d9;">
  <span>SECTION 3: CONTROL POLICY, SAFETY & BENCHMARK RESULTS</span>
  <span class="speaker-meta">Speaker: Dhruv Jha (590023509) | Slides 10–13 | Duration: ~3.5 Mins</span>
</div>

<!-- Slide 10 -->
<div class="cue-card cue-dhruv">
  <div class="cue-header">
    <span class="slide-title">Slide 10: Policy Engine & Mathematical Control Formalization</span>
    <span class="slide-time">7:15 – 8:05 (50s)</span>
  </div>
  <p class="speech-text">
    "Thank you, Aditi.
  </p>
  <p class="speech-text">
    Having an accurate forecast is only half the battle. If a daemon directly sets CPU quota to raw predicted demand, sudden micro-bursts will cause clipping, and noise will cause quota thrashing. Our <strong>Policy Engine</strong> formalizes resource allocation through three mathematical mechanisms:
  </p>
  <p class="speech-text">
    <strong>1. Proactive Headroom Scaling:</strong> <code>Alloc_target(t+1) = D_hat(t+1) * (1 + alpha_headroom)</code>. We incorporate a 15% safety headroom (<em>&alpha; = 0.15</em>) to absorb instantaneous micro-spikes between 1-second sampling boundaries.<br>
    <strong>2. Asymmetric Hysteresis Damping:</strong> When demand surges (&Delta; &gt; 5%), we scale quota <strong>immediately</strong> to protect queuing latency. However, when demand recedes, we enforce a <strong>damped decay</strong> requiring 3 consecutive low-utilization epochs before releasing quota. This completely suppresses rapid quota flapping.<br>
    <strong>3. Bounded Clamping Invariant:</strong> Quotas are strictly clamped between a tenant minimum (0.2 cores) and host maximum (4.0 cores), guaranteeing tenant isolation."
  </p>
</div>

<!-- Slide 11 -->
<div class="cue-card cue-dhruv">
  <div class="cue-header">
    <span class="slide-title">Slide 11: Deterministic Safety Guard & CUSUM Concept Drift</span>
    <span class="slide-time">8:05 – 8:55 (50s)</span>
  </div>
  <p class="speech-text">
    "In systems engineering, production software must be fault-tolerant. What happens if the workload pattern shifts dramatically, or a telemetry sensor fails?
  </p>
  <p class="speech-text">
    As detailed in our <strong>Safety State Machine</strong>, Adapt implements two autonomous safeguards:
  </p>
  <p class="speech-text">
    1. <strong>Dynamic Confidence Scoring:</strong> We compute a real-time confidence score <em>C(t)</em> based on relative error. If <em>C(t) &ge; 0.70</em>, the system operates in <code>NORMAL_PROACTIVE</code> mode. If confidence dips between 0.40 and 0.70, it enters <code>DEGRADED_HEADROOM</code> mode, automatically doubling headroom to 30%.<br>
    2. <strong>CUSUM Residual Drift Detector:</strong> We track cumulative model drift using a Page-Hinkley CUSUM algorithm: <code>S_t = max(0, S_{t-1} + e_t - k)</code>. If cumulative residuals cross a threshold (<em>S_t &gt; 50</em>), an anomaly is declared, and the system transitions to <code>FALLBACK_REACTIVE</code> mode, safely defaulting to proportional feedback control until the model recovers.<br>
    Under no circumstance can a model failure compromise operating system stability."
  </p>
</div>

<!-- Slide 12 -->
<div class="cue-card cue-dhruv">
  <div class="cue-header">
    <span class="slide-title">Slide 12: OS Scheduling Benchmark: Queuing Latency Distribution</span>
    <span class="slide-time">8:55 – 9:50 (55s)</span>
  </div>
  <p class="speech-text">
    "Now let us examine the experimental benchmarks. We evaluated Adapt against three industry-standard baselines under identical bursty trace workloads: a <strong>Static Quota Allocation</strong> (fixed at 2.0 cores), a <strong>Reactive Threshold Daemon</strong> (standard 80% watermark rule), and a <strong>CFS-like Reactive Resource-Control Baseline</strong> that models reactive quota feedback with observation lag.
  </p>
  <p class="speech-text">
    As displayed in our latency distribution graph: Static allocation suffered an intolerable P95 latency of <strong>1,020 milliseconds</strong> and P99 of <strong>2,150 milliseconds</strong> during 3.5-core bursts. The CFS-like Reactive baseline recorded a P95 of <strong>520 milliseconds</strong> and P99 of <strong>1,240 milliseconds</strong> due to reactive allocation lag.
  </p>
  <p class="speech-text">
    <strong>Adapt compressed P50 latency to 2.1 milliseconds, P95 to 8.4 milliseconds, and P99 to 18.2 milliseconds!</strong> This represents a <strong>99.2% reduction in tail queuing latency</strong> over static quotas and a <strong>98.4% reduction</strong> over reactive baselines."
  </p>
</div>

<!-- Slide 13 -->
<div class="cue-card cue-dhruv">
  <div class="cue-header">
    <span class="slide-title">Slide 13: SLA Violations & CPU Throttling Mitigation</span>
    <span class="slide-time">9:50 – 10:45 (55s)</span>
  </div>
  <p class="speech-text">
    "Tail latency directly determines Service Level Agreements (SLAs). In our benchmark, we defined an SLA breach as any request taking longer than 50 milliseconds to complete.
  </p>
  <p class="speech-text">
    As shown on the left chart: The Reactive Threshold daemon breached SLAs for <strong>41.2%</strong> of the runtime. The CFS-like baseline violated SLAs for <strong>33.4%</strong> of the run. <strong>Adapt achieved exactly 0.0% SLA violations across the entire benchmark.</strong>
  </p>
  <p class="speech-text">
    Looking at the right chart, we see why: Adapt reduced total CFS throttling duration from <strong>39.0 seconds down to 5.0 seconds</strong>—an <strong>87.2% reduction</strong>. By pre-allocating quota into the cgroup bandwidth bucket 1 epoch before bursts arrive, runnable tasks find the quota ready and execute without ever hitting the kernel throttling wall.
  </p>
  <div class="transition-box">
    <strong>Handover Cue:</strong> "I now hand over to <strong>Hemang Gupta</strong>, who will walk us through the dynamic trace timeline, ablation study, model explainability, and concluding remarks."
  </div>
</div>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- SECTION 4: HEMANG GUPTA -->
<!-- ========================================================================= -->
<div class="speaker-section-header" style="background: #b45309;">
  <span>SECTION 4: TIMELINE, ABLATION, XAI & CONCLUSION</span>
  <span class="speaker-meta">Speaker: Hemang Gupta (590025443) | Slides 14–18 | Duration: ~3.75 Mins</span>
</div>

<!-- Slide 14 -->
<div class="cue-card cue-hemang">
  <div class="cue-header">
    <span class="slide-title">Slide 14: Dynamic Timeline: Proactive Lead vs. Reactive Deficit</span>
    <span class="slide-time">10:45 – 11:35 (50s)</span>
  </div>
  <p class="speech-text">
    "Thank you, Dhruv.
  </p>
  <p class="speech-text">
    To understand the exact physical mechanics driving these gains, let us inspect this epoch-by-epoch execution timeline between epochs 40 and 60.
  </p>
  <p class="speech-text">
    At epoch <em>t = 44</em>, our XGBoost model anticipates that upcoming demand will spike from 1.5 cores to 3.2 cores at epoch 45. Within 140 microseconds, Adapt proactively raises the Cgroups v2 <code>cpu.max</code> allocation to 3.68 cores. When the workload burst lands at <em>t = 45</em>, sufficient CPU bandwidth is already available. The tasks execute without delay, and queuing latency remains below 5 milliseconds.
  </p>
  <p class="speech-text">
    In contrast, observe the CFS-like reactive baseline in orange: At <em>t = 45</em>, it is trapped at 2.0 cores. It exhausts its quota within 15 milliseconds, throttles the application, and only increases allocation at <em>t = 47</em>. By then, an enormous queue has formed. This trace provides definitive empirical proof: <strong>Adapt demonstrates a proactive response window that eliminates the reactive deficit.</strong>"
  </p>
</div>

<!-- Slide 15 -->
<div class="cue-card cue-hemang">
  <div class="cue-header">
    <span class="slide-title">Slide 15: Component Ablation Study: Isolating Core Mechanisms</span>
    <span class="slide-time">11:35 – 12:20 (45s)</span>
  </div>
  <p class="speech-text">
    "To prove that our improvements stem from sound architectural engineering rather than incidental tuning, we conducted a rigorous <strong>Component Ablation Study (TC-03)</strong>:
  </p>
  <p class="speech-text">
    1. <strong>Full Adapt:</strong> Achieves 8.4 ms P95 latency with only 18 quota transitions.<br>
    2. <strong>Ablating Hysteresis:</strong> Without damping, quota transitions exploded from 18 to <strong>204 transitions</strong>—an <strong>11.3x increase in quota thrashing</strong> that caused severe lock contention in the kernel's virtual file system.<br>
    3. <strong>Ablating Headroom (<em>&alpha; = 0</em>):</strong> P95 tail latency jumped from 8.4 ms to <strong>17.8 ms</strong>—a <strong>2.1x spike</strong>—because unpredicted micro-spikes clipped against exact demand.<br>
    4. <strong>Ablating ML (Static EWMA):</strong> Reverted directly to reactive behavior, failing to predict burst onsets.<br>
    This ablation proves that <strong>both Headroom and Hysteresis are mathematically necessary</strong> for kernel stability and tail latency containment."
  </p>
</div>

<!-- Slide 16 -->
<div class="cue-card cue-hemang">
  <div class="cue-header">
    <span class="slide-title">Slide 16: Explainable AI (XAI) via TreeSHAP Interpretability</span>
    <span class="slide-time">12:20 – 13:05 (45s)</span>
  </div>
  <p class="speech-text">
    "In operating systems, a controller cannot be a complete black box; system administrators require deterministic guarantees and explainability. We applied <strong>TreeSHAP</strong> to our trained XGBoost model to compute exact Shapley feature attributions for every scheduling decision:
  </p>
  <p class="speech-text">
    * <strong>I/O Request Rate</strong> emerged as the single largest contributor, accounting for <strong>48.5% of total model attribution</strong>. This makes complete physical sense: in modern Linux storage and network stacks, kernel I/O interrupts and buffer cache operations immediately precede CPU-intensive user-space computation.<br>
    * <strong>Active Task Count</strong> contributed <strong>28.2%</strong>, serving as an explicit arrival indicator for process thread creation.<br>
    * <strong>Historical CPU Usage</strong> provided the <strong>15.4%</strong> baseline.<br>
    TreeSHAP proves that our machine learning model is learning <strong>genuine physical causality in Linux workload behavior</strong>, rather than spurious statistical correlations."
  </p>
</div>

<!-- Slide 17 -->
<div class="cue-card cue-hemang">
  <div class="cue-header">
    <span class="slide-title">Slide 17: Actuator Overhead & Real-World Feasibility (TC-04)</span>
    <span class="slide-time">13:05 – 13:50 (45s)</span>
  </div>
  <p class="speech-text">
    "A critical concern in OS research is daemon overhead. Can a system run an ML model without robbing compute from tenant workloads? In Benchmark TC-04, we conducted microbenchmarks of every execution phase:
  </p>
  <p class="speech-text">
    * Feature extraction and XGBoost inference took <strong>82.4 microseconds</strong>.<br>
    * Policy and safety guard execution took <strong>18.1 microseconds</strong>.<br>
    * Simulated dry-run actuator calls took <strong>4.2 microseconds</strong>.<br>
    * Real Linux Cgroups v2 sysfs VFS writes to <code>cpu.max</code> took <strong>41.6 microseconds</strong>.<br>
    The <strong>total daemon execution pipeline completes in just 146.3 microseconds (0.146 ms)</strong>. In a 1-second control epoch, the Adapt daemon runs for 0.015% of the time and sleeps for <strong>99.985% of the epoch</strong>. Furthermore, the daemon's Resident Set Size remains strictly under 38 Megabytes. Our automated test suite of 20 unit tests passes in 5.3 seconds, verifying all invariants, clamping bounds, and safety fallback triggers."
  </p>
</div>

<!-- Slide 18 -->
<div class="cue-card cue-hemang">
  <div class="cue-header">
    <span class="slide-title">Slide 18: Conclusion, Future Roadmap & Defense</span>
    <span class="slide-time">13:50 – 14:40 (50s)</span>
  </div>
  <p class="speech-text">
    "To conclude our defense:
  </p>
  <p class="speech-text">
    1. We identified and quantified the <strong>Reactive Latency Tax</strong> in current Linux CFS bandwidth control.<br>
    2. We designed and implemented a <strong>Two-Tier Decoupled Architecture</strong> that safely deploys user-space ML intelligence without touching the microsecond kernel dispatch path.<br>
    3. We validated that <strong>XGBoost achieves sub-0.1ms inference with 94.2% directional accuracy</strong>, outperforming deep recurrent neural networks in systems efficiency.<br>
    4. We empirically demonstrated a <strong>99.2% reduction in tail queuing latency, 87.2% reduction in throttling, and zero SLA violations</strong>.
  </p>
  <p class="speech-text">
    <strong>Future Roadmap:</strong> With Linux kernel 6.12, the new <strong><code>sched_ext</code> (eBPF)</strong> framework allows pluggable user-space CPU schedulers. We plan to integrate Adapt's forecasting engine directly with <code>sched_ext</code> to dynamically tune scheduling slice duration alongside multi-resource memory (<code>memory.high</code>) and I/O weights.
  </p>
  <p class="speech-text">
    We express our heartfelt gratitude to our mentor, <strong>Prof. Shubranil Das</strong>, and the <strong>School of Computer Science, UPES Dehradun</strong>, for their invaluable guidance.
  </p>
  <p class="speech-text" style="font-weight: 700; color: #0b192c; font-size: 10pt;">
    "Thank you. We are now open for questions from the examination committee."
  </p>
</div>

<!-- ========================================================================= -->
<!-- JURY Q&A CHEAT SHEET -->
<!-- ========================================================================= -->
<div class="page-break"></div>
<div class="speaker-section-header" style="background: #1e293b;">
  <span>EXAMINATION COMMITTEE Q&A DEFENSE CHEAT SHEET</span>
  <span class="speaker-meta">Preparation for Committee Inquiry</span>
</div>

<div class="qa-card">
  <div class="qa-q">Q1 (For Ayush): "Why can't you just use an aggressive threshold like 70% instead of machine learning?"</div>
  <p class="qa-a">
    <strong>Answer:</strong> "A simple lower threshold increases allocation whenever utilization crosses 70%, but it remains purely reactive. Under sharp burst traffic, demand jumps from 30% to 100% in a single timeslice—crossing 70% and 100% simultaneously. Furthermore, aggressive low thresholds cause permanent over-provisioning and idle energy waste during normal operation. Machine learning gives us <em>predictive lead time</em> without permanent over-allocation."
  </p>
</div>

<div class="qa-card">
  <div class="qa-q">Q2 (For Aditi): "Why did you choose XGBoost over LSTM when LSTM had a slightly lower MAE (4.05% vs 4.12%)?"</div>
  <p class="qa-a">
    <strong>Answer:</strong> "In an operating systems daemon, latency and compute footprint are first-order design constraints. LSTM required 14.82 ms of inference time and significant CPU cycles for matrix operations, whereas XGBoost executed in 0.082 ms—180 times faster—while matching LSTM's directional accuracy at 94.2%. XGBoost leaves 99.9% of the host CPU core available for user tenant workloads."
  </p>
</div>

<div class="qa-card">
  <div class="qa-q">Q3 (For Dhruv): "What happens if your ML model predicts complete nonsense or crashes?"</div>
  <p class="qa-a">
    <strong>Answer:</strong> "That is the role of our Deterministic Safety Guard. We compute a continuous confidence score <em>C(t)</em> and track cumulative prediction drift using a CUSUM algorithm. If drift exceeds our safety threshold (<em>S_t &gt; 50</em>) or confidence drops below 0.40, the system automatically falls back to deterministic reactive proportional control. The kernel never blindly executes unvalidated ML output."
  </p>
</div>

<div class="qa-card">
  <div class="qa-q">Q4 (For Hemang): "How does your user-space actuation affect the kernel's actual scheduling?"</div>
  <p class="qa-a">
    <strong>Answer:</strong> "Adapt does not alter the microsecond <code>schedule()</code> function inside the kernel. Native Linux CFS continues to pick tasks from the runqueue at sub-microsecond latency. Adapt merely modulates the cgroup's <code>cpu.max</code> bandwidth boundary at 1-second intervals via sysfs, which takes only 41.6 microseconds. This cleanly decouples high-level resource policy from low-level thread dispatching."
  </p>
</div>

</body>
</html>
""".replace("__BADGE_B64__", badge_b64).replace("__UPES_LOGO_B64__", upes_logo_b64)

    html_path = 'docs/PBL_DEFENSE_SPEECH_SCRIPT.html'
    pdf_docs_path = 'docs/PBL_DEFENSE_SPEECH_SCRIPT.pdf'
    pdf_desk_path = '/Users/ayush9085/Desktop/PBL_DEFENSE_SPEECH_SCRIPT.pdf'

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Written HTML script to {html_path}")

    # Use Google Chrome headless to print to PDF
    chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    abs_html = os.path.abspath(html_path)
    abs_pdf = os.path.abspath(pdf_docs_path)

    cmd = [
        chrome_bin,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={abs_pdf}",
        f"file://{abs_html}"
    ]
    print("Running Chrome PDF generation...")
    subprocess.run(cmd, check=True)
    print(f"Generated PDF at {abs_pdf}")

    # Copy to Desktop
    import shutil
    shutil.copyfile(abs_pdf, pdf_desk_path)
    print(f"Copied PDF to Desktop: {pdf_desk_path}")

if __name__ == '__main__':
    generate_script_pdf()
