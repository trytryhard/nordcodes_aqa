"""
Pytest configuration for Playwright + Allure integration.
Requires pytest-playwright configuration
"""

import shutil
from pathlib import Path

import allure
import pytest

ARTIFACTS_ROOT = Path("artifacts")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """pytest hook that make artifacts for allure and playwright"""
    outcome = yield
    report = outcome.get_result()

    # SCREENSHOT
    if report.when == "call":

        page = item.funcargs.get("page")

        if page:

            allure.attach(
                page.screenshot(full_page=True),
                name="final-screenshot",
                attachment_type=allure.attachment_type.PNG,
            )

    # ARTIFACTS
    elif report.when == "teardown":

        output_path = item.funcargs.get("output_path")

        if not output_path:
            return

        source_dir = Path(output_path)

        # TARGET DIR NAME : test_file_test_function
        test_file = Path(item.location[0]).stem
        test_name = item.name
        target_dir = ARTIFACTS_ROOT / f"{test_file}_{test_name}"

        # очищаем только текущий test artifacts
        if target_dir.exists():
            shutil.rmtree(target_dir)

        target_dir.mkdir(parents=True, exist_ok=True)

        # COPY ARTIFACTS
        for file in source_dir.iterdir():

            if file.is_file():

                shutil.copy2(file, target_dir / file.name)

        # TRACE
        trace_file = target_dir / "trace.zip"
        if trace_file.exists():
            allure.attach.file(
                str(trace_file),
                name="trace",
                attachment_type=allure.attachment_type.ZIP,
            )

        # VIDEO
        for video_file in target_dir.glob("*.webm"):
            allure.attach.file(
                str(video_file),
                name=video_file.name,
                attachment_type=allure.attachment_type.WEBM,
            )

        # SCREENSHOTS
        for screenshot_file in target_dir.glob("*.png"):
            allure.attach.file(
                str(screenshot_file),
                name=screenshot_file.name,
                attachment_type=allure.attachment_type.PNG,
            )
