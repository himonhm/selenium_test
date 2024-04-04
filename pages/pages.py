import time
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage
from pages.locators import SbisPageLocators, TensorPageLocators
from tests.conftest import NEW_REGION_NAME


class SbisPage(BasePage):
    page_url = "https://sbis.ru/"

    def find_contacts_link(self) -> WebElement:
        return self.find_element(locator=SbisPageLocators.LINK_CONTACTS)


class SbisContactsPage(BasePage):
    page_url = "https://sbis.ru/contacts/"

    def find_current_region_block(self) -> WebElement:
        return self.find_element(locator=SbisPageLocators.CURRENT_REGION_ELEMENT)

    def find_partners_list_blocks(self) -> list[WebElement]:
        return self.find_elements(locator=SbisPageLocators.PARTNERS_LIST)

    def find_tensor_banner(self) -> WebElement:
        return self.find_element(locator=SbisPageLocators.TENSOR_BANNER)

    def should_able_to_change_current_region(self):
        self.find_current_region_block().click()
        self.find_element(SbisPageLocators.NEW_REGION_LINK, start_delay=2).click()
        time.sleep(2)  # дождемся js
        updated_region_block = self.find_current_region_block()
        assert NEW_REGION_NAME in updated_region_block.text

    def should_changed_partner_list(self, old_partners_list: list[WebElement]):
        new_partners_list = self.find_partners_list_blocks()
        assert old_partners_list != new_partners_list


class TensorPage(BasePage):
    page_url = "https://tensor.ru/"

    def find_power_of_people(self) -> WebElement:
        return self.find_element(locator=TensorPageLocators.POWER_OF_PEOPLE)

    def find_details_link(self) -> WebElement:
        return self.find_element(locator=TensorPageLocators.DETAILS_BLOCK_ABOUT_LINK)


class TensorAboutPage(BasePage):
    page_url = "https://tensor.ru/about"

    def find_working_block(self) -> WebElement:
        return self.find_element(locator=TensorPageLocators.BLOCK_WORKING)

    def find_photos_blocks(self) -> list[WebElement]:
        return self.find_elements(locator=TensorPageLocators.BLOCK_WORKING_PHOTOS)
