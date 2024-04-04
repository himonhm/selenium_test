import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    page_url: str = None

    def __init__(self, driver: WebDriver, timeout: int = 15):
        self.driver = driver
        self.timeout = timeout
        self.driver.implicitly_wait(timeout)

    def open(self):
        self.driver.get(self.page_url)

    def get_title(self) -> str:
        return self.driver.title

    def get_url(self) -> str:
        return self.driver.current_url

    def find_element(
        self,
        locator: tuple[str, str],
        driver_or_element: WebElement = None,
        start_delay: int = 0,
    ) -> WebElement:
        time.sleep(start_delay)
        driver_or_element = (
            self.driver if driver_or_element is None else driver_or_element
        )
        return WebDriverWait(driver_or_element, self.timeout).until(
            EC.presence_of_element_located(locator),
            f"Can't find element by locator {locator}",
        )

    def find_elements(
        self, locator: tuple[str, str], driver_or_element: WebElement = None
    ) -> list[WebElement]:
        driver_or_element = (
            self.driver if driver_or_element is None else driver_or_element
        )
        return WebDriverWait(driver_or_element, self.timeout).until(
            EC.presence_of_all_elements_located(locator),
            f"Can't find elements by locator {locator}",
        )

    def switch_to_new_tab(self):
        tabs = self.driver.window_handles
        self.driver.switch_to.window(tabs[-1])

    def scroll_to_element(self, element: WebElement):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({ block: 'center' });", element
        )
        time.sleep(1)  # дождемся анимации скролла
        return element

    def should_be_in_title(self, text: str):
        assert text in self.get_title()

    def should_be_in_url(self, text: str):
        assert text in self.get_url()

    def should_be_displayed(self, element: WebElement):
        assert element.is_displayed()

    def should_be_same_width_and_height(self, elements: list[WebElement]):
        widths = [int(elem.get_attribute("width")) for elem in elements]
        heights = [int(elem.get_attribute("height")) for elem in elements]

        assert sum(widths) == widths[0] * len(elements) and sum(heights) == heights[
            0
        ] * len(elements)

    def should_be_not_empty(self, elements: list[WebElement]):
        assert len(elements) > 0
