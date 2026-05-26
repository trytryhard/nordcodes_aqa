"""module for test img search // images.google.com"""

import allure
from playwright.sync_api import Page

from playwright_part.pages.google_img import GoogleImg


@allure.feature("Google Image")
@allure.story("Google Lens")
@allure.title("Тест поиска по скриношту")
def test_image_search(page: Page):
    """test function for pasting image from clipboard into images.google with open google search
    -----------
    hypothesis: search result always have
    """
    google_image = GoogleImg(page)

    with allure.step(
        "Open images google page; "
        "Wait page load and skip cookie-banner (accept all cookies)"
    ):
        google_image.open()

    with allure.step("Create screenshot, make it readable for browser and input it"):
        google_image.screenshot_to_clipboard()
        google_image.click_image_button()
        google_image.clipboard_paste_shortcut()

    with allure.step("Wait for results (could be captcha - solve manually)"):
        # could be captcha : CAPTCHA SOLVE MANUALLY
        google_image.wait_text_field_and_search_res()

    with allure.step("Checking existence of datalens area"):
        assert google_image.check_datalense_area()
