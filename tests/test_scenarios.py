import re
import time
from selenium.webdriver.common.by import By

from pages import pages
from pages.locators import SbisPageLocators, TensorPageLocators
from misc import file_tools
from .conftest import DOWNLOAD_FOLDER, NEW_REGION_NAME, NEW_REGION_PARTIAL_URL


def test_scenario_1(driver):
    sbis_page = pages.SbisPage(driver=driver, timeout=10)
    sbis_page.open()
    sbis_page.should_be_in_title("СБИС")

    sbis_page.find_contacts_link().click()

    sbis_contact_page = pages.SbisContactsPage(driver=driver, timeout=10)
    sbis_contact_page.should_be_in_title("Контакты")

    sbis_contact_page.find_tensor_banner().click()

    tensor_page = pages.TensorPage(driver=driver, timeout=10)
    tensor_page.switch_to_new_tab()
    tensor_page.should_be_in_url("https://tensor.ru/")

    power_of_people_block = tensor_page.find_power_of_people()
    tensor_page.should_be_displayed(power_of_people_block)

    details_link = tensor_page.find_details_link()
    tensor_page.scroll_to_element(details_link).click()

    tensor_about_page = pages.TensorAboutPage(driver=driver, timeout=10)
    tensor_about_page.switch_to_new_tab()
    tensor_about_page.should_be_in_url("https://tensor.ru/about")

    working_block = tensor_about_page.find_working_block()
    tensor_about_page.should_be_displayed(working_block)
    tensor_about_page.scroll_to_element(working_block)

    photos_block = tensor_about_page.find_photos_blocks()
    tensor_about_page.should_be_same_width_and_height(photos_block)


def test_scenario_2(driver):
    sbis_page = pages.SbisPage(driver=driver, timeout=10)
    sbis_page.open()
    sbis_page.should_be_in_title("СБИС")

    sbis_page.find_contacts_link().click()

    sbis_contact_page = pages.SbisContactsPage(driver=driver, timeout=10)
    sbis_contact_page.should_be_in_title("Контакты")

    current_region_block = sbis_contact_page.find_current_region_block()
    sbis_contact_page.should_be_displayed(current_region_block)

    partners_list = sbis_contact_page.find_partners_list_blocks()
    sbis_contact_page.should_be_not_empty(partners_list)
    sbis_contact_page.should_able_to_change_current_region()
    sbis_contact_page.should_changed_partner_list(partners_list)
    sbis_contact_page.should_be_in_url(NEW_REGION_PARTIAL_URL)
    sbis_contact_page.should_be_in_title(NEW_REGION_NAME)


def test_scenario_3(driver):
    # переходим на https://sbis.ru/
    sbis_page = pages.SbisPage(driver=driver, timeout=10)
    sbis_page.open()
    assert "СБИС" in sbis_page.get_title()

    # находим footer
    footer = sbis_page.find_element(
        (By.XPATH, "//div[@class='sbisru-Footer__container']")
    )
    sbis_page.scroll_to_element(footer)
    footer.find_element(*SbisPageLocators.BLOCK_FOOTER_DOWNLOAD_LINK).click()

    download_sbis_plugin_link = sbis_page.find_element(
        SbisPageLocators.DOWNLOAD_SBIS_PLUGIN_LINK
    )

    # для того, чтобы клик прошел через робота, нажимаем два раза
    download_sbis_plugin_link.click()
    time.sleep(2)
    download_sbis_plugin_link.click()
    time.sleep(1)  # подождать загрузки js

    download_file_link = sbis_page.find_element(SbisPageLocators.DOWNLOAD_FILE_LINK)
    download_file_link.click()

    file_size_from_page = float(re.findall(r"\d*\.\d+|\d+", download_file_link.text)[0])
    file_size_from_file = file_tools.get_file_size(
        file_tools.get_latest_file_path(DOWNLOAD_FOLDER)
    )

    assert file_size_from_page == round(file_size_from_file, 1)
