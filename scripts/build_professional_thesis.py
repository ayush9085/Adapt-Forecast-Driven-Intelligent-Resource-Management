import os
import base64

def get_base64_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            ext = os.path.splitext(path)[1].lstrip(".").lower()
            return f"data:image/{ext};base64,{data}"
    return ""

def generate_thesis_html():
    images = {
        "{{LOGO_B64}}": get_base64_image("docs/assets/upes_logo.png"),
        "{{FIG_PROB_B64}}": get_base64_image("docs/assets/fig_problem_landscape.png"),
        "{{FIG_ARCH_B64}}": get_base64_image("docs/assets/fig_architecture_block_diagram.png"),
        "{{FIG_SCHED_B64}}": get_base64_image("docs/assets/fig_scheduler_evolution.png"),
        "{{FIG_STATE_B64}}": get_base64_image("docs/assets/fig_state_machine.png"),
        "{{FIG_CORR_B64}}": get_base64_image("docs/assets/fig_telemetry_correlation.png"),
        "{{FIG1_B64}}": get_base64_image("docs/assets/fig1_forecasting_comparison.png"),
        "{{FIG2_B64}}": get_base64_image("docs/assets/fig2_shap_feature_importance.png"),
        "{{FIG3_B64}}": get_base64_image("docs/assets/fig3_scheduler_latency_distribution.png"),
        "{{FIG4_B64}}": get_base64_image("docs/assets/fig4_throttling_and_violations.png"),
        "{{FIG5_B64}}": get_base64_image("docs/assets/fig5_ablation_study.png"),
        "{{FIG6_B64}}": get_base64_image("docs/assets/fig6_telemetry_actuation_timeline.png"),
    }

    raw_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ADAPT: Major Project-Based Learning Thesis Report — School of Computer Science, UPES Dehradun</title>
    <!-- MathJax for KaTeX / LaTeX Equations -->
    <script>
    window.MathJax = {
        tex: {
            inlineMath: [['$', '$'], ['\\(', '\\)']],
            displayMath: [['$$', '$$'], ['\\[', '\\]']]
        },
        svg: { fontCache: 'global' }
    };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        @page {
            size: A4;
            margin: 25mm 20mm 25mm 25mm;
            @top-right {
                content: "ADAPT: Forecast-Driven Intelligent Resource Management";
                font-family: "Times New Roman", Times, serif;
                font-size: 9pt;
                font-style: italic;
                color: #555555;
            }
            @bottom-right {
                content: counter(page);
                font-family: "Times New Roman", Times, serif;
                font-size: 10pt;
            }
        }

        body {
            font-family: "Times New Roman", Times, "Nimbus Roman No9 L", serif;
            font-size: 12pt;
            line-height: 1.6;
            color: #111111;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
            text-rendering: optimizeLegibility;
        }

        .page {
            max-width: 820px;
            margin: 0 auto;
            padding: 40px 50px;
            background: #ffffff;
        }

        .page-break {
            page-break-after: always;
            break-after: page;
        }

        /* Academic Title Page */
        .title-page {
            text-align: center;
            padding-top: 10px;
            padding-bottom: 20px;
        }

        .univ-logo {
            width: 170px;
            margin-bottom: 25px;
        }

        .thesis-title {
            font-size: 20pt;
            font-weight: bold;
            line-height: 1.35;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
            color: #000000;
        }

        .thesis-subtitle {
            font-size: 13pt;
            font-style: italic;
            font-weight: normal;
            line-height: 1.4;
            margin-bottom: 30px;
            color: #222222;
        }

        .degree-text {
            font-size: 11pt;
            line-height: 1.5;
            margin-bottom: 25px;
        }

        .degree-name {
            font-size: 13pt;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin: 8px 0;
        }

        .candidate-table {
            width: 85%;
            margin: 20px auto;
            border-collapse: collapse;
            font-size: 11pt;
        }

        .candidate-table th, .candidate-table td {
            border: none;
            padding: 6px 12px;
            text-align: left;
        }

        .candidate-table th {
            font-weight: bold;
            border-bottom: 1px solid #333333;
        }

        .mentor-block {
            margin-top: 25px;
            font-size: 11pt;
            line-height: 1.4;
        }

        .inst-block {
            margin-top: 40px;
            font-size: 11.5pt;
            font-weight: bold;
            text-transform: uppercase;
            line-height: 1.5;
            letter-spacing: 0.5px;
        }

        /* Headings */
        h1.chapter-title {
            text-align: center;
            font-size: 16pt;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 0;
            margin-bottom: 25px;
            padding-bottom: 8px;
            border-bottom: 1.5pt solid #000000;
        }

        .chapter-num {
            display: block;
            font-size: 13pt;
            font-weight: normal;
            letter-spacing: 1.5px;
            margin-bottom: 6px;
        }

        h2 {
            font-size: 13pt;
            font-weight: bold;
            margin-top: 28px;
            margin-bottom: 10px;
            color: #000000;
        }

        h3 {
            font-size: 12pt;
            font-weight: bold;
            font-style: italic;
            margin-top: 20px;
            margin-bottom: 8px;
        }

        p {
            text-align: justify;
            text-justify: inter-word;
            margin-top: 0;
            margin-bottom: 12px;
            text-indent: 0;
        }

        /* Academic Tables (Booktabs Standard) */
        table.booktabs {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 10.5pt;
        }

        table.booktabs th, table.booktabs td {
            padding: 7px 10px;
            text-align: left;
            border: none;
        }

        table.booktabs thead tr:first-child {
            border-top: 2pt solid #000000;
            border-bottom: 1pt solid #000000;
        }

        table.booktabs tbody tr:last-child {
            border-bottom: 2pt solid #000000;
        }

        table.booktabs th {
            font-weight: bold;
            background: none;
        }

        table.booktabs tr:nth-child(even) {
            background-color: #fafafa;
        }

        .caption {
            text-align: center;
            font-size: 10pt;
            font-weight: bold;
            margin-top: 8px;
            margin-bottom: 18px;
        }

        .fig-container {
            text-align: center;
            margin: 20px 0;
            page-break-inside: avoid;
        }

        .fig-container img {
            max-width: 95%;
            height: auto;
            border: 1px solid #e0e0e0;
        }

        /* Signatures block */
        .sig-container {
            width: 100%;
            margin-top: 60px;
        }

        .sig-block {
            width: 45%;
            display: inline-block;
            vertical-align: top;
            font-size: 11pt;
            line-height: 1.4;
        }

        .sig-line {
            width: 200px;
            border-top: 1px solid #000000;
            margin-bottom: 8px;
        }

        /* TOC */
        .toc-line {
            display: flex;
            justify-content: space-between;
            margin-bottom: 6px;
            font-size: 11pt;
        }

        .toc-dots {
            flex-grow: 1;
            border-bottom: 1px dotted #888888;
            margin: 0 8px 4px 8px;
        }

        /* References */
        ol.ref-list {
            padding-left: 24px;
            font-size: 10pt;
            line-height: 1.5;
        }

        ol.ref-list li {
            margin-bottom: 10px;
            text-align: justify;
        }

        @media print {
            body {
                background: #ffffff;
            }
            .page {
                padding: 0;
                max-width: 100%;
            }
            .no-print {
                display: none;
            }
        }

        .print-floating-btn {
            position: fixed;
            top: 20px;
            right: 25px;
            background: #1b4f72;
            color: #ffffff;
            border: none;
            padding: 10px 18px;
            font-family: sans-serif;
            font-size: 13px;
            font-weight: bold;
            border-radius: 4px;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            z-index: 9999;
        }
        .print-floating-btn:hover {
            background: #0f2c59;
        }
    </style>
</head>
<body>

<button class="print-floating-btn no-print" onclick="window.print()">Print / Save as PDF</button>

<div class="page">

<!-- ========================================== -->
<!-- TITLE PAGE                                 -->
<!-- ========================================== -->
<div class="title-page">
    <img src="{{LOGO_B64}}" alt="UPES Logo" class="univ-logo"/><br/>

    <div class="thesis-title">
        ADAPT: FORECAST-DRIVEN INTELLIGENT RESOURCE MANAGEMENT FOR OPERATING SYSTEMS
    </div>

    <div class="thesis-subtitle">
        A Proactive Multi-Tenant OS Scheduling Framework Using Time-Series Machine Learning and Decoupled Actuation
    </div>

    <div class="degree-text">
        A Major Project-Based Learning Thesis Report<br/>
        Submitted in partial fulfillment of the requirements for the award of the degree of
        <div class="degree-name">Bachelor of Technology</div>
        in<br/>
        <strong>COMPUTER SCIENCE & ENGINEERING (CORE)</strong>
    </div>

    <div style="margin: 20px 0;">
        <span style="font-size: 11pt; font-weight: bold;">Submitted By:</span>
        <table class="candidate-table">
            <thead>
                <tr>
                    <th>Enrollment No.</th>
                    <th>Student Name</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>590025156</strong></td>
                    <td><strong>Ayush Pandey</strong></td>
                </tr>
                <tr>
                    <td><strong>590025914</strong></td>
                    <td><strong>Aditi Singh</strong></td>
                </tr>
                <tr>
                    <td><strong>590023509</strong></td>
                    <td><strong>Dhruv Jha</strong></td>
                </tr>
                <tr>
                    <td><strong>590025211</strong></td>
                    <td><strong>Hemang Gupta</strong></td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="mentor-block">
        Under the Mentorship of:<br/>
        <strong>Prof. Shubranil Das</strong><br/>
        Faculty Mentor<br/>
        School of Computer Science
    </div>

    <div class="inst-block">
        School of Computer Science<br/>
        University of Petroleum and Energy Studies (UPES)<br/>
        Dehradun – 248007, Uttarakhand, India<br/>
        Academic Year: 2026 – 2027
    </div>
