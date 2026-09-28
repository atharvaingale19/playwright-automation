from app.automation import WebFormAutomation


def test_automation_workflow():
    automation = WebFormAutomation()

    result = automation.run()

    assert result["status"] == "Success"

    steps = {
        step["step"]: step["status"]
        for step in result["steps"]
    }

    assert steps["Navigate"] == "Passed"
    assert steps["Fill Form"] == "Passed"
    assert steps["Submit Form"] == "Passed"
    assert steps["Validate Result"] == "Passed"
    assert steps["Screenshot"] == "Passed"