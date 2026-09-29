from pathlib import Path
import json

import streamlit as st

from app.automation import WebFormAutomation
from app.config import (
    HEADLESS,
    TARGET_URL,
    REPORT_DIR,
    SCREENSHOT_DIR,
)


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Playwright Automation",
    page_icon="🎭",
    layout="wide",
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "results" not in st.session_state:
    st.session_state.results = None


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

st.sidebar.title("🎭 Playwright Automation")

st.sidebar.markdown(
    "### Automation Configuration"
)

st.sidebar.write(
    f"**Browser:** Chromium"
)

st.sidebar.write(
    f"**Mode:** {'Headless' if HEADLESS else 'Visible'}"
)

st.sidebar.write(
    f"**Timeout:** configured in `.env`"
)

st.sidebar.divider()

st.sidebar.caption(
    "Browser automation powered by Python and Microsoft Playwright."
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("🎭 Web Form Automation")

st.markdown(
    """
    Automated browser workflow using **Python + Microsoft Playwright**.

    The application navigates to a web form, fills multiple controls,
    submits the form, validates the response, captures a screenshot,
    and generates execution reports.
    """
)

st.info(f"Target URL: {TARGET_URL}")


# ---------------------------------------------------------
# Run automation
# ---------------------------------------------------------

st.subheader("Run Automation")

if st.button(
    "▶ Run Playwright Automation",
    type="primary",
    width="stretch",
):

    with st.spinner(
        "Launching Chromium and running automation..."
    ):

        automation = WebFormAutomation()
        results = automation.run()

        st.session_state.results = results


# ---------------------------------------------------------
# Results
# ---------------------------------------------------------

results = st.session_state.results

if results is not None:

    st.divider()

    st.subheader("Execution Results")

    status = results.get("status", "Unknown")

    if status == "Success":
        st.success("Automation completed successfully.")
    else:
        st.error("Automation failed.")

    # -----------------------------------------------------
    # Summary metrics
    # -----------------------------------------------------

    steps = results.get("steps", [])

    passed_steps = sum(
        1
        for step in steps
        if step.get("status") == "Passed"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Status",
            status,
        )

    with col2:
        st.metric(
            "Steps Passed",
            f"{passed_steps}/{len(steps)}",
        )

    with col3:
        st.metric(
            "Execution Time",
            results.get("timestamp", "N/A"),
        )

    # -----------------------------------------------------
    # Step-by-step results
    # -----------------------------------------------------

    st.subheader("Automation Steps")

    for step in steps:

        step_name = step.get("step", "Unknown")
        step_status = step.get("status", "Unknown")
        details = step.get("details", "")

        if step_status == "Passed":

            st.success(
                f"✓ {step_name}  |  {details}"
            )

        else:

            st.error(
                f"✗ {step_name}  |  {details}"
            )

    # -----------------------------------------------------
    # Final URL
    # -----------------------------------------------------

    if results.get("final_url"):

        st.subheader("Final URL")

        st.code(
            results["final_url"],
            language="text",
        )

    # -----------------------------------------------------
    # Screenshot
    # -----------------------------------------------------

    screenshot_path = (
        SCREENSHOT_DIR / "successful_submission.png"
    )

    if screenshot_path.exists():

        st.subheader("Automation Screenshot")

        st.image(
            str(screenshot_path),
            caption="Screenshot captured after successful submission.",
            width="stretch",
        )

        st.download_button(
            label="⬇️ Download Screenshot",
            data=screenshot_path.read_bytes(),
            file_name="successful_submission.png",
            mime="image/png",
            width="stretch",
            on_click="ignore",
        )

    # -----------------------------------------------------
    # Reports
    # -----------------------------------------------------

    st.subheader("Execution Reports")

    json_report = (
        REPORT_DIR / "automation_report.json"
    )

    html_report = (
        REPORT_DIR / "report.html"
    )

    report_col1, report_col2 = st.columns(2)

    with report_col1:

        if json_report.exists():

            st.download_button(
                label="⬇️ Download JSON Report",
                data=json_report.read_bytes(),
                file_name="automation_report.json",
                mime="application/json",
                width="stretch",
                on_click="ignore",
            )

    with report_col2:

        if html_report.exists():

            st.download_button(
                label="⬇️ Download HTML Report",
                data=html_report.read_bytes(),
                file_name="report.html",
                mime="text/html",
                width="stretch",
                on_click="ignore",
            )

    # -----------------------------------------------------
    # Raw execution data
    # -----------------------------------------------------

    with st.expander("View Raw Execution Data"):

        st.json(results)