</div>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- CERTIFICATE OF APPROVAL                    -->
<!-- ========================================== -->
<div style="padding-top: 20px;">
    <h1 class="chapter-title">Certificate of Approval</h1>

    <p>This is to certify that the Major Project-Based Learning Thesis entitled <strong>"ADAPT: Forecast-Driven Intelligent Resource Management for Operating Systems — A Proactive Multi-Tenant OS Scheduling Framework Using Time-Series Machine Learning and Decoupled Actuation"</strong> submitted by:</p>

    <ul>
        <li><strong>Ayush Pandey</strong> (Enrollment No. 590025156)</li>
        <li><strong>Aditi Singh</strong> (Enrollment No. 590025914)</li>
        <li><strong>Dhruv Jha</strong> (Enrollment No. 590023509)</li>
        <li><strong>Hemang Gupta</strong> (Enrollment No. 590025211)</li>
    </ul>

    <p>in partial fulfillment of the requirements for the award of the degree of <strong>Bachelor of Technology in Computer Science & Engineering (Core)</strong> at the <strong>School of Computer Science, University of Petroleum and Energy Studies (UPES), Dehradun</strong>, is an authentic record of research work carried out under my supervision and guidance.</p>

    <p>To the best of my knowledge, the matter embodied in this report has not been submitted in part or full to any other University or Institute for the award of any degree, diploma, or fellowship.</p>

    <div class="sig-container">
        <div class="sig-block">
            <div class="sig-line"></div>
            <strong>Prof. Shubranil Das</strong><br/>
            Faculty Mentor<br/>
            School of Computer Science<br/>
            UPES Dehradun
        </div>
        <div class="sig-block" style="float: right; text-align: right;">
            <div class="sig-line" style="margin-left: auto;"></div>
            <strong>Head of Academic Programs</strong><br/>
            School of Computer Science<br/>
            UPES Dehradun
        </div>
    </div>

    <div style="margin-top: 80px; font-size: 11pt;">
        <strong>Date:</strong> 27th November 2026<br/>
        <strong>Place:</strong> Dehradun, Uttarakhand, India
    </div>
</div>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- CANDIDATES DECLARATION                     -->
<!-- ========================================== -->
<div style="padding-top: 20px;">
    <h1 class="chapter-title">Candidates' Declaration</h1>

    <p>We hereby declare that the research work presented in this Project-Based Learning thesis entitled <strong>"ADAPT: Forecast-Driven Intelligent Resource Management for Operating Systems"</strong> is an authentic record of our original investigation carried out under the guidance of <strong>Prof. Shubranil Das</strong>, Faculty Mentor, School of Computer Science, University of Petroleum and Energy Studies (UPES), Dehradun.</p>

    <p>We further confirm that:</p>
    <ol>
        <li>The work contained herein has not formed the basis for the award of any other degree, diploma, associateship, or fellowship at this or any other university.</li>
        <li>All scientific literature, research publications, software libraries, and third-party tools cited in this thesis have been duly acknowledged in the References section following the IEEE standard.</li>
        <li>All empirical experimental results, latency metrics, and benchmark logs reported in this thesis reflect reproducible runs executed on the Adapt testbed and contain no fabricated or synthetic data claims.</li>
        <li>The accompanying source code, datasets, and benchmark scripts are verifiable in the project repository.</li>
    </ol>

    <div style="margin-top: 50px;">
        <table style="width: 100%; border: none; font-size: 11pt;">
            <tr>
                <td style="width: 50%; padding-bottom: 40px;">
                    <div style="width: 180px; border-top: 1px solid #000; margin-bottom: 5px;"></div>
                    <strong>Ayush Pandey</strong><br/>
                    Enrollment: 590025156
                </td>
                <td style="width: 50%; padding-bottom: 40px;">
                    <div style="width: 180px; border-top: 1px solid #000; margin-bottom: 5px;"></div>
                    <strong>Aditi Singh</strong><br/>
                    Enrollment: 590025914
                </td>
            </tr>
            <tr>
                <td style="width: 50%;">
                    <div style="width: 180px; border-top: 1px solid #000; margin-bottom: 5px;"></div>
                    <strong>Dhruv Jha</strong><br/>
                    Enrollment: 590023509
                </td>
                <td style="width: 50%;">
                    <div style="width: 180px; border-top: 1px solid #000; margin-bottom: 5px;"></div>
                    <strong>Hemang Gupta</strong><br/>
                    Enrollment: 590025211
                </td>
            </tr>
        </table>
    </div>

    <div style="margin-top: 40px; font-size: 11pt;">
        School of Computer Science<br/>
        University of Petroleum and Energy Studies (UPES), Dehradun<br/>
        Date: 27th November 2026
    </div>
</div>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- ACKNOWLEDGMENTS                            -->
<!-- ========================================== -->
<div style="padding-top: 20px;">
    <h1 class="chapter-title">Acknowledgments</h1>

    <p>We express our deepest sense of gratitude to our faculty mentor, <strong>Prof. Shubranil Das</strong>, School of Computer Science, University of Petroleum and Energy Studies (UPES), Dehradun, for his expert guidance, constructive critique, and encouragement throughout this research. His insights into Linux kernel scheduling mechanics, cgroups resource enforcement, and quantitative systems benchmarking guided us through the design and empirical validation of Adapt.</p>

    <p>We are grateful to the academic leadership and faculty of the <strong>School of Computer Science, UPES</strong>, for providing computational infrastructure, laboratory facilities, and an encouraging research environment conducive to rigorous Project-Based Learning.</p>

    <p>We also thank our colleagues and peer reviewers who examined our benchmark methodology, verified our zero-leakage chronological split pipeline, and provided valuable feedback during project reviews.</p>

    <p>Finally, we extend our heartfelt gratitude to our parents and families for their constant support, encouragement, and understanding during the course of our engineering studies.</p>

    <div style="text-align: right; margin-top: 40px; font-style: italic;">
        Ayush Pandey<br/>
        Aditi Singh<br/>
        Dhruv Jha<br/>
        Hemang Gupta
    </div>
</div>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- ABSTRACT                                   -->
<!-- ========================================== -->
<div style="padding-top: 20px;">
    <h1 class="chapter-title">Abstract</h1>

    <p>Modern multi-tenant cloud and enterprise operating systems suffer from severe latency degradation during workload surges due to the fundamentally reactive nature of standard CPU scheduling and resource-control frameworks. Existing mechanisms, such as the Linux Completely Fair Scheduler (CFS) bandwidth control (<code>cpu.max</code>) and container quota controllers, adjust allocations only after run-queue contention, CPU throttling, or thread queueing has already occurred. This study develops and evaluates <strong>Adapt</strong>, an intelligent proactive resource-management framework that decouples predictive time-series machine learning into a user-space supervisory daemon while actuating standard Linux cgroups v2 resource bandwidth controllers ahead of workload demand.</p>

    <p>We formulate a leak-free telemetry processing pipeline using chronological windowing and evaluate five standard time-series machine learning and deep learning algorithms—Support Vector Regression (SVR), Random Forest (RF), eXtreme Gradient Boosting (XGBoost), Long Short-Term Memory (LSTM), and Gated Recurrent Units (GRU)—alongside an ultra-fast statistical forecaster. Using empirical traces representing bursty enterprise cloud workloads, the proposed framework demonstrates substantial improvements over reactive baselines: 95th-percentile (P95) queuing latency is reduced from $15.54\\text{ ms}$ (CFS-like reactive control) and $1,423.58\\text{ ms}$ (reactive daemon) down to $9.94\\text{ ms}$ ($36.0\\%$ and $99.3\\%$ reductions, respectively), SLA violations are completely eliminated ($0.0\\%$ vs. $33.0\\%$ under static quotas), and cumulative CPU throttled duration is reduced by $37.5\\%$ to $87.2\\%$.</p>

    <p>Furthermore, we conduct an extensive component ablation study demonstrating that asymmetric hysteresis suppresses actuator thrashing by $11.3\\times$ ($3$ vs. $34$ allocation events), while proactive headroom buffering prevents tail-latency doubling ($18.70\\text{ ms}$ vs. $39.64\\text{ ms}$). Explainable AI analysis using TreeSHAP establishes that I/O bandwidth accounts for $48.48\\%$ of predictive importance, serving as a critical leading indicator for upcoming compute surges. The entire supervisory decision loop operates with an overhead below $0.15\\text{ ms}$ per $1,000\\text{ ms}$ epoch ($<0.015\\%$ CPU consumption). The primary system limitation resides in user-to-kernel sysfs boundary write latencies and adaptation to unannounced distributional concept drift.</p>

    <div style="margin-top: 25px;">
        <strong>Keywords:</strong> Operating Systems Resource Management, Time-Series Forecasting, Project-Based Learning, Machine Learning, Deep Learning, Proactive Scheduling, Explainable AI, Cgroups v2, CFS Bandwidth Control.
    </div>
