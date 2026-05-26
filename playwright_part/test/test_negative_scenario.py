"""module for testing negative scenarios"""

from os.path import abspath, dirname
from os.path import join as path_join
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from playwright_part.pages.google_img import GoogleImg
from playwright_part.pages.google_page import GooglePage

TARGET_DIR = Path(path_join(dirname(abspath(__file__)), "asset"))

FINE_EXTENSION = {".jpg", ".png", ".bmp", ".tif", ".webp"}
WRONG_EXTENSION = [
    file_path
    for file_path in TARGET_DIR.rglob("*")
    if file_path.is_file() and file_path.suffix.lower() not in FINE_EXTENSION
]


@allure.feature("Google Image")
@allure.story("Textfield")
@allure.story("Google lens")
@allure.title("Тест неверного ввода ссылки и загрузка файлов неверного расширения")
@pytest.mark.parametrize("file_path", ([WRONG_EXTENSION]))
def test_wrong_img_search(page: Page, file_path: list[Path]):
    """scenario:
    user try to upload files with wrong extension
    and
    user input wrong link-type for link field
    -----------
    hypothesis:
    page is not changing after facing with wrong extension of file or wrong hyperlink
    """
    google_image = GoogleImg(page)

    with allure.step(
        "Open images google page. Wait load and skip cookie-banner "
        "(accept all cookies)"
    ):
        google_image.open()

    with allure.step("Focus on new window for img-interactions"):
        google_image.click_image_button()
        google_image.focus_upload_img_hyperlink()

    for file in file_path:
        with allure.step("Uploading file via hyperlink. Assert current with start url"):
            google_image.upload_via_hyperlink(file)
            assert google_image.start_page == page.url

        with allure.step(
            "Input wrong hyperlinks into textfield. Assert current with start url "
        ):
            google_image.search_image_via_link(str(file.name))
            assert google_image.start_page == page.url
            google_image.clear_img_input_text()


@allure.feature("Google Text")
@allure.story("Textfield")
@allure.title("Тест длины текстового запроса")
def test_extra_large_text_query(page: Page):
    """scenario: user trying to input text-query > 2048 symbols"""

    google_text = GooglePage(page)
    with allure.step(
        "Open search google page. load and skip cookie-banner (accept all cookies)"
    ):
        google_text.open()

    with allure.step("Create and input 3000 symb search query"):
        search_query = "0" * 3000
        google_text.input_text_query(search_query, typing_time=0)

    with allure.step("Asserting length of query in text field"):
        assert (
            len(google_text.get_text_out_of_search_field()) < len(search_query)
            and len(google_text.get_text_out_of_search_field()) == 2048
        )
