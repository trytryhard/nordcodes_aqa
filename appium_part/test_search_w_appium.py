"""test android-system of automation of googling"""

from pathlib import Path

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.parametrize("query", ["wikipedia"])
def test_appium(query: str, manual_chromedriver: bool = True):
    """test android-system of automation of googling"""
    # saint options that helped to run test on my smartphone
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "Android Device"
    options.set_capability("appium:appPackage", "com.android.chrome")
    options.set_capability("appium:appActivity", "com.google.android.apps.chrome.Main")
    options.set_capability("appium:ignoreHiddenApiPolicyError", True)
    options.set_capability("appium:noReset", True)
    options.set_capability("appium:fullReset", False)
    options.set_capability("appium:disableAutomaticScreenshots", True)
    options.set_capability("appium:skipDeviceInitialization", True)
    options.set_capability(
        "appium:chromeOptions", {"args": ["--no-first-run", "--disable-fre"]}
    )
    options.set_capability("appium:enforceAppInstall", False)
    options.set_capability("appium:dontStopAppOnReset", True)

    if manual_chromedriver:
        # path to chromedriver for v. 148_0_x
        base_dir = Path(__file__).resolve().parent

        driver_path = base_dir / "chromedriver" / "chromedriver.exe"

        options.set_capability("appium:chromedriverExecutable", str(driver_path))

    driver = webdriver.Remote(command_executor="http://127.0.0.1:4723", options=options)

    # logic starts here
    driver.get("https://www.google.com")

    # searching in native_app-context with XPATH
    search = driver.find_element(
        AppiumBy.XPATH, '//android.widget.EditText[@package="com.android.chrome"]'
    )
    search.click()
    search.send_keys(query)

    # for starting search suggestions
    search.click()

    # get and calc relative position for pick needed search suggestion
    window_rect = driver.get_window_size()
    search_via_keyboard = {
        "x": window_rect["width"] // 2,
        "y": window_rect["height"] // 4,
    }  # {'x': 1080, 'y': 2400}

    # click on search suggestion
    driver.execute_script("mobile: clickGesture", search_via_keyboard)

    # switch context to html
    driver.switch_to.context("WEBVIEW_chrome")

    # locator for result column of google.com
    cent_col = (AppiumBy.XPATH, '//div[@id="center_col"]')

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located(cent_col))

    # locator for all links on the page
    link_locator = (AppiumBy.XPATH, '//a[@href!=""]')  # and @data-ved

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located(link_locator))

    links = driver.find_elements(*link_locator)

    # filters all links from page to really needed one
    filtered_links = []
    for link in links:
        try:
            if link.get_attribute("href")[:8] == r"https://":
                link.get_attribute("data-ved")
                link.get_attribute("ping")
                filtered_links.append(link.get_attribute("href"))
        except Exception:  # pylint: disable=W0718
            continue

    # if real one links exist on result page - test is passed
    assert set(filtered_links)
