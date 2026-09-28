import json
from pathlib import Path


def generate_html_report(report_data: dict, screenshot_path: Path, output_path: Path) -> None:
    status = report_data.get("status", "Unknown")
    status_class = "success" if status == "Success" else "failed"

    steps_html = ""

    for step in report_data.get("steps", []):
        step_status = step.get("status", "Unknown")
        step_class = "passed" if step_status == "Passed" else "failed"

        steps_html += f"""
        <div class="step">
            <div class="step-icon">{'✓' if step_status == 'Passed' else '✕'}</div>
            <div class="step-info">
                <h3>{step.get('step', 'Unknown')}</h3>
                <p>{step.get('details', '')}</p>
            </div>
            <span class="badge {step_class}">{step_status}</span>
        </div>
        """

    screenshot_uri = screenshot_path.resolve().as_uri()

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Playwright Automation Report</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    font-family: Inter, Arial, sans-serif;
    background: #0b1120;
    color: #e5e7eb;
}}

.container {{
    max-width: 1050px;
    margin: 50px auto;
    padding: 0 24px;
}}

.header {{
    margin-bottom: 30px;
}}

.header h1 {{
    font-size: 32px;
    margin-bottom: 8px;
}}

.header p {{
    color: #94a3b8;
}}

.status {{
    padding: 28px;
    border-radius: 18px;
    margin-bottom: 24px;
    border: 1px solid #1e293b;
    background: #111827;
}}

.status.success {{
    border-left: 5px solid #22c55e;
}}

.status.failed {{
    border-left: 5px solid #ef4444;
}}

.status h2 {{
    margin: 0 0 8px;
}}

.status-text {{
    font-size: 14px;
    color: #94a3b8;
}}

.cards {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin-bottom: 30px;
}}

.card {{
    background: #111827;
    border: 1px solid #1e293b;
    padding: 22px;
    border-radius: 16px;
}}

.card-title {{
    color: #94a3b8;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.card-value {{
    margin-top: 8px;
    font-size: 22px;
    font-weight: 700;
}}

.section {{
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 18px;
    padding: 25px;
    margin-bottom: 25px;
}}

.section h2 {{
    margin-top: 0;
}}

.step {{
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 17px 0;
    border-bottom: 1px solid #1e293b;
}}

.step:last-child {{
    border-bottom: none;
}}

.step-icon {{
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #14532d;
    color: #4ade80;
    font-weight: bold;
}}

.step-info {{
    flex: 1;
}}

.step-info h3 {{
    margin: 0 0 5px;
    font-size: 16px;
}}

.step-info p {{
    margin: 0;
    color: #94a3b8;
    font-size: 13px;
}}

.badge {{
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
}}

.badge.passed {{
    background: #14532d;
    color: #86efac;
}}

.badge.failed {{
    background: #7f1d1d;
    color: #fca5a5;
}}

.screenshot {{
    width: 100%;
    border-radius: 12px;
    border: 1px solid #334155;
    margin-top: 15px;
}}

.footer {{
    text-align: center;
    color: #64748b;
    font-size: 13px;
    padding: 20px;
}}

@media (max-width: 700px) {{
    .cards {{
        grid-template-columns: 1fr;
    }}

    .step {{
        align-items: flex-start;
    }}
}}

</style>
</head>

<body>

<div class="container">

    <div class="header">
        <h1>Web Form Automation</h1>
        <p>Playwright Automation Execution Report</p>
    </div>

    <div class="status {status_class}">
        <h2>{'✓ Automation Successful' if status == 'Success' else '✕ Automation Failed'}</h2>
        <div class="status-text">
            Automated browser workflow completed with status: <strong>{status}</strong>
        </div>
    </div>

    <div class="cards">

        <div class="card">
            <div class="card-title">Status</div>
            <div class="card-value">{status}</div>
        </div>

        <div class="card">
            <div class="card-title">Steps</div>
            <div class="card-value">{len(report_data.get('steps', []))}</div>
        </div>

        <div class="card">
            <div class="card-title">Browser</div>
            <div class="card-value">Chromium</div>
        </div>

    </div>

    <div class="section">

        <h2>Execution Steps</h2>

        {steps_html}

    </div>

    <div class="section">

        <h2>Execution Screenshot</h2>

        <img
            class="screenshot"
            src="{screenshot_uri}"
            alt="Automation execution screenshot"
        >

    </div>

    <div class="section">

        <h2>Target</h2>

        <p>{report_data.get('url', 'Unknown')}</p>

        <p class="status-text">
            Execution timestamp: {report_data.get('timestamp', 'Unknown')}
        </p>

    </div>

    <div class="footer">
        Python · Playwright · Chromium
    </div>

</div>

</body>
</html>
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html)