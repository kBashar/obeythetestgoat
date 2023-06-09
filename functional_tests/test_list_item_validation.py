from unittest import skip
from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):
    def test_can_not_add_empty_list_item(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:invalid")
        )

        # She tries again with some text for the item, which now works
        self.get_item_input_box().send_keys("Buy milk")
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:valid")
        )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: Buy milk")

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys("Make tea")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: Buy milk")
        self.wait_for_row_in_table("2: Make tea")
