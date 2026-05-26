"""module for testing positive scenarios"""

import allure
import pytest
from playwright.sync_api import Page

from playwright_part.pages.google_page import GooglePage
from playwright_part.test.data.search_cases import SEARCH_CASE


@allure.feature("Google Text")
@allure.story("Textfield")
@allure.title(
    "Тест результатов поиска после перключения между внутренних вкладок Google"
)
@pytest.mark.parametrize("data", SEARCH_CASE.values())
def test_search_after_switching_tabs(page: Page, data: dict[str, list[str] | str]):
    """scenario: user search info, switching to news,
    check few pages and return to search page
    -----------
    hypothesis:
    after switching sub-pages on google user get relevant result from page
    """

    google_text = GooglePage(page)

    with allure.step("Open search google page. Wait page load & accept cookies"):
        google_text.open()

    with allure.step(
        "Search and extract started res links (could be captcha - solve manually)"
    ):
        start_links = google_text.search_and_extract_results(data["query"])

    with allure.step(
        "Moves to another sub-tabs and if exist pages-entity - go deeper in result"
    ):
        # go to sub_tab, possibly news
        google_text.switch_sub_tab(2)
        google_text.wait_text_field_and_search_res(kind="both")
        google_text.screen("Result of current sub-page")
        # switch page back
        fact_switch = google_text.switch_page()
        if fact_switch:
            google_text.wait_text_field_and_search_res(kind="both")
            google_text.screen("Result of current sub-page after switching page")

    with allure.step("Move back in sub-tabs on the search-page"):
        # go back to search page and assert current links with started links
        google_text.switch_sub_tab()
        google_text.wait_text_field_and_search_res()
        google_text.screen("Result of main-page")

    with allure.step(
        "Final extract result from page and asserting: start & finish & expected results "
    ):

        end_links = google_text.extract_results()
        assert set(start_links) & set(end_links) & set(data["expected"])
