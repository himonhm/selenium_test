import re
import time
from selenium.webdriver.common.by import By

from pages import pages
from pages.locators import SbisPageLocators, TensorPageLocators
from misc import file_tools
from .conftest import DOWNLOAD_FOLDER, NEW_REGION_NAME, NEW_REGION_PARTIAL_URL


def test_scenario_1(driver):
    # переходим на https://sbis.ru/ в раздел "Контакты"
    sbis_page = pages.SbisPage(driver=driver, timeout=10)
    sbis_page.open()
    assert "СБИС" in sbis_page.get_title()

    link_contacts = sbis_page.find_element(locator=SbisPageLocators.LINK_CONTACTS)
    link_contacts.click()
    assert "Контакты" in sbis_page.get_title()

    # Находим банер Тензор, кликнуть по нему
    tensor_banner = sbis_page.find_element(locator=SbisPageLocators.TENSOR_BANNER)
    tensor_banner.click()
    sbis_page.switch_to_new_tab()

    # Проверяем, что открылась страница https://tensor.ru/
    tensor_page = pages.TensorPage(driver=driver, timeout=10)
    assert "https://tensor.ru/" == tensor_page.get_url()

    # Проверяем, что есть блок "Сила в людях"
    block_power_of_people = tensor_page.find_element(
        locator=TensorPageLocators.POWER_OF_PEOPLE
    )
    assert block_power_of_people.is_displayed()

    # переходим в подробнее, убеждаемся, что открывается https://tensor.ru/about
    link_details = tensor_page.find_element(
        locator=TensorPageLocators.DETAILS_BLOCK_ABOUT_LINK
    )
    tensor_page.scroll_to_element(element=link_details)
    link_details.click()
    tensor_page.switch_to_new_tab()
    assert "https://tensor.ru/about" == tensor_page.get_url()

    # Находим раздел "Работаем" и проверяем, что у всех фотографий хронологии
    # одинаковые высота (height) и ширина (width)
    block_working = tensor_page.find_element(locator=TensorPageLocators.BLOCK_WORKING)
    photos = tensor_page.find_elements(locator=TensorPageLocators.BLOCK_PHOTOS)

    widths = [int(photo.get_attribute("width")) for photo in photos]
    heights = [int(photo.get_attribute("height")) for photo in photos]

    assert sum(widths) == widths[0] * len(photos) and sum(heights) == heights[0] * len(
        photos
    )


def test_scenario_2(driver):
    # переходим на https://sbis.ru/ в раздел "Контакты"
    sbis_page = pages.SbisPage(driver=driver, timeout=10)
    sbis_page.open()
    assert "СБИС" in sbis_page.get_title()

    link_contacts = sbis_page.find_element(locator=SbisPageLocators.LINK_CONTACTS)
    link_contacts.click()
    assert "Контакты" in sbis_page.get_title()

    # проверяем, что определился регион и есть список партнеров
    block_current_region = sbis_page.find_current_region_element()
    partners_list = sbis_page.find_elements(locator=SbisPageLocators.PARTNERS_LIST)

    assert block_current_region.is_displayed()
    assert len(partners_list) > 0

    # Изменяем регион на Камчатский край и проверяем что подставился выбранный регион
    block_current_region.click()
    sbis_page.find_element(SbisPageLocators.NEW_REGION_LINK, start_delay=2).click()
    new_block_current_region = sbis_page.find_current_region_element(start_delay=3)

    assert NEW_REGION_NAME in new_block_current_region.text

    # проверяем что список партнеров изменился
    new_partner_list = sbis_page.find_elements(locator=SbisPageLocators.PARTNERS_LIST)
    assert partners_list != new_partner_list

    # проверяем url и title
    assert NEW_REGION_PARTIAL_URL in sbis_page.get_url()
    assert NEW_REGION_NAME in sbis_page.get_title()


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
