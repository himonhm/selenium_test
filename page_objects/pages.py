import time
from page_objects.base_page import BasePage
from selenium.webdriver.common.by import By


class SbisPage(BasePage):
    page_url = "https://sbis.ru/"

    def find_current_region_element(self, start_delay: int = 0):
        time.sleep(start_delay)

        return self.find_element(
            locator=(
                By.XPATH,
                "//div[@class='sbisru-Contacts']//span[contains(@class, 'sbis_ru-Region-Chooser__text')]",
            )
        )


class TensorPage(BasePage):
    page_url = "https://tensor.ru/"
