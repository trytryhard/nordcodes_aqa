"""module for test text search // google.com"""

import allure
import pytest
from playwright.sync_api import Page

from playwright_part.pages.google_page import GooglePage
from playwright_part.test.data.search_cases import SEARCH_CASE


@allure.feature("Google Text")
@allure.story("Textfield")
@allure.title("Тест результата текстового поиска Google ")
@pytest.mark.parametrize("data", SEARCH_CASE.values())
def test_different_language_search(page: Page, data: dict[str, list[str] | str]):
    """Test text search engine
    -----------
    hypothesis:
    user get relevant result from search-page
    """
    google_text = GooglePage(page)
    with allure.step(
        "Open search google page & load & skip cookie-banner (accept all cookies)"
    ):
        google_text.open()

    with allure.step(
        "Search and extract resulted links (could be captcha - solve manually)"
    ):
        links = google_text.search_and_extract_results(data["query"])

    with allure.step("Asser extracted result with expected"):
        # links = google_text.extract_results()
        assert set(links) & set(data["expected"])
