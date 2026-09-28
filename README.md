# Web Form Automation with Playwright

A modular browser automation project built with **Python** and **Microsoft Playwright**.

The project automates a complete web-form workflow using a public Selenium demonstration page. It launches Chromium, navigates to the target page, interacts with multiple form controls, submits the form, validates the result, captures a screenshot, and generates structured execution reports.

## Features

- Browser automation using Microsoft Playwright
- Chromium browser execution
- Automated form interaction
- Text input handling
- Password field handling
- Textarea interaction
- Dropdown selection
- Checkbox interaction
- Radio button interaction
- Form submission
- Result validation
- Automatic screenshots
- JSON execution reports
- HTML execution reports
- Structured logging
- Exception handling
- Configurable timeout
- Headless/headed execution
- Environment-based configuration
- Automated test coverage with pytest
- Modular project architecture

## Target Website

The automation uses the official Selenium Web Form demonstration page:

https://www.selenium.dev/selenium/web/web-form.html

The page provides multiple form controls specifically suitable for browser automation practice. Selenium's own documentation uses this page for demonstrating browser interaction and form submission. :contentReference[oaicite:1]{index=1}

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Playwright | Browser automation |
| Chromium | Automated browser |
| python-dotenv | Environment configuration |
| pytest | Automated testing |
| JSON | Execution result storage |
| HTML/CSS | Human-readable execution report |

## Project Structure

```text
playwright-automation/
│
├── app/
│   ├── __init__.py
│   ├── automation.py
│   ├── config.py
│   ├── main.py
│   ├── report_generator.py
│   └── utils.py
│
├── tests/
│   └── test_automation.py
│
├── screenshots/
│   └── successful_submission.png
│
├── reports/
│   ├── automation_report.json
│   └── report.html
│
├── logs/
│   └── automation.log
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── documentation.md