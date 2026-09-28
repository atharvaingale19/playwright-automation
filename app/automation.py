import json
import logging
from datetime import datetime

from playwright.sync_api import sync_playwright

from .config import (
    HEADLESS,
    REPORT_DIR,
    SCREENSHOT_DIR,
    TARGET_URL,
    TIMEOUT,
)
from .report_generator import generate_html_report


logger = logging.getLogger(__name__)


class WebFormAutomation:
    """Automates a web form using Microsoft Playwright."""

    def __init__(self):
        self.results = {
            "status": "Not Started",
            "url": TARGET_URL,
            "steps": [],
            "timestamp": None,
        }

    def _record_step(
        self,
        step: str,
        status: str,
        details: str = "",
    ):
        """Record an automation step."""

        self.results["steps"].append(
            {
                "step": step,
                "status": status,
                "details": details,
            }
        )

        logger.info(
            "%s | %s | %s",
            step,
            status,
            details,
        )

    def run(self) -> dict:
        """Execute the complete browser automation workflow."""

        start_time = datetime.now()

        try:
            with sync_playwright() as playwright:

                logger.info("Launching Chromium.")

                browser = playwright.chromium.launch(
                    headless=HEADLESS
                )

                page = browser.new_page()

                page.set_default_timeout(TIMEOUT)

                try:
                    self._navigate(page)

                    self._fill_form(page)

                    self._submit_form(page)

                    self._validate_result(page)

                    self.results["final_url"] = page.url
                    
                    self._take_screenshot(page)

                    self.results["status"] = "Success"

                except Exception as error:

                    self.results["status"] = "Failed"

                    logger.exception(
                        "Automation failed: %s",
                        error,
                    )

                    try:
                        page.screenshot(
                            path=str(
                                SCREENSHOT_DIR / "failure.png"
                            ),
                            full_page=True,
                        )
                    except Exception:
                        logger.exception(
                            "Failed to capture failure screenshot."
                        )

                    raise

                finally:

                    logger.info("Closing browser.")

                    browser.close()

        except Exception:

            self.results["status"] = "Failed"

        self.results["timestamp"] = start_time.isoformat()

        self._save_report()

        return self.results

    def _navigate(self, page):
        """Navigate to the demo web form and apply custom styling."""

        logger.info("Navigating to demo form.")

        page.goto(
            TARGET_URL,
            wait_until="domcontentloaded",
        )

        # Custom CSS for a cleaner automation demo.
        page.add_style_tag(
            content="""
                body {
                    background:
                        linear-gradient(
                            135deg,
                            #0f172a,
                            #1e293b
                        ) !important;

                    color: #f8fafc !important;

                    font-family:
                        Inter,
                        Arial,
                        sans-serif !important;

                    padding-bottom: 60px !important;
                }

                h1 {
                    color: #38bdf8 !important;

                    font-weight: 800 !important;

                    margin-bottom: 30px !important;
                }

                label {
                    color: #e2e8f0 !important;

                    font-weight: 600 !important;
                }

                input,
                textarea,
                select {
                    background: #1e293b !important;

                    color: #f8fafc !important;

                    border: 1px solid #475569 !important;

                    border-radius: 8px !important;

                    padding: 10px !important;
                }

                input::placeholder,
                textarea::placeholder {
                    color: #94a3b8 !important;
                }

                input:focus,
                textarea:focus,
                select:focus {
                    border-color: #38bdf8 !important;

                    outline: none !important;

                    box-shadow:
                        0 0 0 3px
                        rgba(56, 189, 248, 0.2)
                        !important;
                }

                button {
                    background: #2563eb !important;

                    color: white !important;

                    border: none !important;

                    border-radius: 8px !important;

                    padding: 11px 24px !important;

                    font-weight: 700 !important;

                    cursor: pointer !important;

                    transition:
                        background 0.2s ease,
                        transform 0.2s ease !important;
                }

                button:hover {
                    background: #1d4ed8 !important;

                    transform: translateY(-1px) !important;
                }

                input[type="checkbox"],
                input[type="radio"] {
                    accent-color: #38bdf8 !important;
                }

                .container {
                    max-width: 1100px !important;
                }

                a {
                    color: #38bdf8 !important;
                }

                .form-control:disabled,
                .form-control[readonly] {
                    background: #334155 !important;

                    color: #94a3b8 !important;
                }
            """
        )

        page.get_by_role(
            "heading",
            name="Web form",
        ).wait_for()

        self._record_step(
            "Navigate",
            "Passed",
            "Demo form loaded successfully.",
        )

    def _fill_form(self, page):
        """Fill the available form controls."""

        logger.info("Filling form fields.")

        # Text input
        page.get_by_label(
            "Text input"
        ).fill(
            "Playwright Automation"
        )

        # Password
        page.get_by_label(
            "Password"
        ).fill(
            "Automation123!"
        )

        # Textarea
        page.get_by_label(
            "Textarea"
        ).fill(
            "Automated form submission using Python and Playwright."
        )

        # Dropdown
        page.get_by_label(
            "Dropdown (select)"
        ).select_option(
            "1"
        )

        # Checkbox
        page.get_by_label(
            "Checked checkbox"
        ).check()

        # Radio button
        page.get_by_label(
            "Default radio"
        ).check()

        self._record_step(
            "Fill Form",
            "Passed",
            (
                "Text, password, textarea, dropdown, "
                "checkbox and radio fields populated."
            ),
        )

    def _submit_form(self, page):
        """Submit the completed form."""

        logger.info("Submitting form.")

        page.get_by_role(
            "button",
            name="Submit",
        ).click()

        self._record_step(
            "Submit Form",
            "Passed",
            "Submit button clicked.",
        )

    def _validate_result(self, page):
        """Validate the confirmation returned by the website."""

        logger.info(
            "Validating submission result."
        )

        message = page.locator(
            "#message"
        )

        message.wait_for(
            state="visible"
        )

        result_text = (
            message
            .inner_text()
            .strip()
        )

        if result_text != "Received!":

            raise AssertionError(
                f"Unexpected result: {result_text}"
            )

        self._record_step(
            "Validate Result",
            "Passed",
            (
                "Received expected "
                f"confirmation: {result_text}"
            ),
        )

    def _take_screenshot(self, page):
        """Capture the styled page after successful submission."""

        screenshot_path = (
            SCREENSHOT_DIR
            / "successful_submission.png"
        )

        page.screenshot(
            path=str(screenshot_path),
            full_page=True,
        )

        self._record_step(
            "Screenshot",
            "Passed",
            str(screenshot_path),
        )

    def _save_report(self):
        """Save JSON and HTML execution reports."""

        # JSON report
        report_path = (
            REPORT_DIR
            / "automation_report.json"
        )

        with open(
            report_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self.results,
                file,
                indent=4,
            )

        # HTML report
        html_report_path = (
            REPORT_DIR
            / "report.html"
        )

        screenshot_path = (
            SCREENSHOT_DIR
            / "successful_submission.png"
        )

        generate_html_report(
            self.results,
            screenshot_path,
            html_report_path,
        )

        logger.info(
            "JSON report saved to %s",
            report_path,
        )

        logger.info(
            "HTML report saved to %s",
            html_report_path,
        )