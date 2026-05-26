"""module of images google for PAGE OBJECT MODEL"""

import base64
from pathlib import Path

from playwright_part.pages.google_page import GooglePage


class GoogleImg(GooglePage):
    """class for extended google page (images google)"""

    def __init__(self, page):
        super().__init__(page)
        self.image_button = self.page.locator('div[data-is-images-mode="true"]')
        self.drop_area = self.page.locator('div[tabindex="1"]')
        self.lens_area = self.page.locator('div[data-blu="https://lens.google.com"]')

        self.search_img_input_file = self.page.locator('input[type="file"]')

        self.search_img_input_text = self.page.locator('input[text="text"]')
        # self.page.locator('input[text="text"]')

        self.start_page = "https://images.google.com/"

    def click_image_button(self, focus_click_delay: int = 500):
        """
        focus and click on image button with delay
        param: focus_click_delay - milliseconds
        """
        self.image_button.focus()
        self.wait(focus_click_delay)
        self.image_button.click()
        self.screen("Open image window from search-bar")

    def screenshot_to_clipboard(self):
        """moves screenshot into browser's buffer"""
        screenshot = self.page.screenshot()

        # python bytes -> browser readable blob
        self.page.evaluate(
            """
            async (b64) => {
                const blob = await fetch(
                    `data:image/png;base64,${b64}`
                ).then(r => r.blob());

                await navigator.clipboard.write([
                    new ClipboardItem({
                        'image/png': blob
                    })
                ]);
            }
            """,
            base64.b64encode(screenshot).decode(),
        )

    def check_datalense_area(self) -> bool:
        """check visablity of datalens"""
        self.screen("Check datalens area")
        return self.lens_area.nth(1).is_visible()

    # page.locator('span[role="button"]')

    def focus_upload_img_hyperlink(self):
        """check the fact of open window for google lens
        with a fact of visability of self.search_img_field
        and focus on hyperlink"""
        if self.search_img_input_file.is_visible():
            self.search_img_input_file.focus()
            # self.span_button.nth(0).focus()

    def upload_via_hyperlink(self, file_path: Path):
        """upload file via hyperlink"""
        self.search_img_input_file.set_input_files(file_path)
        self.screen("Check fact of file upload")

    def search_image_via_link(
        self, link: str, typing_time: int = 10, search_delay: int = 250
    ):
        """
        param:
            link - link for image
            typing_time - time of inputting link into text field. in seconds
            search_delay - time between input link and pressing enter. in milliseconds
        :return:
        """
        self.search_img_input_text.press_sequentially(link, delay=typing_time)
        self.wait(search_delay)
        self.page.keyboard.press("Enter")
        self.wait(300)
        self.screen("Check search link-input for image-search")

    def clear_img_input_text(self):
        """clear text field for img search by link"""
        self.search_img_input_text.clear()
