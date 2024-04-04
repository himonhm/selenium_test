import time
from pages.base_page import BasePage
from pages.locators import SbisPageLocators, TensorPageLocators


class SbisPage(BasePage):
    page_url = "https://sbis.ru/"

    def find_current_region_element(self, start_delay: int = 0):
        time.sleep(start_delay)

        return self.find_element(locator=SbisPageLocators.CURRENT_REGION_ELEMENT)

    def find_contacts_link(self):
        return self.find_element(locator=SbisPageLocators.LINK_CONTACTS)


class SbisContactsPage(BasePage):
    page_url = "https://sbis.ru/contacts/"

    def find_tensor_banner(self):
        return self.find_element(locator=SbisPageLocators.TENSOR_BANNER)


class TensorPage(BasePage):
    page_url = "https://tensor.ru/"

    def find_power_of_people(self):
        return self.find_element(locator=TensorPageLocators.POWER_OF_PEOPLE)

    def find_details_link(self):
        return self.find_element(locator=TensorPageLocators.DETAILS_BLOCK_ABOUT_LINK)


class TensorAboutPage(BasePage):
    page_url = "https://tensor.ru/about"

    def find_working_block(self):
        return self.find_element(locator=TensorPageLocators.BLOCK_WORKING)

    def find_photos_blocks(self):
        return self.find_elements(locator=TensorPageLocators.BLOCK_WORKING_PHOTOS)
