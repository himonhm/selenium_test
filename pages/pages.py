import time
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from pages.locators import SbisPageLocators


class SbisPage(BasePage):
    page_url = "https://sbis.ru/"

    def find_current_region_element(self, start_delay: int = 0):
        time.sleep(start_delay)

        return self.find_element(locator=SbisPageLocators.CURRENT_REGION_ELEMENT)


class TensorPage(BasePage):
    page_url = "https://tensor.ru/"