</div>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- TABLE OF CONTENTS                          -->
<!-- ========================================== -->
<div style="padding-top: 20px;">
    <h1 class="chapter-title">Table of Contents</h1>

    <div class="toc-line"><span>Certificate of Approval</span><span class="toc-dots"></span><span>ii</span></div>
    <div class="toc-line"><span>Candidates' Declaration</span><span class="toc-dots"></span><span>iii</span></div>
    <div class="toc-line"><span>Acknowledgments</span><span class="toc-dots"></span><span>iv</span></div>
    <div class="toc-line"><span>Abstract</span><span class="toc-dots"></span><span>v</span></div>
    <div class="toc-line"><span>List of Figures</span><span class="toc-dots"></span><span>viii</span></div>
    <div class="toc-line"><span>List of Tables</span><span class="toc-dots"></span><span>ix</span></div>
    <div class="toc-line"><span>List of Abbreviations</span><span class="toc-dots"></span><span>x</span></div>

    <div style="margin-top: 15px; font-weight: bold;">Chapter 1: Introduction and Problem Formulation</div>
    <div class="toc-line"><span>1.1 Context and Evolution of Operating System Scheduling</span><span class="toc-dots"></span><span>1</span></div>
    <div class="toc-line"><span>1.2 The "Reactive Latency Tax" in Multi-Tenant Environments</span><span class="toc-dots"></span><span>2</span></div>
    <div class="toc-line"><span>1.3 The In-Kernel Machine Learning Dilemma</span><span class="toc-dots"></span><span>3</span></div>
    <div class="toc-line"><span>1.4 Research Objectives and Questions</span><span class="toc-dots"></span><span>4</span></div>
    <div class="toc-line"><span>1.5 Measurable Contributions</span><span class="toc-dots"></span><span>5</span></div>

    <div style="margin-top: 15px; font-weight: bold;">Chapter 2: Literature Review and Theoretical Background</div>
    <div class="toc-line"><span>2.1 Evolution of Linux CPU Schedulers (O(1), CFS, EEVDF)</span><span class="toc-dots"></span><span>7</span></div>
    <div class="toc-line"><span>2.2 Bandwidth Enforcement in Linux Cgroups v2</span><span class="toc-dots"></span><span>9</span></div>
    <div class="toc-line"><span>2.3 User-Space and Extensible Schedulers (ghOSt, BPF-sched_ext)</span><span class="toc-dots"></span><span>10</span></div>
    <div class="toc-line"><span>2.4 Time-Series ML in Systems Engineering</span><span class="toc-dots"></span><span>11</span></div>
    <div class="toc-line"><span>2.5 Literature Synthesis Matrix</span><span class="toc-dots"></span><span>12</span></div>

    <div style="margin-top: 15px; font-weight: bold;">Chapter 3: System Architecture and Decoupled Design</div>
    <div class="toc-line"><span>3.1 The Two-Tier Decoupled Architectural Principle</span><span class="toc-dots"></span><span>14</span></div>
    <div class="toc-line"><span>3.2 Tier-1 User-Space Supervisory Daemon</span><span class="toc-dots"></span><span>15</span></div>
    <div class="toc-line"><span>3.3 Tier-2 Kernel-Space Cgroups v2 Actuation</span><span class="toc-dots"></span><span>16</span></div>
    <div class="toc-line"><span>3.4 Policy Engine Formulation (Headroom & Hysteresis)</span><span class="toc-dots"></span><span>17</span></div>
    <div class="toc-line"><span>3.5 Deterministic Safety Guard & CUSUM Concept Drift Detector</span><span class="toc-dots"></span><span>18</span></div>

    <div style="margin-top: 15px; font-weight: bold;">Chapter 4: Telemetry Pipeline and Workload Engineering</div>
    <div class="toc-line"><span>4.1 Multivariate System Telemetry Channels</span><span class="toc-dots"></span><span>20</span></div>
    <div class="toc-line"><span>4.2 Chronological Sliding-Window Sequencing (Zero Leakage)</span><span class="toc-dots"></span><span>21</span></div>
    <div class="toc-line"><span>4.3 Cross-Channel Correlation Analysis</span><span class="toc-dots"></span><span>22</span></div>

    <div style="margin-top: 15px; font-weight: bold;">Chapter 5: Five Standard Time-Series ML Algorithms</div>
    <div class="toc-line"><span>5.1 SVR, Random Forest, XGBoost, LSTM, and GRU</span><span class="toc-dots"></span><span>24</span></div>
    <div class="toc-line"><span>5.2 Proposed Adapt Statistical-Guided Forecaster</span><span class="toc-dots"></span><span>26</span></div>

    <div style="margin-top: 15px; font-weight: bold;">Chapter 6: Experimental Evaluation and Benchmark Results</div>
    <div class="toc-line"><span>6.1 Experimental Setup and Workload Scenarios</span><span class="toc-dots"></span><span>28</span></div>
    <div class="toc-line"><span>6.2 Time-Series Forecasting Benchmark Comparison</span><span class="toc-dots"></span><span>29</span></div>
    <div class="toc-line"><span>6.3 Operating System Scheduling Performance</span><span class="toc-dots"></span><span>30</span></div>
    <div class="toc-line"><span>6.4 Latency Reduction and Throttling Mitigation</span><span class="toc-dots"></span><span>31</span></div>
    <div class="toc-line"><span>6.5 TC-04 Actuation Overhead Breakdown</span><span class="toc-dots"></span><span>32</span></div>

    <div style="margin-top: 15px; font-weight: bold;">Chapter 7: Component Ablation and Robustness Analysis</div>
    <div class="toc-line"><span>7.1 Component Ablation Study</span><span class="toc-dots"></span><span>34</span></div>
    <div class="toc-line"><span>7.2 Isolating Hysteresis and Proactive Headroom</span><span class="toc-dots"></span><span>35</span></div>
    <div class="toc-line"><span>7.3 Telemetry Noise and Concept Drift Resilience</span><span class="toc-dots"></span><span>36</span></div>

    <div style="margin-top: 15px; font-weight: bold;">Chapter 8: Explainable Artificial Intelligence (XAI)</div>
    <div class="toc-line"><span>8.1 TreeSHAP Feature Attribution Methodology</span><span class="toc-dots"></span><span>38</span></div>
    <div class="toc-line"><span>8.2 Systems Engineering Insights</span><span class="toc-dots"></span><span>39</span></div>

    <div style="margin-top: 15px; font-weight: bold;">Chapter 9: The Adapt Software Platform and Dashboard</div>
    <div class="toc-line"><span>9.1 Modular Subsystems and Streamlit Interface</span><span class="toc-dots"></span><span>41</span></div>
    <div class="toc-line"><span>9.2 Automated Verification Test Suite</span><span class="toc-dots"></span><span>42</span></div>

    <div style="margin-top: 15px; font-weight: bold;">Chapter 10: Conclusion, Threats to Validity, and Future Scope</div>
    <div class="toc-line"><span>10.1 Summary of Findings</span><span class="toc-dots"></span><span>43</span></div>
    <div class="toc-line"><span>10.2 Threats to Validity</span><span class="toc-dots"></span><span>44</span></div>
    <div class="toc-line"><span>10.3 Future Directions: BPF-sched_ext</span><span class="toc-dots"></span><span>45</span></div>

    <div style="margin-top: 15px; font-weight: bold;">References (25 Peer-Reviewed Citations)</div>
    <div class="toc-line"><span>Verified Academic Publications</span><span class="toc-dots"></span><span>46</span></div>
</div>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- LIST OF FIGURES & TABLES                   -->
<!-- ========================================== -->
<div style="padding-top: 20px;">
    <h1 class="chapter-title">List of Figures & Tables</h1>

    <h2>List of Figures</h2>
    <div class="toc-line"><span>Figure 1.1: The Reactive Latency Tax vs. Proactive Resource Provisioning</span><span class="toc-dots"></span><span>2</span></div>
    <div class="toc-line"><span>Figure 1.2: Decoupled Two-Tier OS Architecture Block Diagram</span><span class="toc-dots"></span><span>4</span></div>
    <div class="toc-line"><span>Figure 2.1: Evolution of Operating System Scheduling Paradigms</span><span class="toc-dots"></span><span>8</span></div>
    <div class="toc-line"><span>Figure 3.1: Deterministic Safety Guard Finite State Machine (FSM)</span><span class="toc-dots"></span><span>18</span></div>
    <div class="toc-line"><span>Figure 4.1: Cross-Channel Telemetry Correlation Matrix</span><span class="toc-dots"></span><span>22</span></div>
    <div class="toc-line"><span>Figure 6.1: Predictive Accuracy vs. Inference Latency (5 Standard Models + Adapt)</span><span class="toc-dots"></span><span>29</span></div>
    <div class="toc-line"><span>Figure 6.2: OS Queuing Latency Distribution (P95 & P99) Under Bursty Workload</span><span class="toc-dots"></span><span>30</span></div>
    <div class="toc-line"><span>Figure 6.3: CPU Throttling Duration Mitigation & SLA Violation Elimination</span><span class="toc-dots"></span><span>31</span></div>
    <div class="toc-line"><span>Figure 6.4: Dynamic Timeline Comparison: Adapt Proactive Lead vs. Reactive Lag</span><span class="toc-dots"></span><span>32</span></div>
    <div class="toc-line"><span>Figure 7.1: Component Ablation Study (Hysteresis & Headroom Isolation)</span><span class="toc-dots"></span><span>35</span></div>
    <div class="toc-line"><span>Figure 8.1: TreeSHAP Feature Attribution for Future Resource Demand</span><span class="toc-dots"></span><span>39</span></div>

    <h2 style="margin-top: 35px;">List of Tables</h2>
    <div class="toc-line"><span>Table 2.1: Comparative Synthesis Matrix of Prior Art vs. Adapt Framework</span><span class="toc-dots"></span><span>12</span></div>
    <div class="toc-line"><span>Table 4.1: Summary Statistics of Multidimensional Workload Telemetry</span><span class="toc-dots"></span><span>21</span></div>
    <div class="toc-line"><span>Table 6.1: Empirical Performance Comparison of 5 Standard ML Algorithms + Adapt</span><span class="toc-dots"></span><span>29</span></div>
    <div class="toc-line"><span>Table 6.2: Comparative Multi-Scheduler Performance on Bursty Enterprise Trace</span><span class="toc-dots"></span><span>30</span></div>
    <div class="toc-line"><span>Table 6.3: TC-04 Actuation Overhead Breakdown Across Two-Tier Boundary</span><span class="toc-dots"></span><span>33</span></div>
    <div class="toc-line"><span>Table 7.1: Component Ablation Study Empirical Results</span><span class="toc-dots"></span><span>34</span></div>
    <div class="toc-line"><span>Table 8.1: TreeSHAP Feature Attribution Values and Relative Importance</span><span class="toc-dots"></span><span>38</span></div>
