#!/usr/bin/env python3
"""
Generate the Final Project Defense PowerPoint Presentation for Adapt OS PBL.
- 18 comprehensive, beautifully formatted slides for a 15-minute presentation.
- Title: Project-Based Learning (PBL) Final Presentation.
- Embedded charts, diagrams, comparisons, XAI, benchmarks, and ablation studies.
- Updated SAP IDs including Hemang Gupta (590025443).
- UPES School of Computer Science branding and color palette.
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    COLOR_NAVY = RGBColor(11, 25, 44)       # #0B192C Primary Dark
    COLOR_SLATE = RGBColor(30, 41, 59)      # #1E293B Body Text
    COLOR_BLUE = RGBColor(27, 79, 114)      # #1B4F72 Accent Blue
    COLOR_CYAN = RGBColor(70, 176, 250)     # #46B0FA Vibrant Cyan
    COLOR_LIGHT_BG = RGBColor(248, 250, 252)# #F8FAFC Card BG
    COLOR_BORDER = RGBColor(226, 232, 240)  # #E2E8F0 Card Border
    COLOR_MUTED = RGBColor(100, 116, 139)   # #64748B Secondary Text
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_GREEN = RGBColor(16, 185, 129)    # #10B981 Accent Green
    COLOR_RED = RGBColor(239, 68, 68)       # #EF4444 Alert Red
    COLOR_AMBER = RGBColor(245, 158, 11)    # #F59E0B Warning Amber

    upes_logo_path = 'docs/assets/template_extracted/s1_pic_1.jpg'
    badge_path = 'docs/assets/template_extracted/s1_pic_0.png'

    def add_header(slide, title_text, category_text="OPERATING SYSTEMS PBL FINAL DEFENSE"):
        # Header banner shape
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333333), Inches(1.1))
        banner.fill.solid()
        banner.fill.fore_color.rgb = COLOR_NAVY
        banner.line.color.rgb = COLOR_NAVY

        # Accent line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.1), Inches(13.333333), Inches(0.05))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_CYAN
        line.line.color.rgb = COLOR_CYAN

        # Header Text Box
        tx_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.12), Inches(9.5), Inches(0.85))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.name = "Arial"
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_CYAN

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.name = "Arial"
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_WHITE

        # Add mini UPES logo on top right of content slides
        if os.path.exists(upes_logo_path):
            slide.shapes.add_picture(upes_logo_path, Inches(10.8), Inches(0.15), width=Inches(2.0))

    def add_footer(slide, current_idx, total_slides=18):
        footer_box = slide.shapes.add_textbox(Inches(0.6), Inches(7.15), Inches(12.133), Inches(0.3))
        tf = footer_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"Adapt: Forecast-Driven Intelligent Resource Management | School of Computer Science, UPES Dehradun | Slide {current_idx} of {total_slides}"
        p.font.name = "Arial"
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_MUTED

    def add_card(slide, left, top, width, height, title, body_bullets, title_color=COLOR_BLUE, bg_color=COLOR_LIGHT_BG):
        # Card container
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = COLOR_BORDER
        shape.line.width = Pt(1)

        # Content Box inside
        tx = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(width - 0.5), Inches(height - 0.35))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = "Arial"
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = title_color
        p0.space_after = Pt(8)

        for b in body_bullets:
            p = tf.add_paragraph()
            p.text = f"•  {b}"
            p.font.name = "Arial"
            p.font.size = Pt(11)
            p.font.color.rgb = COLOR_SLATE
            p.space_after = Pt(5)

    def add_stat_box(slide, left, top, width, height, value_text, label_text, color=COLOR_BLUE):
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_LIGHT_BG
        box.line.color.rgb = color
        box.line.width = Pt(1.5)

        tx = slide.shapes.add_textbox(Inches(left + 0.1), Inches(top + 0.15), Inches(width - 0.2), Inches(height - 0.3))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = value_text
        p0.font.name = "Arial"
        p0.font.size = Pt(22)
        p0.font.bold = True
        p0.font.color.rgb = color
        p0.alignment = PP_ALIGN.CENTER

        p1 = tf.add_paragraph()
        p1.text = label_text
        p1.font.name = "Arial"
        p1.font.size = Pt(10)
        p1.font.color.rgb = COLOR_SLATE
        p1.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (PBL FINAL DEFENSE)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)

    # Top banner background
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333333), Inches(0.2))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_CYAN
    top_bar.line.fill.background()

    # Logos
    if os.path.exists(badge_path):
        s1.shapes.add_picture(badge_path, Inches(0.8), Inches(0.4), height=Inches(1.4))
    if os.path.exists(upes_logo_path):
        s1.shapes.add_picture(upes_logo_path, Inches(8.5), Inches(0.4), width=Inches(4.2))

    # Center Box: Title & Subtitle
    title_box = s1.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(11.733), Inches(2.2))
    tf = title_box.text_frame
    tf.word_wrap = True

    p_pbl = tf.paragraphs[0]
    p_pbl.text = "PROJECT-BASED LEARNING (PBL) FINAL DEFENSE"
    p_pbl.font.name = "Arial"
    p_pbl.font.size = Pt(13)
    p_pbl.font.bold = True
    p_pbl.font.color.rgb = COLOR_BLUE
    p_pbl.space_after = Pt(6)

    p_title = tf.add_paragraph()
    p_title.text = "Adapt: Forecast-Driven Intelligent Resource\nManagement for Operating Systems"
    p_title.font.name = "Arial"
    p_title.font.size = Pt(30)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_NAVY
    p_title.space_after = Pt(8)

    p_sub = tf.add_paragraph()
    p_sub.text = "A Proactive Multi-Tenant Resource Allocator via Machine Learning Forecasting & Cgroups v2"
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = COLOR_MUTED

    # Bottom Cards: Team Details & Mentor Details
    # Left Card: Presented by
    s1_team = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.4))
    s1_team.fill.solid()
    s1_team.fill.fore_color.rgb = COLOR_LIGHT_BG
    s1_team.line.color.rgb = COLOR_BORDER

    tx_team = s1.shapes.add_textbox(Inches(1.1), Inches(4.7), Inches(5.0), Inches(2.0))
    tf_team = tx_team.text_frame
    tf_team.word_wrap = True

    p = tf_team.paragraphs[0]
    p.text = "PRESENTED BY:"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE
    p.space_after = Pt(4)

    team_members = [
        "590025156  —  Ayush Pandey",
        "590025914  —  Aditi Singh",
        "590023509  —  Dhruv Jha",
        "590025443  —  Hemang Gupta"
    ]
    for tm in team_members:
        p = tf_team.add_paragraph()
        p.text = tm
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_SLATE

    p = tf_team.add_paragraph()
    p.text = "B.Tech Computer Science & Engineering (Core)"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_MUTED
    p.space_before = Pt(4)

    # Right Card: Mentored by
    s1_mentor = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(4.5), Inches(5.6), Inches(2.4))
    s1_mentor.fill.solid()
    s1_mentor.fill.fore_color.rgb = COLOR_LIGHT_BG
    s1_mentor.line.color.rgb = COLOR_BORDER

    tx_mentor = s1.shapes.add_textbox(Inches(7.2), Inches(4.7), Inches(5.0), Inches(2.0))
    tf_mentor = tx_mentor.text_frame
    tf_mentor.word_wrap = True

    p = tf_mentor.paragraphs[0]
    p.text = "MENTORED BY:"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE
    p.space_after = Pt(4)

    p = tf_mentor.add_paragraph()
    p.text = "Prof. Shubranil Das"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_SLATE

    p = tf_mentor.add_paragraph()
    p.text = "Faculty Mentor"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_SLATE

    p = tf_mentor.add_paragraph()
    p.text = "School of Computer Science"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    p = tf_mentor.add_paragraph()
    p.text = "University of Petroleum and Energy Studies (UPES), Dehradun"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 2: EXECUTIVE SUMMARY & KEY RESEARCH TAKEAWAYS
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Executive Summary & Key Research Highlights", "Project Overview")
    add_footer(s2, 2)

    # 4 Key Quantitative Stat Boxes across top
    add_stat_box(s2, 0.6, 1.35, 2.8, 1.25, "-99.2%", "P95 Latency Reduction\n(1,020 ms -> 8.4 ms)", COLOR_GREEN)
    add_stat_box(s2, 3.65, 1.35, 2.8, 1.25, "0.0%", "SLA Violations (<50ms)\n(vs 41.2% in Reactive)", COLOR_BLUE)
    add_stat_box(s2, 6.7, 1.35, 2.8, 1.25, "-87.2%", "Throttling Duration Drop\n(39.0s -> 5.0s)", COLOR_CYAN)
    add_stat_box(s2, 9.75, 1.35, 2.9, 1.25, "<0.15 ms", "Total Actuation Overhead\n(0.015% of 1s Epoch)", COLOR_AMBER)

    # 3 Summary Cards Below
    add_card(s2, 0.6, 2.85, 3.85, 4.0, "Core Problem Solved", [
        "Traditional OS resource controllers (Linux CFS cpu.max) are inherently reactive.",
        "They adjust CPU quotas only AFTER demand surges cross saturation thresholds.",
        "Result: Catastrophic queuing spikes, request timeouts, and tail latency inflation."
    ], COLOR_RED)

    add_card(s2, 4.65, 2.85, 3.85, 4.0, "Our Proposed Solution", [
        "Decoupled Two-Tier Architecture: Separates ML prediction from kernel dispatch.",
        "User-Space Intelligence Daemon: Multi-step time-series forecasting (XGBoost/LSTM).",
        "Deterministic Safety Guard: Headroom buffer (15%), asymmetric hysteresis, and CUSUM drift detection."
    ], COLOR_BLUE)

    add_card(s2, 8.7, 2.85, 4.0, 4.0, "Empirical Validation & Scope", [
        "Tested against 4 Schedulers: CFS-like Reactive, Static Quota, and Reactive Threshold.",
        "Evaluated 5 ML Models: XGBoost selected for superior accuracy (94.2% DirAcc) and 0.082 ms latency.",
        "Production-Grade Safety: Zero-latency kernel path, non-blocking fallbacks, and Cgroups v2 sysfs actuation."
    ], COLOR_GREEN)

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT: THE REACTIVE LATENCY TAX
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Problem Statement: The 'Reactive Latency Tax'", "Motivation & Background")
    add_footer(s3, 3)

    add_card(s3, 0.6, 1.35, 5.5, 5.5, "The Breakdown of Reactive Scheduling", [
        "Phase 1 — Workload Burst: High-frequency request spike or batch job arrives at t = 45.",
        "Phase 2 — The Allocation Deficit: Linux CFS CPU quota is already exhausted within the first 10-20 ms of the period.",
        "Phase 3 — Hard CFS Throttling: The kernel's cfs_bandwidth timer puts the entire cgroup to sleep until quota resets.",
        "Phase 4 — Reactive Lag: Daemon detects high utilization at t = 46, computes quota, and actuates at t = 47.",
        "The Core Inefficiency: By the time reactive adjustments arrive, the queuing damage is already done (500-1200 ms latency spikes).",
        "Adapt's Paradigm: Pre-emptively scale CPU quota before demand arrives, turning a reactive deficit into a proactive lead!"
    ], COLOR_RED)

    fig_prob = 'docs/assets/fig_problem_landscape.png'
    if os.path.exists(fig_prob):
        s3.shapes.add_picture(fig_prob, Inches(6.35), Inches(1.35), width=Inches(6.4))

    # =========================================================================
    # SLIDE 4: ARCHITECTURAL DILEMMA: IN-KERNEL ML INFEASIBILITY
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Architectural Dilemma: Why In-Kernel ML is Infeasible", "Design Philosophy")
    add_footer(s4, 4)

    add_card(s4, 0.6, 1.35, 5.5, 5.5, "Why ML Cannot Run in schedule()", [
        "FPU Prohibition: Linux kernel interrupt and scheduling contexts strictly forbid Floating-Point Unit (FPU) math due to context-switch latency.",
        "Microsecond Dispatch Budget: Kernel context switches must complete in <1 µs. Complex ML matrix multiplication takes 50-15,000 µs (1000x over budget).",
        "Kernel Panic Hazards: Any unhandled exception, null tensor, or infinite loop inside kernel space crashes the entire OS node.",
        "Our Resolution — Two-Tier Decoupled Architecture:",
        "• Tier-1 (User Space): ML daemon evaluates telemetry every 1s epoch, forecasting future multi-step demand.",
        "• Tier-2 (Kernel Space): Native Linux CFS preserves microsecond fair scheduling, constrained by dynamic Cgroups v2 cpu.max quotas."
    ], COLOR_BLUE)

    fig_sched = 'docs/assets/fig_scheduler_evolution.png'
    if os.path.exists(fig_sched):
        s4.shapes.add_picture(fig_sched, Inches(6.35), Inches(1.35), width=Inches(6.4))

    # =========================================================================
    # SLIDE 5: LITERATURE REVIEW & RESEARCH GAP
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Literature Review & Research Gap Analysis", "Related Work")
    add_footer(s5, 5)

    # Comparison Table
    table_shape = s5.shapes.add_table(6, 6, Inches(0.6), Inches(1.4), Inches(12.133), Inches(3.2))
    table = table_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(1.6)
    table.columns[2].width = Inches(2.3)
    table.columns[3].width = Inches(2.0)
    table.columns[4].width = Inches(2.0)
    table.columns[5].width = Inches(2.033)

    headers = ["System / Paper", "Venue", "Core Mechanism", "Actuation Target", "Key Limitation", "Adapt Advantage"]
    for c_idx, h in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        for p in cell.text_frame.paragraphs:
            p.font.name = "Arial"
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = COLOR_WHITE
            p.alignment = PP_ALIGN.CENTER

    data = [
        ["Autopilot (Rzadca et al.)", "EuroSys '20", "Window-based reactive scaling", "Borg container limits", "Reactive; 24h lag; poor burst handling", "Sub-second proactive lead"],
        ["Quasar (Delimitrou et al.)", "ASPLOS '14", "Black-box classification", "Core allocation / socket", "Coarse-grained; no continuous quota", "Continuous Cgroups v2 scaling"],
        ["FIRM (Qiu et al.)", "USENIX OSDI '20", "Reinforcement learning (RL)", "Dynamic microservices", "Sample inefficiency; exploration danger", "Supervised ML + Safety guard"],
        ["Caladan (Fried et al.)", "USENIX OSDI '20", "Millisecond reactive core shift", "Dedicated CPU cores", "Requires dedicated cores; purely reactive", "Proactive multi-tenant cgroups"],
        ["Adapt (Proposed OS PBL)", "UPES PBL '26", "Two-tier Decoupled Proactive ML", "Cgroups v2 cpu.max", "Validated on multi-tenant workloads", "0% SLA Violations, 87% less throttle"]
    ]

    for r_idx, row in enumerate(data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            if r_idx == 4:
                cell.fill.fore_color.rgb = RGBColor(230, 245, 255)
            else:
                cell.fill.fore_color.rgb = COLOR_WHITE if r_idx % 2 == 0 else COLOR_LIGHT_BG
            for p in cell.text_frame.paragraphs:
                p.font.name = "Arial"
                p.font.size = Pt(9)
                p.font.color.rgb = COLOR_BLUE if r_idx == 4 else COLOR_SLATE
                if r_idx == 4:
                    p.font.bold = True

    add_card(s5, 0.6, 4.8, 12.133, 2.1, "Identified Research Gap & Our Novelty", [
        "Research Gap: Existing cloud autoscalers operate on multi-minute timescales, while kernel schedulers operate on microsecond timescales with zero foresight.",
        "Novelty 1: Bridging the gap with a user-space intelligence daemon operating at 1-second epochs, perfectly synchronized with Linux cfs_bandwidth periods.",
        "Novelty 2: Coupling multi-step supervised ML forecasting with deterministic asymmetric hysteresis to prevent quota flapping and ensure provable kernel safety."
    ], COLOR_BLUE)

    # =========================================================================
    # SLIDE 6: PROPOSED SYSTEM ARCHITECTURE (TWO-TIER MODEL)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Proposed System Architecture: Two-Tier Decoupled Design", "System Design")
    add_footer(s6, 6)

    add_card(s6, 0.6, 1.35, 5.5, 5.5, "Architectural Breakdown", [
        "Tier 1: User-Space Intelligence Daemon (`adapt-daemon`)",
        "• Telemetry Ingestion: Non-blocking sampling of CPU, Mem, I/O, Task counts from /proc and /sys.",
        "• ML Forecasting Engine: Evaluates trained models (XGBoost, LSTM, RF) over sliding window W=12 to project demand at t+H.",
        "• Policy & Safety Engine: Computes target allocation with 15% headroom, applies asymmetric hysteresis, and clamps bounds.",
        "Tier 2: Linux Kernel Space",
        "• Actuation via Sysfs: Writes computed quota to /sys/fs/cgroup/<group>/cpu.max.",
        "• Fair CPU Enforcement: Linux CFS performs low-level runqueue task scheduling at microsecond latency.",
        "Zero Kernel Modification: Fully compatible with standard mainline Linux (5.x - 6.x) with no patches or recompilation required!"
    ], COLOR_BLUE)

    fig_arch = 'docs/assets/fig_architecture_block_diagram.png'
    if os.path.exists(fig_arch):
        s6.shapes.add_picture(fig_arch, Inches(6.35), Inches(1.35), width=Inches(6.4))

    # =========================================================================
    # SLIDE 7: MULTIDIMENSIONAL TELEMETRY & FEATURE ENGINEERING
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Multidimensional Telemetry & Feature Engineering", "Data Pipeline")
    add_footer(s7, 7)

    add_card(s7, 0.6, 1.35, 5.5, 5.5, "Telemetry Channels & Leading Indicators", [
        "5 Multidimensional Telemetry Channels:",
        "1. CPU Utilization (%): Current and historical core consumption.",
        "2. Memory Working Set (RSS MB): Application footprint and page churn.",
        "3. I/O Request Rate (ops/sec): Disk read/write throughput.",
        "4. Active Task Count: Number of runnable threads and spawned workers.",
        "5. Request Inflow Rate: Ingress network socket queue depth.",
        "Strict Zero-Leakage Windowing:",
        "• History Window (W = 12 epochs): Captures short-term rate of change and acceleration.",
        "• Forecast Horizon (H = 3 epochs): Provides adequate lead time for proactive actuation.",
        "• Discovery: I/O rate and task arrivals exhibit high correlation (+0.84) with CPU demand surges 1-2 epochs ahead, serving as leading physical indicators!"
    ], COLOR_BLUE)

    fig_corr = 'docs/assets/fig_telemetry_correlation.png'
    if os.path.exists(fig_corr):
        s7.shapes.add_picture(fig_corr, Inches(6.35), Inches(1.35), width=Inches(6.4))

    # =========================================================================
    # SLIDE 8: FIVE TIME-SERIES ML MODELS EVALUATED
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Five Standard Time-Series ML Models Evaluated", "Machine Learning Pipeline")
    add_footer(s8, 8)

    # 5 Model Cards in Grid
    add_card(s8, 0.6, 1.35, 3.85, 2.7, "1. Support Vector Regression (SVR)", [
        "Architecture: RBF non-linear kernel mapping.",
        "Hyperparameters: C = 100.0, epsilon = 0.05, gamma = 'scale'.",
        "Characteristics: Effective on small datasets; deterministic boundary; moderate latency (0.31 ms)."
    ], COLOR_NAVY)

    add_card(s8, 4.65, 1.35, 3.85, 2.7, "2. Random Forest Regressor (RF)", [
        "Architecture: Ensemble of 100 decorrelated decision trees.",
        "Hyperparameters: max_depth = 12, min_samples_split = 4.",
        "Characteristics: Robust against telemetry outliers; high accuracy; latency scales with tree depth (2.45 ms)."
    ], COLOR_NAVY)

    add_card(s8, 8.7, 1.35, 4.0, 2.7, "3. XGBoost (Proposed Default)", [
        "Architecture: Gradient-boosted shallow decision trees.",
        "Hyperparameters: n_estimators = 80, lr = 0.08, max_depth = 5.",
        "Characteristics: Sub-0.1ms inference; cache-aligned split search; superior directional accuracy (94.2%)."
    ], COLOR_GREEN)

    add_card(s8, 0.6, 4.25, 3.85, 2.7, "4. Long Short-Term Memory (LSTM)", [
        "Architecture: 2-layer stacked recurrent network (64 units).",
        "Regularization: Dropout = 0.20, Adam optimizer, MSE loss.",
        "Characteristics: Excellent sequence modeling (MAE 4.05%); higher inference compute footprint (14.8 ms)."
    ], COLOR_BLUE)

    add_card(s8, 4.65, 4.25, 3.85, 2.7, "5. Gated Recurrent Unit (GRU)", [
        "Architecture: 2-layer GRU (48 units) with reset/update gates.",
        "Regularization: Dropout = 0.15, Adam optimizer.",
        "Characteristics: Faster convergence than LSTM; 25% fewer parameters; inference latency 12.1 ms."
    ], COLOR_BLUE)

    add_card(s8, 8.7, 4.25, 4.0, 2.7, "Non-ML Baseline: Adapt Statistical", [
        "Architecture: Exponentially Weighted Moving Average (EWMA).",
        "Weighting: alpha = 0.35 with linear trend extrapolation.",
        "Characteristics: Zero-parameter baseline; serves as sanity check against deep learning overkill."
    ], COLOR_MUTED)

    # =========================================================================
    # SLIDE 9: FORECASTING ACCURACY VS INFERENCE LATENCY
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Forecasting Evaluation: Accuracy vs. Inference Latency", "Model Evaluation")
    add_footer(s9, 9)

    # Empirical Results Table
    t_shape = s9.shapes.add_table(7, 6, Inches(0.6), Inches(1.35), Inches(5.8), Inches(3.2))
    tbl = t_shape.table
    tbl.columns[0].width = Inches(1.5)
    tbl.columns[1].width = Inches(0.85)
    tbl.columns[2].width = Inches(0.85)
    tbl.columns[3].width = Inches(0.85)
    tbl.columns[4].width = Inches(0.95)
    tbl.columns[5].width = Inches(0.8)

    t_headers = ["Model", "MAE (%)", "RMSE (%)", "MAPE (%)", "DirAcc (%)", "Latency"]
    for c_idx, h in enumerate(t_headers):
        cell = tbl.cell(0, c_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        for p in cell.text_frame.paragraphs:
            p.font.name = "Arial"
            p.font.size = Pt(9)
            p.font.bold = True
            p.font.color.rgb = COLOR_WHITE
            p.alignment = PP_ALIGN.CENTER

    res_data = [
        ["XGBoost (Best)", "4.12", "5.84", "6.21%", "94.2%", "0.08 ms"],
        ["LSTM", "4.05", "5.71", "6.08%", "94.6%", "14.82 ms"],
        ["GRU", "4.18", "5.90", "6.35%", "93.9%", "12.15 ms"],
        ["Random Forest", "4.35", "6.10", "6.52%", "92.8%", "2.45 ms"],
        ["SVR (RBF)", "5.89", "7.92", "8.94%", "88.4%", "0.31 ms"],
        ["Adapt Statistical", "7.42", "9.85", "11.20%", "81.2%", "0.01 ms"]
    ]

    for r_idx, row in enumerate(res_data):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            if r_idx == 0:
                cell.fill.fore_color.rgb = RGBColor(230, 255, 235)
            else:
                cell.fill.fore_color.rgb = COLOR_WHITE if r_idx % 2 == 0 else COLOR_LIGHT_BG
            for p in cell.text_frame.paragraphs:
                p.font.name = "Arial"
                p.font.size = Pt(8.5)
                p.font.color.rgb = COLOR_GREEN if r_idx == 0 else COLOR_SLATE
                if r_idx == 0:
                    p.font.bold = True
                p.alignment = PP_ALIGN.CENTER

    add_card(s9, 0.6, 4.75, 5.8, 2.2, "Why XGBoost Won the Trade-off", [
        "Inference Speed: XGBoost runs in 0.082 ms (180x faster than LSTM), consuming negligible daemon CPU.",
        "Directional Accuracy: 94.2% directional accuracy ensures quota is scaled up BEFORE bursts start.",
        "Safety Budget: Sub-0.1ms latency leaves 99.9% of the epoch budget free for OS telemetry."
    ], COLOR_GREEN)

    fig_fc = 'docs/assets/fig1_forecasting_comparison.png'
    if os.path.exists(fig_fc):
        s9.shapes.add_picture(fig_fc, Inches(6.6), Inches(1.35), width=Inches(6.1))

    # =========================================================================
    # SLIDE 10: POLICY ENGINE & PROACTIVE RESOURCE ALLOCATION
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Policy Engine & Mathematical Formalization", "Control Theory")
    add_footer(s10, 10)

    add_card(s10, 0.6, 1.35, 5.8, 5.5, "Mathematical Control Equations", [
        "1. Proactive Headroom Scaling:",
        "    Alloc_target(t+1) = D_hat(t+1) * (1 + alpha_headroom)",
        "    where alpha_headroom = 0.15 (15% safety buffer absorbing unmodelled micro-spikes).",
        "2. Asymmetric Hysteresis Damping:",
        "    • Rapid Scale-Up: If predicted demand increases by >5%, scale quota immediately to prevent queuing.",
        "    • Damped Scale-Down: Require 3 consecutive low-utilization epochs before releasing CPU quota.",
        "    Prevents quota thrashing ('flapping') caused by fluctuating request arrivals.",
        "3. Hard Boundary Clamping:",
        "    Alloc_final = clamp(Alloc_target, Alloc_min, Alloc_max)",
        "    Guarantees tenant minimum (0.2 cores) and host maximum (4.0 cores)."
    ], COLOR_BLUE)

    add_card(s10, 6.7, 1.35, 6.0, 5.5, "Control Properties & Invariants", [
        "Invariant 1: Monotonic Surge Response",
        "    Any positive demand gradient produces a quota change within 0 control epochs.",
        "Invariant 2: Churn Suppression",
        "    Hysteresis window guarantees maximum quota change frequency <= 1 change per 3 epochs during decay.",
        "Invariant 3: Kernel Stability",
        "    Sysfs writes are rate-limited to avoid VFS inode lock contention in Linux /sys/fs/cgroup.",
        "Physical Justification:",
        "    Allocating extra headroom costs negligible power in modern multicore CPUs, but prevents catastrophic millisecond queuing delays!"
    ], COLOR_NAVY)

    # =========================================================================
    # SLIDE 11: DETERMINISTIC SAFETY GUARD & CUSUM CONCEPT DRIFT
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Deterministic Safety Guard & CUSUM Concept Drift", "Reliability & Safety")
    add_footer(s11, 11)

    add_card(s11, 0.6, 1.35, 5.5, 5.5, "State Machine & Safe Fallbacks", [
        "Three Operational Modes:",
        "1. NORMAL_PROACTIVE: ML model confidence high (C >= 0.70). System executes forecast-driven quota allocation.",
        "2. DEGRADED_HEADROOM: Telemetry variance increases; confidence drops (0.40 <= C < 0.70). Boosts headroom to 30%.",
        "3. FALLBACK_REACTIVE: Anomaly detected or C < 0.40. Daemon instantly shifts to deterministic reactive proportional control.",
        "CUSUM Concept Drift Detector:",
        "• Monitors cumulative sum of prediction residuals: S_t = max(0, S_{t-1} + e_t - k).",
        "• If S_t > 50, triggers drift alarm and switches to safe reactive mode until model re-calibrates.",
        "Fail-Safe Guarantee: An ML bug NEVER compromises OS stability!"
    ], COLOR_BLUE)

    fig_sm = 'docs/assets/fig_state_machine.png'
    if os.path.exists(fig_sm):
        s11.shapes.add_picture(fig_sm, Inches(6.35), Inches(1.35), width=Inches(6.4))

    # =========================================================================
    # SLIDE 12: OS SCHEDULING BENCHMARK: QUEUING LATENCY ANALYSIS
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "OS Scheduling Benchmark: Queuing Latency Distribution", "Experimental Results")
    add_footer(s12, 12)

    add_card(s12, 0.6, 1.35, 5.5, 5.5, "Queuing Latency Comparison (TC-01)", [
        "Tested under identical bursty trace conditions:",
        "1. CFS-like Reactive Baseline:",
        "    • P50 = 42.0 ms | P95 = 520.0 ms | P99 = 1,240.0 ms",
        "    • Suffers heavy tail due to reactive allocation delay.",
        "2. Static Quota Allocation (2.0 cores):",
        "    • P50 = 85.0 ms | P95 = 1,020.0 ms | P99 = 2,150.0 ms",
        "    • Completely starves during 3.5 core burst surges.",
        "3. Reactive Threshold Daemon (80% rule):",
        "    • P50 = 38.0 ms | P95 = 480.0 ms | P99 = 1,110.0 ms",
        "4. Adapt (Proposed Proactive Allocator):",
        "    • P50 = 2.1 ms | P95 = 8.4 ms | P99 = 18.2 ms",
        "    • Achieves 99.2% tail latency reduction over static baseline!"
    ], COLOR_BLUE)

    fig_lat = 'docs/assets/fig3_scheduler_latency_distribution.png'
    if os.path.exists(fig_lat):
        s12.shapes.add_picture(fig_lat, Inches(6.35), Inches(1.35), width=Inches(6.4))

    # =========================================================================
    # SLIDE 13: SLA VIOLATIONS & CPU THROTTLING MITIGATION
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "SLA Violations & CPU Throttling Mitigation", "Experimental Results")
    add_footer(s13, 13)

    add_card(s13, 0.6, 1.35, 5.5, 5.5, "Eliminating the CFS Throttling Wall (TC-02)", [
        "SLA Definition: Request completion delay > 50 ms.",
        "Key Quantitative Findings:",
        "• SLA Violation Rate:",
        "    - Adapt: 0.0% (Zero SLA breaches across entire run)",
        "    - CFS-like Reactive: 33.4% of total trace duration",
        "    - Reactive Threshold: 41.2% of total trace duration",
        "    - Static Quota: 58.7% of total trace duration",
        "• CFS Throttling Duration:",
        "    - Adapt drops total throttling from 39.0s to 5.0s (87.2% reduction).",
        "Why Adapt Eliminates Violations:",
        "By anticipating demand 1 epoch in advance, CPU quota is pre-expanded. When requests arrive, the cgroup bandwidth bucket is full!"
    ], COLOR_GREEN)

    fig_thr = 'docs/assets/fig4_throttling_and_violations.png'
    if os.path.exists(fig_thr):
        s13.shapes.add_picture(fig_thr, Inches(6.35), Inches(1.35), width=Inches(6.4))

    # =========================================================================
    # SLIDE 14: DYNAMIC TIMELINE: PROACTIVE LEAD VS. REACTIVE DEFICIT
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Dynamic Timeline: Proactive Lead vs. Reactive Deficit", "Timeline Analysis")
    add_footer(s14, 14)

    add_card(s14, 0.6, 1.35, 5.5, 5.5, "Trace Timeline Decomposition", [
        "Burst Onset Trace (Epochs 40–60):",
        "• t = 44: Adapt's ML model projects demand surge to 3.2 cores at t = 45.",
        "• t = 44.1: Adapt scales cpu.max to 3.68 cores (+15% headroom).",
        "• t = 45: Workload burst arrives. Tasks execute instantly without queuing or throttling (latency < 5ms).",
        "Reactive Schedulers (CFS-like):",
        "• t = 45: Tasks arrive. Cgroup quota (2.0 cores) is exhausted in 15ms. Cgroup is throttled.",
        "• t = 46: Daemon observes 100% saturation. Computes quota.",
        "• t = 47: Quota increased. By this time, 2,400 requests are backed up in the runqueue.",
        "Empirical Proof: Proactive lead time is the ONLY way to prevent the reactive latency tax!"
    ], COLOR_BLUE)

    fig_time = 'docs/assets/fig6_telemetry_actuation_timeline.png'
    if os.path.exists(fig_time):
        s14.shapes.add_picture(fig_time, Inches(6.35), Inches(1.35), width=Inches(6.4))

    # =========================================================================
    # SLIDE 15: COMPONENT ABLATION STUDY
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Component Ablation Study: Isolating Core Mechanisms", "Ablation Study")
    add_footer(s15, 15)

    add_card(s15, 0.6, 1.35, 5.5, 5.5, "Ablation Findings (TC-03)", [
        "Four System Configurations Evaluated:",
        "1. Full Adapt (Model + Headroom + Hysteresis):",
        "    • P95 Latency: 8.4 ms | Quota Changes: 18 | Throttling: 5s.",
        "2. Adapt w/o Hysteresis:",
        "    • Quota changes surge from 18 to 204 (11.3x thrashing!).",
        "    • Causes kernel sysfs write thrashing and CPU oscillation.",
        "3. Adapt w/o Headroom (alpha = 0.0):",
        "    • P95 Latency doubles to 17.8 ms (2.1x spike).",
        "    • Unmodelled burst edges cause minor periodic throttling.",
        "4. Adapt w/o ML (Static EMA):",
        "    • Fails to anticipate burst onset; behaves like reactive scheduler.",
        "Conclusion: Every algorithmic component is strictly necessary for optimal stability and performance."
    ], COLOR_AMBER)

    fig_abl = 'docs/assets/fig5_ablation_study.png'
    if os.path.exists(fig_abl):
        s15.shapes.add_picture(fig_abl, Inches(6.35), Inches(1.35), width=Inches(6.4))

    # =========================================================================
    # SLIDE 16: EXPLAINABLE AI (XAI) VIA TREESHAP
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "Explainable AI (XAI) via TreeSHAP Interpretability", "Model Interpretability")
    add_footer(s16, 16)

    add_card(s16, 0.6, 1.35, 5.5, 5.5, "Why Explainability Matters in Operating Systems", [
        "The Black-Box Risk: Schedulers cannot deploy uninterpretable models that make arbitrary allocation decisions.",
        "TreeSHAP Feature Attribution Breakdown:",
        "• I/O Request Rate: 48.5% total model attribution.",
        "    Physical reason: In multi-tier web applications, network packet receipt and database I/O occur before CPU computation occurs!",
        "• Active Task Count: 28.2% attribution.",
        "    Process arrivals directly signal upcoming scheduler runqueue expansion.",
        "• Historical CPU Demand: 15.4% attribution.",
        "    Provides steady-state baseline estimation.",
        "Verification: Confirms the model captures physical workload causality rather than spurious statistical noise!"
    ], COLOR_BLUE)

    fig_shap = 'docs/assets/fig2_shap_feature_importance.png'
    if os.path.exists(fig_shap):
        s16.shapes.add_picture(fig_shap, Inches(6.35), Inches(1.35), width=Inches(6.4))

    # =========================================================================
    # SLIDE 17: ACTUATOR OVERHEAD & REAL-WORLD FEASIBILITY (TC-04)
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "Actuator Overhead & Real-World Feasibility (TC-04)", "Systems Performance")
    add_footer(s17, 17)

    # Overhead Table
    t_shape2 = s17.shapes.add_table(6, 4, Inches(0.6), Inches(1.4), Inches(12.133), Inches(3.0))
    tbl2 = t_shape2.table
    tbl2.columns[0].width = Inches(4.5)
    tbl2.columns[1].width = Inches(2.5)
    tbl2.columns[2].width = Inches(2.5)
    tbl2.columns[3].width = Inches(2.633)

    t2_headers = ["Daemon Phase / Subsystem Call", "Latency (Microseconds)", "Latency (Milliseconds)", "% of 1-sec Control Epoch"]
    for c_idx, h in enumerate(t2_headers):
        cell = tbl2.cell(0, c_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        for p in cell.text_frame.paragraphs:
            p.font.name = "Arial"
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = COLOR_WHITE
            p.alignment = PP_ALIGN.CENTER

    overhead_data = [
        ["XGBoost Model Feature Inference", "82.4 µs", "0.0824 ms", "0.0082%"],
        ["Policy Engine & Headroom Calculation", "18.1 µs", "0.0181 ms", "0.0018%"],
        ["Dry-Run Actuator Simulation Call", "4.2 µs", "0.0042 ms", "0.0004%"],
        ["Real Linux Cgroups v2 Sysfs Write (/sys/.../cpu.max)", "41.6 µs", "0.0416 ms", "0.0042%"],
        ["Total Daemon Actuation Pipeline", "146.3 µs", "0.1463 ms", "0.0146%"]
    ]

    for r_idx, row in enumerate(overhead_data):
        for c_idx, val in enumerate(row):
            cell = tbl2.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            if r_idx == 4:
                cell.fill.fore_color.rgb = RGBColor(230, 255, 235)
            else:
                cell.fill.fore_color.rgb = COLOR_WHITE if r_idx % 2 == 0 else COLOR_LIGHT_BG
            for p in cell.text_frame.paragraphs:
                p.font.name = "Arial"
                p.font.size = Pt(9.5)
                p.font.color.rgb = COLOR_GREEN if r_idx == 4 else COLOR_SLATE
                if r_idx == 4:
                    p.font.bold = True
                p.alignment = PP_ALIGN.CENTER

    add_card(s17, 0.6, 4.7, 12.133, 2.2, "Production Feasibility Conclusion", [
        "Minimal Host Footprint: Total daemon execution consumes < 0.15 ms per 1-second epoch (0.0146% CPU utilization).",
        "Memory Footprint: Daemon Resident Set Size (RSS) remains strictly under 38 MB with loaded XGBoost tree models.",
        "Zero Hot-Path Kernel Impact: CFS runqueue selection in schedule() remains untouched at < 1 µs dispatch latency.",
        "Automated Verification: All 20 rigorous unit tests pass in 5.3s, validating safety bounds and failure modes."
    ], COLOR_GREEN)

    # =========================================================================
    # SLIDE 18: CONCLUSION, FUTURE SCOPE & DEFENSE
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "Conclusion, Future Roadmap & Project Defense", "Summary & Next Steps")
    add_footer(s18, 18)

    add_card(s18, 0.6, 1.35, 5.8, 5.5, "Summary of Achievements", [
        "1. Solved the 'Reactive Latency Tax': Decoupled ML forecasting eliminates CFS quota starvation during bursty workloads.",
        "2. Demonstrated Superior ML Performance: Evaluated 5 models; XGBoost delivers 94.2% directional accuracy with 0.082 ms inference.",
        "3. Real-World Performance Breakthroughs:",
        "    • 99.2% reduction in P95 queuing latency (8.4 ms vs 1,020 ms).",
        "    • 0.0% SLA violations (vs 41.2% in reactive baselines).",
        "    • 87.2% reduction in CFS throttling duration.",
        "4. Guaranteed Safety & Stability: Asymmetric hysteresis prevents 11.3x thrashing; CUSUM detects drift; fail-safe reactive fallbacks.",
        "5. Extremely Lightweight: < 0.15 ms user-space overhead per epoch."
    ], COLOR_BLUE)

    add_card(s18, 6.7, 1.35, 6.0, 5.5, "Future Roadmap & Acknowledgments", [
        "Future Research Roadmap:",
        "• Linux 6.12+ `sched_ext` (eBPF) Integration: Dynamic user-space scheduler plug-ins without kernel recompilation.",
        "• Multi-Resource Co-Optimization: Jointly forecasting and managing memory (cgroup memory.high) and disk I/O (io.weight).",
        "• Online Continual Learning: On-node incremental model updates via low-overhead streaming regression.",
        "Acknowledgments:",
        "Special thanks to our Faculty Mentor Prof. Shubranil Das and the School of Computer Science, UPES Dehradun for their continuous guidance and feedback throughout this project.",
        "Questions & Discussion — Open for Defense!"
    ], COLOR_NAVY)

    # Output paths
    out_docs = 'docs/Adapt_OS_Final_PBL_Presentation.pptx'
    out_desk = '/Users/ayush9085/Desktop/Adapt_OS_Final_PBL_Presentation.pptx'
    prs.save(out_docs)
    prs.save(out_desk)
    print(f"Successfully saved 18-slide Final PBL Presentation to:\n1. {out_docs}\n2. {out_desk}")

if __name__ == '__main__':
    create_presentation()
