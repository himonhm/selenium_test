import time
from page_objects.base_page import BasePage
from selenium.webdriver.common.by import By


class SbisPage(BasePage):
    page_url = "https://sbis.ru/"

    def find_current_region_element(
        self, is_recently_changed: bool = True, wait_time: int = 2
    ):
        # дождемся загрузки если была смена региона
        if is_recently_changed:
            time.sleep(wait_time)

        return self.find_element(
            locator=(
                By.XPATH,
                "//div[@class='sbisru-Contacts']//span[contains(@class, 'sbis_ru-Region-Chooser__text')]",
            )
        )


class TensorPage(BasePage):
    page_url = "https://tensor.ru/"
