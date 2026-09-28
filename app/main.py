import logging

from .automation import WebFormAutomation
from .config import LOG_DIR
from .utils import setup_logging


def main():
    setup_logging(LOG_DIR)

    logger = logging.getLogger(__name__)

    logger.info("Starting Web Form Automation.")

    automation = WebFormAutomation()

    result = automation.run()

    logger.info(
        "Automation completed with status: %s",
        result["status"],
    )

    print("\nAutomation Result")
    print("=================")
    print(f"Status: {result['status']}")
    print(f"Start URL: {result['url']}")
    print(f"Final URL: {result.get('final_url', result['url'])}")
    for step in result["steps"]:
        print(
            f"{step['step']}: {step['status']}"
        )


if __name__ == "__main__":
    main()