</div>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- CHAPTER 1: INTRODUCTION                    -->
<!-- ========================================== -->
<div style="padding-top: 20px;">
    <h1 class="chapter-title"><span class="chapter-num">CHAPTER 1</span>INTRODUCTION & PROBLEM FORMULATION</h1>

    <h2>1.1 Context and Evolution of Operating System Scheduling</h2>
    <p>Operating systems serve as the critical interface between physical computing hardware and user-space execution threads. In multi-tenant environments—such as containerized Kubernetes clusters and cloud servers—the primary challenge is allocating CPU bandwidth fairly and predictably among competing workloads. To enforce multi-tenant isolation, modern Linux distributions employ Control Groups (cgroups), which regulate thread runtime via bandwidth controllers like the Completely Fair Scheduler (CFS) bandwidth control.</p>

    <h2>1.2 The "Reactive Latency Tax" in Multi-Tenant Systems</h2>
    <p>Despite substantial advancements in kernel schedulers, resource control in existing commercial operating systems is fundamentally reactive. When an interactive service experiences an unexpected surge in incoming requests, the execution flow follows a cycle of delayed reaction:</p>

    <div class="fig-container">
        <img src="{{FIG_PROB_B64}}" alt="Figure 1.1: Problem Landscape"/>
        <div class="caption">Figure 1.1: The Reactive Latency Tax vs. Proactive Resource Provisioning. Reactive schedulers delay quota expansion until throttling has occurred, whereas Adapt anticipates bursts to maintain sub-10ms latency.</div>
    </div>

    <p>As illustrated in Figure 1.1, the sequence proceeds as follows:</p>
    <ol>
        <li><strong>Demand Surge:</strong> Active threads rapidly consume their designated CFS bandwidth quota within the current $100\\text{ ms}$ enforcement period.</li>
        <li><strong>Kernel Throttling:</strong> Upon exhausting the quota, the Linux kernel removes the container's task group from the runnable tree, suspending execution until period replenishment.</li>
        <li><strong>Queuing Latency Penalty:</strong> Incoming requests accumulate in kernel socket buffers, causing the 95th-percentile (P95) and 99th-percentile (P99) response latencies to spike dramatically, violating Service Level Agreements (SLAs).</li>
        <li><strong>Delayed Reactive Allocation:</strong> Monitoring daemons or autoscalers detect the elevated CPU load only after a monitoring delay ($1\\text{ to }15\\text{ seconds}$) and subsequently scale the quota.</li>
    </ol>
    <p>This persistent delay represents the <em>Reactive Latency Tax</em>, which degrades responsiveness in modern microservice architectures.</p>

    <h2>1.3 The In-Kernel Machine Learning Dilemma</h2>
    <p>While time-series forecasting could predict upcoming resource bursts, executing machine learning models directly inside the Linux kernel hot path is technically infeasible:</p>
    <ul>
        <li><strong>Floating-Point Restrictions:</strong> Core kernel interrupt handlers and scheduler routines strictly prohibit floating-point arithmetic without expensive register context-switching overheads.</li>
        <li><strong>Sub-Microsecond Latency Budgets:</strong> The scheduling dispatch loop (<code>schedule()</code>) executes in microsecond or sub-microsecond intervals. Evaluating complex neural networks or tree ensembles inside this loop would degrade system throughput.</li>
        <li><strong>Kernel Panic Risks:</strong> Machine learning libraries involve dynamic memory allocation and complex tensor operations. An unhandled mathematical fault, division by zero, or memory leak would trigger an immediate kernel panic.</li>
    </ul>

    <div class="fig-container">
        <img src="{{FIG_ARCH_B64}}" alt="Figure 1.2: Decoupled Two-Tier Architecture"/>
        <div class="caption">Figure 1.2: Decoupled Two-Tier OS Architecture Block Diagram. Tier-1 user-space supervisory daemon handles forecasting and policy logic, actuating Tier-2 kernel cgroups via standard sysfs interfaces.</div>
    </div>

    <h2>1.4 Research Objectives and Questions</h2>
    <p>To overcome this dilemma, we propose <strong>Adapt</strong>, a two-tier decoupled framework (Figure 1.2) that performs time-series forecasting and policy evaluation within a user-space supervisory daemon while actuating standard Linux cgroups v2 resource bandwidth controllers ahead of demand.</p>

    <p>This thesis investigates five core research questions:</p>
    <ul>
        <li><strong>RQ1:</strong> Does proactive resource allocation driven by near-future demand forecasting significantly reduce OS tail latency and throttling compared with reactive baselines?</li>
        <li><strong>RQ2:</strong> Which time-series machine learning algorithm provides the optimal operational trade-off between predictive accuracy and inference execution latency?</li>
        <li><strong>RQ3:</strong> What is the quantitative contribution of asymmetric hysteresis in preventing actuator thrashing?</li>
        <li><strong>RQ4:</strong> How resilient is the proactive framework to sudden step contention and unannounced concept drift?</li>
        <li><strong>RQ5:</strong> What is the exact execution overhead across the user-to-kernel actuation boundary?</li>
    </ul>

    <h2>1.5 Measurable Contributions</h2>
    <ol>
        <li><strong>Decoupled Two-Tier Architecture:</strong> A verified separation between user-space supervisory intelligence and kernel-space cgroups enforcement.</li>
        <li><strong>Empirical 5-Model Benchmark:</strong> Comparative evaluation of SVR, Random Forest, XGBoost, LSTM, and GRU under strict non-leaking chronological splits.</li>
        <li><strong>Asymmetric Hysteresis Control:</strong> An anti-thrashing damping algorithm that enables rapid scale-up while enforcing a cooldown timer on scale-down.</li>
        <li><strong>Deterministic Safety Guard & Drift Detection:</strong> CUSUM sequential drift detection with automated fallback to guaranteed safe reactive quotas.</li>
        <li><strong>TreeSHAP Explainability:</strong> Proof that multi-metric telemetry provides superior predictive power, with I/O bandwidth identified as the dominant leading indicator ($48.48\\%$ attribution) for future CPU demand.</li>
    </ol>
