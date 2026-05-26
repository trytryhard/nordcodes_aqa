# pylint: disable = R0902

"""module of default google for PAGE OBJECT MODEL"""

import allure
from playwright.sync_api import expect

from playwright_part.utils.simplify_query import simpling


class GooglePage:
    """class for google page"""

    def __init__(self, page):
        self.page = page
        self.text_area = self.page.locator('textarea[name="q"]')
        self.result_area = page.locator("#center_col")

        self.result_area_links = page.locator("#center_col a[href]")
        self.image_from_cookie_banner = page.locator('img[alt="Google"]')
        self.span_button = page.locator('span[role="button"]')
        self.start_page = "https://google.com/"

        # 1 - search, 2-6 could be vids, news, goods,
        self.sub_tab_list = page.locator('div[role="listitem"]')

    def screen(self, name: str):
        """screenshot"""
        allure.attach(
            self.page.screenshot(full_page=True),
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )

    def pass_cookie_banner(self):
        """if exists cookie banner - pass it"""
        self.wait(500)
        if self.image_from_cookie_banner:
            (
                self.page.get_by_role("button")
                .nth(self.page.get_by_role("button").count() - 2)
                .click()
            )

    def wait_text_field_and_search_res(
        self, kind: str = "both", timeout_sec: int = 100
    ):
        """
        wait text field for sec of timeout_val
        param:
            timeout - integer amount of Seconds to wait
            type - both:
                    text_field:
                    search_res:

        """
        if kind in ["both", "text_field"]:
            (
                self.page.wait_for_load_state(
                    expect(self.text_area).to_be_visible(timeout=timeout_sec * 1000)
                )
            )

        if kind in ["both", "search_res"]:
            (
                self.page.wait_for_load_state(
                    expect(self.result_area).to_be_visible(timeout=timeout_sec * 1000)
                )
            )

    def open(self):
        """open start_page"""
        self.page.goto(self.start_page)
        self.screen("Passing cookie banner")
        self.pass_cookie_banner()
        self.screen("Passed cookie banner")
        self.wait_text_field_and_search_res(kind="text_field", timeout_sec=10)

    def extract_results(self) -> list[str]:
        """return: extracted links from result area"""
        return self.result_area_links.evaluate_all("(els) => els.map(el => el.href)")

    def input_text_query(self, search_line: str, typing_time: int = 10):
        """input text query into text field"""
        (self.text_area.press_sequentially(search_line, delay=typing_time))
        self.screen(f"Search query:{simpling(search_line)}")

    def get_text_out_of_search_field(self) -> str:
        """get value out of text field"""
        return self.text_area.input_value()

    def find(self, search_line: str, typing_time: int = 10):
        """searching through with text area field
        param:
            search_line - search query
            typing_time - time for typing the query in seconds
        """
        self.input_text_query(search_line, typing_time)
        self.page.keyboard.press("Enter")

    def clear_text_field(self):
        """clear searching text field"""
        self.text_area.clear()

    def wait(self, timeout_msec: int = 500):
        """wait function
        param: timeout_msec - value in milliseconds"""
        self.page.wait_for_timeout(timeout_msec)

    def clipboard_paste_shortcut(self, timeout_msec: int = 500):
        """clipboard shortcut
        param:
            timeout_msec in millisecond for timeout before using shortcut
        """
        self.wait(timeout_msec)
        self.page.keyboard.press("Control+V")
        self.screen("Used past-shortcut")

    def switch_page(self, page_number: int = 2) -> bool:
        """switch pages if possible
        param: page_number - number of page
        start pages 1-10, after 10+ from 7th it go floating +-5 from current page
        """
        if self.page.locator(f'a[aria-label="Page {page_number}"]').is_visible():
            self.page.locator(f'a[aria-label="Page {page_number}"]').click()
            self.screen("Switched page")
            return True
        return False

    def switch_sub_tab(self, page_number: int = 1):
        """
        switch to another subtab in google_page
        0 - ai, 1 - all-search tab, all ohter are not strict
        param: page_number - number of choosing sub_tab
        """
        if self.sub_tab_list.nth(page_number).is_visible():
            self.sub_tab_list.nth(page_number).click()

    def search_and_extract_results(self, query_line: str | None) -> list[str]:
        """search(if needed) and extract combination"""
        if query_line is not None:
            self.find(search_line=query_line)
        self.wait_text_field_and_search_res()
        self.screen("Result of search")
        return self.extract_results()
