import os
import base64
import re

def get_base64_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            ext = os.path.splitext(path)[1].lstrip(".").lower()
            return f"data:image/{ext};base64,{data}"
    return ""

def main():
    md_path = "docs/ADAPT_THESIS_REPORT.md"
    html_path = "docs/ADAPT_THESIS_REPORT.html"

    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Base64 encode images for 100% self-contained portability
    logo_b64 = get_base64_image("docs/assets/upes_logo.png")
    fig1_b64 = get_base64_image("docs/assets/fig1_forecasting_comparison.png")
    fig2_b64 = get_base64_image("docs/assets/fig2_shap_feature_importance.png")
    fig3_b64 = get_base64_image("docs/assets/fig3_scheduler_latency_distribution.png")
    fig4_b64 = get_base64_image("docs/assets/fig4_throttling_and_violations.png")
    fig5_b64 = get_base64_image("docs/assets/fig5_ablation_study.png")
    fig6_b64 = get_base64_image("docs/assets/fig6_telemetry_actuation_timeline.png")

    # Replace relative asset paths with embedded base64 data URIs
    replacements = {
        'src="assets/upes_logo.png"': f'src="{logo_b64}"',
        'src="assets/fig1_forecasting_comparison.png"': f'src="{fig1_b64}"',
        'src="assets/fig2_shap_feature_importance.png"': f'src="{fig2_b64}"',
        'src="assets/fig3_scheduler_latency_distribution.png"': f'src="{fig3_b64}"',
        'src="assets/fig4_throttling_and_violations.png"': f'src="{fig4_b64}"',
        'src="assets/fig5_ablation_study.png"': f'src="{fig5_b64}"',
        'src="assets/fig6_telemetry_actuation_timeline.png"': f'src="{fig6_b64}"'
    }

    for target, rep in replacements.items():
        if rep:
            md_content = md_content.replace(target, rep)

    # Escape markdown content for embedding into JS template literal
    escaped_md = md_content.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ADAPT: Major Project-Based Learning Thesis Report — UPES Dehradun</title>
    <!-- MathJax for rendering KaTeX / LaTeX math -->
    <script>
    window.MathJax = {{
        tex: {{
            inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
            displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
        }},
        svg: {{ fontCache: 'global' }}
    }};
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <!-- Marked.js for parsing Markdown -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        @page {{
            size: A4;
            margin: 25mm 20mm 25mm 20mm;
            @bottom-right {{
                content: counter(page);
            }}
        }}
        body {{
            font-family: "Georgia", "Cambria", "Times New Roman", serif;
            line-height: 1.65;
            color: #1a1a1a;
            background-color: #fafafa;
            margin: 0;
            padding: 40px 20px;
        }}
        .report-container {{
            max-width: 900px;
            margin: 0 auto;
            background: #ffffff;
            padding: 60px 70px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border-radius: 4px;
        }}
        h1, h2, h3, h4 {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            color: #0f2c59;
            font-weight: 700;
        }}
        h1 {{
            border-bottom: 2px solid #0f2c59;
            padding-bottom: 8px;
            margin-top: 35px;
            font-size: 2rem;
        }}
        h2 {{
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 6px;
            margin-top: 28px;
            font-size: 1.45rem;
            color: #1a365d;
        }}
        h3 {{
            font-size: 1.15rem;
            margin-top: 20px;
            color: #2b6cb0;
        }}
        p, li {{
            font-size: 1.05rem;
            text-align: justify;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 24px 0;
            font-size: 0.95rem;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        th, td {{
            border: 1px solid #cbd5e1;
            padding: 10px 12px;
            text-align: left;
        }}
        th {{
            background-color: #f1f5f9;
            color: #0f2c59;
            font-weight: 600;
        }}
        tr:nth-child(even) {{
            background-color: #f8fafc;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 6px;
            margin: 15px auto;
            display: block;
        }}
        code {{
            background: #f1f5f9;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
            font-size: 0.9em;
            color: #c0392b;
        }}
        pre {{
            background: #0f172a;
            color: #f8fafc;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            font-size: 0.9rem;
        }}
        pre code {{
            background: none;
            color: inherit;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #2b6cb0;
            padding-left: 16px;
            margin: 16px 0;
            color: #4a5568;
            font-style: italic;
            background: #f7fafc;
            padding: 10px 16px;
        }}
        .print-btn {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #0f2c59;
            color: #ffffff;
            border: none;
            padding: 10px 20px;
            font-size: 1rem;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
            transition: all 0.2s ease;
            z-index: 9999;
        }}
        .print-btn:hover {{
            background: #1a365d;
            transform: translateY(-1px);
        }}
        @media print {{
            body {{
                background: #ffffff;
                padding: 0;
            }}
            .report-container {{
                box-shadow: none;
                padding: 0;
                max-width: 100%;
            }}
            .print-btn {{
                display: none;
            }}
            div[style*="page-break-after: always"] {{
                page-break-after: always;
                break-after: page;
            }}
            h1, h2 {{
                page-break-after: avoid;
                break-after: avoid;
            }}
            table, img {{
                page-break-inside: avoid;
                break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <button class="print-btn" onclick="window.print()">🖨️ Print / Save as PDF</button>
    <div class="report-container" id="content"></div>

    <script>
        const rawMarkdown = `{escaped_md}`;
        document.getElementById('content').innerHTML = marked.parse(rawMarkdown);
    </script>
</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"[✓] Standalone interactive HTML report compiled: {html_path}")

if __name__ == "__main__":
    main()