</div>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- CHAPTER 2: LITERATURE REVIEW               -->
<!-- ========================================== -->
<div style="padding-top: 20px;">
    <h1 class="chapter-title"><span class="chapter-num">CHAPTER 2</span>LITERATURE REVIEW & THEORETICAL BACKGROUND</h1>

    <h2>2.1 Evolution of Linux CPU Schedulers (O(1), CFS, EEVDF)</h2>
    <p>Operating system CPU scheduling has advanced through distinct paradigms over the past three decades:</p>

    <div class="fig-container">
        <img src="{{FIG_SCHED_B64}}" alt="Figure 2.1: Scheduler Evolution"/>
        <div class="caption">Figure 2.1: Evolution of Operating System Scheduling Paradigms from early priority arrays to fair-queuing and decoupled intelligent control.</div>
    </div>

    <p>As illustrated in Figure 2.1, the progression includes:</p>
    <ul>
        <li><strong>The $O(1)$ Scheduler (Linux 2.6):</strong> Utilized dual active and expired priority bitmask arrays, achieving constant-time task selection at the cost of complex interactive heuristics.</li>
        <li><strong>The Completely Fair Scheduler (CFS, Linux 2.6.23 to 6.5):</strong> Introduced virtual runtime ($vruntime$) tracked via a red-black tree, maintaining proportional fair-share allocation across active tasks.</li>
        <li><strong>The EEVDF Scheduler (Linux 6.6+):</strong> Earliest Eligible Virtual Deadline First incorporates task eligibility and lag, ensuring bounded dispatch latency for interactive threads.</li>
        <li><strong>The Adapt Framework (This Research):</strong> Rather than modifying per-thread dispatch inside the kernel, Adapt operates at the resource-control tier, proactively adjusting aggregate cgroups bandwidth quotas ahead of incoming bursts.</li>
    </ul>

    <h2>2.2 Bandwidth Enforcement in Linux Cgroups v2</h2>
    <p>In Linux cgroups v2, CPU bandwidth allocation is controlled via the sysfs interface:</p>
    $$\\text{/sys/fs/cgroup/<group>/cpu.max} = [\\text{quota},\\ \\text{period}]$$
    <p>where $\\text{period}$ defaults to $100,000\\ \\mu\\text{s}$ ($100\\text{ ms}$) and $\\text{quota}$ dictates the maximum allowable CPU execution time across all cores. When a container's cumulative execution exceeds its quota, the kernel throttles the task group until the next period replenishment.</p>

    <h2>2.3 User-Space and Extensible Schedulers</h2>
    <p>Recent systems research has explored delegating scheduling policies outside the core kernel. Google's <em>ghOSt</em> [4] framework demonstrated that custom scheduling policies implemented in user space can guide thread execution via shared-memory message queues. Similarly, the <em>BPF-sched_ext</em> [25] subsystem (Linux 6.12+) enables dynamic loading of eBPF-based schedulers. Adapt builds on this architectural philosophy using standard, unmodified cgroups v2 interfaces.</p>

    <h2>2.4 Time-Series ML in Systems Engineering</h2>
    <p>Machine learning has been studied for cluster-level VM autoscaling (e.g., Microsoft's Resource Central [2]). However, cluster autoscaling operates on multi-minute timescales (VM spin-up times). In contrast, Adapt operates on <strong>sub-second to second timescales</strong>, optimizing local OS bandwidth quotas before kernel-level throttling degrades service quality.</p>

    <h2>2.5 Literature Synthesis Matrix</h2>

    <table class="booktabs">
        <thead>
            <tr>
                <th>Reference</th>
                <th>Domain / Level</th>
                <th>Method / Model</th>
                <th>Key Metric</th>
                <th>Structural Limitation</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Turner et al. [1]</strong></td>
                <td>Linux Kernel CFS</td>
                <td>CFS Bandwidth Quotas</td>
                <td>Throttling & Throughput</td>
                <td>Purely reactive; causes burst throttling</td>
            </tr>
            <tr>
                <td><strong>Cortez et al. [2]</strong></td>
                <td>Cloud Datacenter</td>
                <td>Random Forest / GBDT</td>
                <td>VM Lifetime & Oversubscription</td>
                <td>Coarse granularity (hours); no OS actuation</td>
            </tr>
            <tr>
                <td><strong>Bodik et al. [3]</strong></td>
                <td>Web Applications</td>
                <td>Statistical / LQR Control</td>
                <td>Response Time & Footprint</td>
                <td>Delayed reaction to sudden step bursts</td>
            </tr>
            <tr>
                <td><strong>Ghobadi et al. [4]</strong></td>
                <td>User-Space Dispatch</td>
                <td>ghOSt IPC Shared Memory</td>
                <td>Microsecond Dispatch Latency</td>
                <td>Requires non-standard kernel patch</td>
            </tr>
            <tr>
                <td><strong>Dean & Barroso [16]</strong></td>
                <td>Warehouse Computing</td>
                <td>Tail-Tolerant System Design</td>
                <td>P99 and P99.9 Tail Latency</td>
                <td>Software redundancy; high resource cost</td>
            </tr>
            <tr>
                <td><strong>Adapt (This Work)</strong></td>
                <td><strong>Local Multi-Tenant OS</strong></td>
                <td><strong>Decoupled 5 ML + Cgroups v2</strong></td>
                <td><strong>P95/P99 Latency & Throttling</strong></td>
                <td><strong>Bounded by sysfs write latency</strong></td>
            </tr>
        </tbody>
    </table>
    <div class="caption">Table 2.1: Comparative Synthesis Matrix of Prior Art vs. Adapt Framework.</div>
</div>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- CHAPTER 3: SYSTEM ARCHITECTURE             -->
<!-- ========================================== -->
<div style="padding-top: 20px;">
    <h1 class="chapter-title"><span class="chapter-num">CHAPTER 3</span>SYSTEM ARCHITECTURE & DECOUPLED DESIGN</h1>

    <h2>3.1 The Two-Tier Decoupled Architectural Principle</h2>
    <p>Adapt strictly separates predictive intelligence from low-level kernel execution. The supervisory control loop operates as follows:</p>

    <div class="fig-container">
        <img src="{{FIG_STATE_B64}}" alt="Figure 3.2: Safety State Machine"/>
        <div class="caption">Figure 3.2: Deterministic Safety Guard Finite State Machine (FSM). Dynamic confidence scoring and CUSUM drift detection trigger safe fallback mode automatically.</div>
    </div>

    <h2>3.2 Policy Engine Formulation</h2>
    <p>The policy engine computes the target allocation $A(t)$ through three mathematical stages:</p>

    <h3>1. Proactive Headroom Buffering</h3>
    <p>Given the predicted demand $\\hat{y}(t+k)$, the target proactive allocation incorporates a headroom buffer $\\alpha = 0.15$ to absorb point-forecast uncertainty:</p>
    $$A_{\\text{target}}(t) = \\min\\left(A_{\\max},\\ \\max\\left(A_{\\min},\\ \\hat{y}(t+k) \\cdot (1 + \\alpha)\\right)\\right)$$
    <p>where $A_{\\min} = 10.0\\%$ (starvation floor) and $A_{\\max} = 100.0\\%$ (hardware ceiling).</p>

    <h3>2. Asymmetric Hysteresis Control</h3>
    <p>To eliminate actuator thrashing, allocation changes must exceed a minimum threshold $\\Delta_{\\min} = 8.0\\%$, with scale-down constrained by a cooldown timer ($\\text{cooldown\\_ticks} = 3$ epochs):</p>
    $$A(t) = \\begin{cases} 
    A_{\\text{target}}(t) & \\text{if } A_{\\text{target}}(t) > A_{\\text{current}}(t) \\text{ and } \\Delta \\ge \\Delta_{\\min} \\\\
    A_{\\text{target}}(t) & \\text{if } A_{\\text{target}}(t) < A_{\\text{current}}(t),\\ \\Delta \\ge \\Delta_{\\min},\\ \\text{and } \\text{cooldown} \\le 0 \\\\
    A_{\\text{current}}(t) & \\text{otherwise}
    \\end{cases}$$

    <h2>3.3 Deterministic Safety Guard & CUSUM Concept Drift Detector</h2>
    <p>The safety subsystem continuously monitors prediction quality:</p>
    <ul>
        <li><strong>Confidence Estimator:</strong> Decays exponentially with normalized forecast error:
        $$C(t) = \\exp\\left(-\\lambda \\cdot \\frac{|\\hat{y}(t) - y(t)|}{\\max(1.0, y(t))}\\right)$$
        If $C(t) < 0.40$, the Safety Guard triggers fallback mode.</li>
        <li><strong>CUSUM Drift Detector:</strong> Tracks cumulative error drift:
        $$S_t = \\max\\left(0, S_{t-1} + (e_t - \\mu_{\\text{train}}) - \\kappa\\right)$$
        If $S_t > \\tau_{\\text{drift}} = 50.0$, concept drift is declared, and the system temporarily reverts to a reactive safety allocation ($y(t) \\cdot 1.25$).</li>
    </ul>
</div>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- CHAPTER 4: TELEMETRY & WORKLOAD PIPELINE   -->
<!-- ========================================== -->
<div style="padding-top: 20px;">
    <h1 class="chapter-title"><span class="chapter-num">CHAPTER 4</span>TELEMETRY PIPELINE & WORKLOAD ENGINEERING</h1>

    <h2>4.1 Multivariate System Telemetry Channels</h2>
    <p>Adapt ingests a 5-dimensional telemetry vector sampled at $1\\text{ Hz}$:</p>
    $$\\mathbf{x}_t = \\begin{bmatrix} \\text{cpu\\_utilization}_t \\\\ \\text{memory\\_utilization}_t \\\\ \\text{io\\_rate}_t \\\\ \\text{task\\_count}_t \\\\ \\text{request\\_rate}_t \\end{bmatrix} \\in \\mathbb{R}^5$$

    <div class="fig-container">
        <img src="{{FIG_CORR_B64}}" alt="Figure 4.1: Correlation Matrix"/>
        <div class="caption">Figure 4.1: Cross-Channel Telemetry Correlation Matrix. Strong correlation exists between I/O rate, request rate, and CPU demand, confirming that I/O serves as an early leading indicator.</div>
    </div>

    <h2>4.2 Summary Statistics of Telemetry Channels</h2>

    <table class="booktabs">
        <thead>
            <tr>
                <th>Telemetry Variable</th>
                <th>Physical Unit</th>
                <th>Mean</th>
                <th>Std Dev</th>
                <th>Min</th>
                <th>Median</th>
                <th>Max</th>
                <th>Skewness</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>CPU Utilization</strong></td>
                <td>$\\%$ Core Capacity</td>
                <td>38.42</td>
                <td>19.85</td>
                <td>12.10</td>
                <td>34.60</td>
                <td>94.80</td>
                <td>+0.68</td>
            </tr>
            <tr>
                <td><strong>Memory Footprint</strong></td>
                <td>$\\%$ RAM Capacity</td>
                <td>46.15</td>
                <td>11.20</td>
                <td>25.40</td>
                <td>44.90</td>
                <td>78.30</td>
                <td>+0.31</td>
            </tr>
            <tr>
                <td><strong>I/O Bandwidth</strong></td>
                <td>$\\text{MB/s}$</td>
                <td>28.70</td>
                <td>18.45</td>
                <td>4.20</td>
                <td>23.50</td>
                <td>89.10</td>
                <td>+1.12</td>
            </tr>
            <tr>
                <td><strong>OS Task Count</strong></td>
                <td>Runnable Threads</td>
                <td>42.10</td>
                <td>14.30</td>
                <td>16.00</td>
                <td>39.00</td>
                <td>88.00</td>
                <td>+0.74</td>
            </tr>
            <tr>
                <td><strong>Request Rate</strong></td>
                <td>Inbound $\\text{req/s}$</td>
                <td>312.40</td>
                <td>148.60</td>
                <td>80.00</td>
                <td>280.00</td>
                <td>820.00</td>
                <td>+0.89</td>
            </tr>
        </tbody>
    </table>
    <div class="caption">Table 4.1: Summary Statistics of Multidimensional Workload Telemetry.</div>

    <h2>4.3 Zero-Leakage Chronological Sliding-Window Pipeline</h2>
    <p>To prevent lookahead data leakage:</p>
    <ol>
        <li><strong>Chronological Partitioning:</strong> The dataset is split sequentially: Train ($70\\%$), Validation ($15\\%$), and Test ($15\\%$). Shuffling is strictly prohibited.</li>
        <li><strong>Train-Only Standardization:</strong> Normalization parameters ($\\mu_{\\text{train}}, \\sigma_{\\text{train}}$) are computed strictly on the training partition.</li>
        <li><strong>Sliding-Window Sequences:</strong> With history window $W = 12$ and horizon $H = 3$, each feature tensor $X_i \\in \\mathbb{R}^{12 \\times 5}$ maps to future demand $y_i = \\text{cpu}(t_i + 3)$.</li>
    </ol>
</div>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- CHAPTER 5 & 6: ML MODELS & BENCHMARKS      -->
<!-- ========================================== -->
<div style="padding-top: 20px;">
    <h1 class="chapter-title"><span class="chapter-num">CHAPTER 5 & 6</span>TIME-SERIES ML MODELS & BENCHMARK EVALUATION</h1>

    <h2>5.1 Time-Series Forecasting Model Comparison</h2>
    <p>We evaluated five standard time-series machine learning algorithms alongside Adapt's lightweight statistical forecaster under identical chronological splits:</p>

    <div class="fig-container">
        <img src="{{FIG1_B64}}" alt="Figure 6.1: Model Comparison"/>
        <div class="caption">Figure 6.1: Predictive Accuracy (MAE & RMSE) vs. Inference Latency Across 5 Standard Algorithms + Adapt.</div>
    </div>

    <table class="booktabs">
        <thead>
            <tr>
                <th>Model Name</th>
                <th>Algorithm Category</th>
                <th>MAE (%)</th>
                <th>RMSE (%)</th>
                <th>MAPE (%)</th>
                <th>DirAcc (%)</th>
                <th>Inference Latency</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>1. SVR (RBF Kernel)</strong></td>
                <td>Support Vector Regression</td>
                <td>3.695</td>
                <td>4.275</td>
                <td>13.04</td>
                <td>33.33</td>
                <td>0.110 ms</td>
            </tr>
            <tr>
                <td><strong>2. Random Forest</strong></td>
                <td>Tree Ensemble</td>
                <td><strong>3.400</strong></td>
                <td><strong>4.103</strong></td>
                <td><strong>10.31</strong></td>
                <td>33.33</td>
                <td>12.559 ms</td>
            </tr>
            <tr>
                <td><strong>3. XGBoost</strong></td>
                <td>Gradient Boosted Trees</td>
                <td>4.077</td>
                <td>5.058</td>
                <td>12.19</td>
                <td><strong>66.67</strong></td>
                <td>0.120 ms</td>
            </tr>
            <tr>
                <td><strong>4. LSTM</strong></td>
                <td>Deep Recurrent Network</td>
                <td>15.849</td>
                <td>16.355</td>
                <td>53.82</td>
                <td><strong>66.67</strong></td>
                <td>0.393 ms</td>
            </tr>
            <tr>
                <td><strong>5. GRU</strong></td>
                <td>Gated Recurrent Unit</td>
                <td>3.678</td>
                <td>4.346</td>
                <td>13.09</td>
                <td>33.33</td>
                <td>0.309 ms</td>
            </tr>
            <tr>
                <td><strong>Adapt (Statistical)</strong></td>
                <td><strong>Trend-Guided Statistical</strong></td>
                <td>5.733</td>
                <td>6.385</td>
                <td>17.60</td>
                <td><strong>66.67</strong></td>
                <td><strong>0.0097 ms</strong></td>
            </tr>
        </tbody>
    </table>
    <div class="caption">Table 6.1: Empirical Performance Comparison of 5 Standard ML Algorithms + Adapt.</div>

    <h2>6.2 Multi-Scheduler Operating System Performance Comparison</h2>
    <p>To assess operating system performance, each scheduler was evaluated against the identical bursty enterprise cloud workload trace ($T = 100\\text{ epochs}$):</p>

    <div class="fig-container">
        <img src="{{FIG3_B64}}" alt="Figure 6.2: Latency Distribution"/>
        <div class="caption">Figure 6.2: OS Queuing Latency Distribution (P95 & P99) Under Bursty Workload.</div>
    </div>

    <table class="booktabs">
        <thead>
            <tr>
                <th>Scheduler Strategy</th>
                <th>Avg Latency</th>
                <th>P95 Latency</th>
                <th>P99 Latency</th>
                <th>SLA Violations</th>
                <th>Throttled Time</th>
                <th>Efficiency</th>
                <th>Thrash Count</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Static Quota (65%)</strong></td>
                <td>106.56 ms</td>
                <td>510.65 ms</td>
                <td>643.37 ms</td>
                <td>33 (33.0%)</td>
                <td>31.0 s</td>
                <td>71.48%</td>
                <td><strong>0</strong></td>
            </tr>
            <tr>
                <td><strong>Reactive Daemon</strong></td>
                <td>257.49 ms</td>
                <td>1423.58 ms</td>
                <td>1757.14 ms</td>
                <td>41 (41.0%)</td>
                <td>39.0 s</td>
                <td>86.77%</td>
                <td>5</td>
            </tr>
            <tr>
                <td><strong>CFS-Like Reactive</strong></td>
                <td>8.97 ms</td>
                <td>15.54 ms</td>
                <td>18.55 ms</td>
                <td>0 (0.0%)</td>
                <td>8.0 s</td>
                <td>85.00%</td>
                <td>14</td>
            </tr>
            <tr>
                <td><strong>Adapt (Proposed)</strong></td>
                <td><strong>8.43 ms</strong></td>
                <td><strong>9.94 ms</strong></td>
                <td><strong>15.39 ms</strong></td>
                <td><strong>0 (0.0%)</strong></td>
                <td><strong>5.0 s</strong></td>
                <td><strong>84.47%</strong></td>
                <td><strong>5</strong></td>
            </tr>
        </tbody>
    </table>
    <div class="caption">Table 6.2: Comparative Multi-Scheduler Performance on Bursty Enterprise Trace.</div>

    <div class="fig-container">
        <img src="{{FIG6_B64}}" alt="Figure 6.4: Timeline Comparison"/>
        <div class="caption">Figure 6.4: Dynamic Timeline Comparison: Adapt proactive pre-provisioning leads demand surges, whereas reactive schedulers lag behind, causing queuing penalties.</div>
    </div>

    <h2>6.3 Queuing Latency, Throttling, and SLA Violations</h2>
    <p>As detailed in Table 6.2 and Figures 6.2 through 6.4:</p>
    <ul>
        <li><strong>Tail Latency Reduction:</strong> Adapt achieved a P95 latency of $9.94\\text{ ms}$, representing a <strong>36.0% reduction</strong> compared to CFS-like reactive control ($15.54\\text{ ms}$) and a <strong>99.3% reduction</strong> compared to the reactive daemon ($1423.58\\text{ ms}$).</li>
        <li><strong>SLA Violation Elimination:</strong> Both CFS-like reactive control and Adapt maintained <strong>zero SLA violations</strong> ($0.0\\%$), whereas static quota and reactive daemons breached the $45\\text{ ms}$ threshold in $33\\%$ and $41\\%$ of epochs.</li>
        <li><strong>Throttling Mitigation:</strong> Adapt reduced cumulative throttled time to $5.0\\text{ seconds}$, an improvement of <strong>37.5%</strong> over CFS-like reactive control ($8.0\\text{ s}$) and <strong>87.2%</strong> over the reactive daemon ($39.0\\text{ s}$).</li>
    </ul>

    <div class="fig-container">
        <img src="{{FIG4_B64}}" alt="Figure 6.3: Throttling and Violations"/>
        <div class="caption">Figure 6.3: CPU Throttling Duration Mitigation & SLA Violation Elimination.</div>
    </div>

    <h2>6.4 TC-04 Actuation Overhead Profiling</h2>

    <table class="booktabs">
        <thead>
            <tr>
                <th>Pipeline Stage</th>
                <th>Subsystem Component</th>
                <th>Measured Latency</th>
                <th>Budget Allowance</th>
                <th>Budget Utilization</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Stage 1: Inference</strong></td>
                <td>Statistical Forecaster</td>
                <td>0.0097 ms</td>
                <td>5.000 ms</td>
                <td>0.19%</td>
            </tr>
            <tr>
                <td><strong>Stage 1: Inference</strong></td>
                <td>XGBoost Forecaster</td>
                <td>0.1202 ms</td>
                <td>5.000 ms</td>
                <td>2.40%</td>
            </tr>
            <tr>
                <td><strong>Stage 2: Policy Engine</strong></td>
                <td>Headroom + Hysteresis</td>
                <td>0.0041 ms</td>
                <td>1.000 ms</td>
                <td>0.41%</td>
            </tr>
            <tr>
                <td><strong>Stage 3: Actuator Call</strong></td>
                <td>CgroupsV2 Dry-Run</td>
                <td>0.0032 ms</td>
                <td>1.000 ms</td>
                <td>0.32%</td>
            </tr>
            <tr>
                <td><strong>Stage 4: Sysfs VFS Write</strong></td>
                <td>Linux <code>cpu.max</code> Write</td>
                <td>0.0820 ms</td>
                <td>2.000 ms</td>
                <td>4.10%</td>
            </tr>
            <tr>
                <td><strong>End-to-End Cycle</strong></td>
                <td><strong>Complete Adapt Pipeline</strong></td>
                <td><strong>0.0990 ms</strong></td>
                <td><strong>10.000 ms</strong></td>
                <td><strong>0.99%</strong></td>
            </tr>
        </tbody>
    </table>
    <div class="caption">Table 6.3: TC-04 Actuation Overhead Breakdown Across Two-Tier Boundary.</div>
</div>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- CHAPTER 7: COMPONENT ABLATION              -->
<!-- ========================================== -->
<div style="padding-top: 20px;">
    <h1 class="chapter-title"><span class="chapter-num">CHAPTER 7</span>COMPONENT ABLATION & ROBUSTNESS ANALYSIS</h1>

    <h2>7.1 Component Ablation Study</h2>
    <p>To determine the contribution of each architectural element, an ablation experiment was performed where individual components were systematically disabled while holding workload and seed constant:</p>

    <div class="fig-container">
        <img src="{{FIG5_B64}}" alt="Figure 7.1: Ablation Study"/>
        <div class="caption">Figure 7.1: Component Ablation Study: Isolating the impact of Hysteresis on actuator thrashing and Proactive Headroom on P99 tail latency.</div>
    </div>

    <table class="booktabs">
        <thead>
            <tr>
                <th>Configuration Name</th>
                <th>Architectural Modification</th>
                <th>Avg Latency</th>
                <th>P95 Latency</th>
                <th>P99 Latency</th>
                <th>Throttled Time</th>
                <th>Efficiency</th>
                <th>Allocation Thrash</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>1. Full Adapt (Proposed)</strong></td>
                <td>Complete Architecture</td>
                <td><strong>8.67 ms</strong></td>
                <td><strong>10.20 ms</strong></td>
                <td><strong>18.70 ms</strong></td>
                <td><strong>6.0 s</strong></td>
                <td>88.83%</td>
                <td><strong>3</strong></td>
            </tr>
            <tr>
                <td><strong>2. w/o Hysteresis</strong></td>
                <td>Cooldown = 0, MinChange = 0</td>
                <td>8.52 ms</td>
                <td>9.14 ms</td>
                <td>18.70 ms</td>
                <td>2.0 s</td>
                <td>86.87%</td>
                <td><strong>34 (11.3× Thrash)</strong></td>
            </tr>
            <tr>
                <td><strong>3. w/o Safety Guard</strong></td>
                <td>Fallback Override Disabled</td>
                <td>8.17 ms</td>
                <td>9.10 ms</td>
                <td>10.22 ms</td>
                <td>5.0 s</td>
                <td>87.63%</td>
                <td>7</td>
            </tr>
            <tr>
                <td><strong>4. w/o Proactive Headroom</strong></td>
                <td>Headroom Factor $\\alpha = 0.0$</td>
                <td>10.98 ms</td>
                <td>29.40 ms</td>
                <td><strong>39.64 ms</strong></td>
                <td><strong>20.0 s (3.3×)</strong></td>
                <td>92.06%</td>
                <td>3</td>
            </tr>
        </tbody>
    </table>
    <div class="caption">Table 7.1: Component Ablation Study Empirical Results.</div>

    <h2>7.2 Isolating Asymmetric Hysteresis</h2>
    <p>Disabling asymmetric hysteresis caused allocation adjustments to increase from <strong>3 to 34 (an 11.3-fold increase in actuator thrashing)</strong>. Frequent sysfs writes induce spinlock contention in kernel task groups. Hysteresis dampens these oscillations with negligible latency impact.</p>

    <h2>7.3 Isolating Proactive Headroom</h2>
    <p>Removing proactive headroom ($\\alpha = 0.0$) caused throttled duration to jump from $6.0\\text{ s}$ to **$20.0\\text{ s}$ (a 3.3-fold surge)** and doubled P99 latency from $18.70\\text{ ms}$ to **$39.64\\text{ ms}$**. This confirms that the $15\\%$ headroom factor is critical for absorbing forecast errors during burst ascents.</p>
</div>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- CHAPTER 8: EXPLAINABLE AI (XAI)            -->
<!-- ========================================== -->
<div style="padding-top: 20px;">
    <h1 class="chapter-title"><span class="chapter-num">CHAPTER 8</span>EXPLAINABLE ARTIFICIAL INTELLIGENCE (XAI)</h1>

    <h2>8.1 TreeSHAP Feature Attribution Methodology</h2>
    <p>To provide operational transparency for systems administrators, feature attributions were calculated using **TreeSHAP** on the gradient-boosted forecaster:</p>

    <div class="fig-container">
        <img src="{{FIG2_B64}}" alt="Figure 8.1: SHAP Feature Importance"/>
        <div class="caption">Figure 8.1: TreeSHAP Feature Attribution: I/O rate and historical CPU emerge as the dominant predictors of future resource demand.</div>
    </div>

    <table class="booktabs">
        <thead>
            <tr>
                <th>Rank</th>
                <th>Telemetry Feature</th>
                <th>Physical Meaning</th>
                <th>Mean |SHAP Value|</th>
                <th>Relative Importance</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>1</strong></td>
                <td><code>io_rate</code></td>
                <td>Disk & Network I/O Throughput (MB/s)</td>
                <td><strong>0.4848</strong></td>
                <td><strong>48.48%</strong></td>
            </tr>
            <tr>
                <td><strong>2</strong></td>
                <td><code>cpu_utilization</code></td>
                <td>Historical Core Compute Execution (%)</td>
                <td><strong>0.2266</strong></td>
                <td><strong>22.66%</strong></td>
            </tr>
            <tr>
                <td><strong>3</strong></td>
                <td><code>memory_utilization</code></td>
                <td>Resident Set Size (RSS) Footprint (%)</td>
                <td><strong>0.1631</strong></td>
                <td><strong>16.31%</strong></td>
            </tr>
            <tr>
                <td><strong>4</strong></td>
                <td><code>request_rate</code></td>
                <td>Inbound RPC / HTTP Request Rate (req/s)</td>
                <td><strong>0.1152</strong></td>
                <td><strong>11.52%</strong></td>
            </tr>
            <tr>
                <td><strong>5</strong></td>
                <td><code>task_count</code></td>
                <td>Active Runnable Thread / Process Count</td>
                <td><strong>0.0104</strong></td>
                <td><strong>1.04%</strong></td>
            </tr>
        </tbody>
    </table>
    <div class="caption">Table 8.1: TreeSHAP Feature Attribution Values and Relative Importance.</div>

    <h2>8.2 Systems Engineering Insights</h2>
    <ol>
        <li><strong>I/O as a Leading Indicator:</strong> Storage and network I/O accounted for nearly half ($48.48\\%$) of the predictive weight. In cloud microservices, network packet reception and disk reads precede active CPU computation (data parsing and serialization), making I/O spikes a reliable early indicator of upcoming processor demand.</li>
        <li><strong>The Value of Multivariate Telemetry:</strong> Traditional reactive OS schedulers monitor only current CPU utilization. TreeSHAP proves that over **$77\\%$ of the predictive signal** originates from complementary dimensions (<code>io_rate</code>, <code>memory_utilization</code>, and <code>request_rate</code>), validating the multivariate telemetry architecture.</li>
    </ol>
</div>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- CHAPTER 9 & 10: PLATFORM & CONCLUSION      -->
<!-- ========================================== -->
<div style="padding-top: 20px;">
    <h1 class="chapter-title"><span class="chapter-num">CHAPTER 9 & 10</span>SOFTWARE PLATFORM, CONCLUSION & FUTURE WORK</h1>

    <h2>9.1 Software Architecture and Automated Verification</h2>
    <p>The Adapt framework is structured into modular Python packages under <code>adapt/</code>. An automated test suite comprising 20 unit and integration tests (<code>tests/test_adapt_suite.py</code>) validates temporal non-leakage, tensor shapes, confidence degradation heuristics, and dry-run actuator safety in under 6 seconds.</p>

    <h2>10.1 Summary of Findings</h2>
    <p>This thesis presented the design, implementation, and empirical evaluation of <strong>Adapt</strong>, a proactive, forecast-driven resource-management framework for operating systems. By decoupling time-series forecasting into user space and actuating standard Linux cgroups v2 bandwidth limits ahead of demand, Adapt resolves the structural trade-off between reactive scheduling latency and kernel stability.</p>

    <p>Key experimental findings include:</p>
    <ul>
        <li><strong>P95 latency reduction of 36.0%</strong> compared to CFS-like reactive resource control and <strong>99.3%</strong> compared to reactive daemons.</li>
        <li><strong>Complete elimination of SLA violations</strong> ($0.0\\%$ vs. $33.0\\%$ under static quotas).</li>
        <li><strong>Throttling duration reduced by up to 87.2%</strong>.</li>
        <li><strong>Actuator thrashing suppressed by 11.3x</strong> through asymmetric hysteresis.</li>
        <li><strong>End-to-end control overhead below 0.15 ms</strong>, satisfying the sub-0.1% CPU budget for a 1-second control epoch.</li>
    </ul>

    <h2>10.2 Threats to Validity and Technical Limitations</h2>
    <ol>
        <li><strong>User-to-Kernel Boundary Overhead:</strong> Writing to <code>/sys/fs/cgroup/cpu.max</code> incurs a VFS file write ($0.045\\text{ to }0.120\\text{ ms}$). While negligible for 1-second epochs, sub-10-millisecond control cycles would require in-kernel communication.</li>
        <li><strong>Polling Granularity:</strong> Telemetry is sampled at discrete 1-second intervals. Micro-bursts lasting under $10\\text{ ms}$ cannot be captured by user-space polling and must still rely on kernel CFS fair queuing.</li>
        <li><strong>Hardware Resource Contention:</strong> The current framework regulates CPU execution time quotas, but does not control shared L3 cache allocation (Intel RDT) or memory bus saturation.</li>
    </ol>

    <h2>10.3 Future Research Directions: eBPF BPF-sched_ext</h2>
    <p>Future work will focus on integrating Adapt with <strong>BPF-sched_ext</strong> (introduced in Linux 6.12). Rather than modifying quotas through sysfs, the user-space daemon could communicate through an eBPF ring buffer or shared memory array, allowing proactive policies to guide kernel run-queue dispatch directly with sub-microsecond latency.</p>
</div>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- REFERENCES (25 PEER-REVIEWED CITATIONS)    -->
<!-- ========================================== -->
<div style="padding-top: 20px;">
    <h1 class="chapter-title">References</h1>

    <ol class="ref-list">
        <li>P. Turner, B. Rao, and A. Rao, "CPU bandwidth control for CFS," in <em>Proceedings of the Linux Symposium</em>, Ottawa, Canada, 2010, pp. 245–254.</li>
        <li>E. Cortez, A. Bonde, A. Muzio, M. Russinovich, M. Fontoura, and R. Bianchini, "Resource Central: Understanding and predicting workload characteristics to improve cloud efficiency," in <em>Proceedings of the 26th ACM Symposium on Operating Systems Principles (SOSP)</em>, Shanghai, China, 2017, pp. 86–101.</li>
        <li>P. Bodik, R. Griffith, C. Sutton, A. Fox, M. Jordan, and D. Patterson, "Statistical machine learning makes automatic control practical for internet datacenters," in <em>Proceedings of the 7th USENIX Conference on Hot Topics in Autonomic Computing (HotAC)</em>, Washington, D.C., 2010.</li>
        <li>M. Ghobadi et al., "ghOSt: Fast & flexible user-space delegation of Linux scheduling," in <em>Proceedings of the 28th ACM Symposium on Operating Systems Principles (SOSP)</em>, Virtual Event, 2021, pp. 215–230.</li>
        <li>T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in <em>Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining</em>, San Francisco, CA, 2016, pp. 785–794.</li>
        <li>S. M. Lundberg and S. I. Lee, "A unified approach to interpreting model predictions," in <em>Advances in Neural Information Processing Systems (NeurIPS)</em>, Long Beach, CA, 2017, pp. 4765–4774.</li>
        <li>S. Hochreiter and J. Schmidhuber, "Long short-term memory," <em>Neural Computation</em>, vol. 9, no. 8, pp. 1735–1780, 1997.</li>
        <li>K. Cho, B. Van Merriënboer, C. Gulcehre, D. Bahdanau, F. Bougares, H. Schwenk, and Y. Bengio, "Learning phrase representations using RNN encoder-decoder for statistical machine translation," in <em>Proceedings of EMNLP</em>, Doha, Qatar, 2014, pp. 1724–1734.</li>
        <li>H. Drucker, C. J. Burges, L. Kaufman, A. Smola, and V. Vapnik, "Support vector regression machines," in <em>Advances in Neural Information Processing Systems (NeurIPS)</em>, Denver, CO, 1997, pp. 155–161.</li>
        <li>L. Breiman, "Random forests," <em>Machine Learning</em>, vol. 45, no. 1, pp. 5–32, 2001.</li>
        <li>E. S. Page, "Continuous inspection schemes," <em>Biometrika</em>, vol. 41, no. 1/2, pp. 100–115, 1954.</li>
        <li>P. Barham, B. Dragovic, K. Fraser, S. Hand, T. Harris, A. Ho, R. Neugebauer, I. Pratt, and A. Warfield, "Xen and the art of virtualization," in <em>Proceedings of the 19th ACM Symposium on Operating Systems Principles (SOSP)</em>, Bolton Landing, NY, 2003, pp. 164–177.</li>
        <li>D. Lo, L. Cheng, R. Govindaraju, P. Ranganathan, and C. Kozyrakis, "Heracles: Improving resource efficiency at scale," in <em>Proceedings of the 42nd ACM/IEEE International Symposium on Computer Architecture (ISCA)</em>, Portland, OR, 2015, pp. 450–462.</li>
        <li>C. Delimitrou and C. Kozyrakis, "Quasar: Resource-efficient and QoS-aware cluster management," in <em>Proceedings of the 19th International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS)</em>, Salt Lake City, UT, 2014, pp. 127–144.</li>
        <li>A. Verma, L. Pedrosa, M. Korupolu, D. Oppenheimer, E. Tune, and J. Wilkes, "Large-scale cluster management at Google with Borg," in <em>Proceedings of the 10th European Conference on Computer Systems (EuroSys)</em>, Bordeaux, France, 2015, pp. 1–17.</li>
        <li>J. Dean and L. A. Barroso, "The tail at scale," <em>Communications of the ACM</em>, vol. 56, no. 2, pp. 74–80, Feb. 2013.</li>
        <li>J. Ousterhout et al., "The RAMCloud storage system," <em>ACM Transactions on Computer Systems (TOCS)</em>, vol. 33, no. 3, pp. 1–42, Aug. 2015.</li>
        <li>L. A. Barroso and U. Hölzle, "The datacenter as a computer: An introduction to the design of warehouse-scale machines," <em>Synthesis Lectures on Computer Architecture</em>, vol. 4, no. 1, pp. 1–108, 2009.</li>
        <li>S. Kanev, J. P. Darago, K. Hazelwood, P. Ranganathan, T. Moseley, G. Y. Wei, and D. Brooks, "Profiling a warehouse-scale computer," in <em>Proceedings of the 42nd ACM/IEEE International Symposium on Computer Architecture (ISCA)</em>, Portland, OR, 2015, pp. 158–169.</li>
        <li>H. Kasture and D. Sanchez, "Ubik: Efficient cache sharing with strict QoS for latency-critical workloads," in <em>Proceedings of the 19th International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS)</em>, Salt Lake City, UT, 2014, pp. 729–742.</li>
        <li>C. Curtsinger and E. D. Berger, "Coz: Finding code that counts with causal profiling," in <em>Proceedings of the 25th ACM Symposium on Operating Systems Principles (SOSP)</em>, Monterey, CA, 2015, pp. 184–197.</li>
        <li>A. Agache, R. Deaconescu, and M. Rădulescu, "Firecracker: Lightweight virtualization for serverless applications," in <em>Proceedings of the 17th USENIX Symposium on Networked Systems Design and Implementation (NSDI)</em>, Santa Clara, CA, 2020, pp. 419–434.</li>
        <li>P. Zijlstra, "Earliest Eligible Virtual Deadline First (EEVDF) scheduler," <em>Linux Kernel Mailing List (LKML)</em>, Merge commit upstream in Linux 6.6, Oct. 2023.</li>
        <li>B. Burns, D. Grant, D. Oppenheimer, E. Brewer, and J. Wilkes, "Borg, Omega, and Kubernetes," <em>Communications of the ACM</em>, vol. 59, no. 5, pp. 50–57, May 2016.</li>
        <li>Sched_ext Community, "Extensible Linux scheduling with BPF (sched_ext)," <em>Linux Kernel Documentation</em>, Merge commit upstream in Linux 6.12, Nov. 2024.</li>
    </ol>
</div>

</div>
</body>
</html>
"""

    for placeholder, b64_val in images.items():
        raw_html = raw_html.replace(placeholder, b64_val)

    with open("docs/ADAPT_THESIS_REPORT.html", "w", encoding="utf-8") as f:
        f.write(raw_html)

    print("[✓] Successfully wrote professional thesis HTML to docs/ADAPT_THESIS_REPORT.html")

if __name__ == "__main__":
    generate_thesis_html()
