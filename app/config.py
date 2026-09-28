import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


TARGET_URL = "https://www.selenium.dev/selenium/web/web-form.html"

HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

TIMEOUT = int(os.getenv("TIMEOUT", "15000"))

SCREENSHOT_DIR = BASE_DIR / "screenshots"
REPORT_DIR = BASE_DIR / "reports"
LOG_DIR = BASE_DIR / "logs"


for directory in (
    SCREENSHOT_DIR,
    REPORT_DIR,
    LOG_DIR,
):
    directory.mkdir(exist_ok=True)