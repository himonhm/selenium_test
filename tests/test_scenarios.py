import re
import time
from selenium.webdriver.common.by import By

from page_objects import pages
from misc import file_tools
from .conftest import DOWNLOAD_FOLDER


def test_scenario_1(driver):
    # переходим на https://sbis.ru/ в раздел "Контакты"
    sbis_page = pages.SbisPage(driver=driver, timeout=10)
    sbis_page.open()
    assert "СБИС" in sbis_page.get_title()

    link_contacts = sbis_page.find_element(locator=(By.LINK_TEXT, "Контакты"))
    link_contacts.click()
    assert "Контакты" in sbis_page.get_title()

    # Находим банер Тензор, кликнуть по нему
    tensor_banner = sbis_page.find_element(
        locator=(By.XPATH, "//a[@href='https://tensor.ru/' and @title='tensor.ru']/img")
    )
    tensor_banner.click()
    sbis_page.switch_to_new_tab()

    # Проверяем, что открылась страница https://tensor.ru/
    tensor_page = pages.TensorPage(driver=driver, timeout=10)
    assert "https://tensor.ru/" == tensor_page.get_url()

    # Проверяем, что есть блок "Сила в людях"
    block_power_of_people = tensor_page.find_element(
        locator=(By.XPATH, "//p[text()='Сила в людях']")
    )
    assert block_power_of_people.is_displayed()

    # переходим в подробнее, убеждаемся, что открывается https://tensor.ru/about
    link_details = block_power_of_people.find_element(
        By.XPATH, "./following::a[@href='/about' and text()='Подробнее']"
    )
    tensor_page.scroll_to_element(element=link_details)
    link_details.click()
    tensor_page.switch_to_new_tab()
    assert "https://tensor.ru/about" == tensor_page.get_url()

    # Находим раздел "Работаем" и проверяем, что у всех фотографий хронологии
    # одинаковые высота (height) и ширина (width)
    block_working = tensor_page.find_element(
        locator=(
            By.XPATH,
            "//h2[text()='Работаем']",
        )
    )
    photos = tensor_page.find_elements(
        locator=(
            By.XPATH,
            "./parent::*/following-sibling::*//img",
        ),
        driver_or_element=block_working,
    )

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

    link_contacts = sbis_page.find_element(locator=(By.LINK_TEXT, "Контакты"))
    link_contacts.click()
    assert "Контакты" in sbis_page.get_title()

    # проверяем, что определился регион и есть список партнеров
    block_current_region = sbis_page.find_current_region_element(
        is_recently_changed=False
    )
    partners_list = sbis_page.find_elements(
        locator=(
            By.XPATH,
            "//div[contains(@class, 'sbisru-Contacts-List__item')]",
        )
    )

    assert block_current_region.is_displayed()
    assert len(partners_list) > 0

    # Изменяем регион на Камчатский край
    block_current_region.click()

    new_region_name = "Камчатский край"
    sbis_page.find_element(
        (By.XPATH, f"//span[@title='{new_region_name}']/span")
    ).click()

    new_block_current_region = sbis_page.find_current_region_element()

    # проверяем что подставился выбранный регион
    assert new_region_name in new_block_current_region.text

    # проверяем что список партнеров изменился
    new_partner_list = sbis_page.find_elements(
        locator=(
            By.XPATH,
            "//div[contains(@class, 'sbisru-Contacts-List__item')]",
        )
    )
    assert partners_list != new_partner_list

    # проверяем url и title
    assert "41-kamchatskij-kraj" in sbis_page.get_url()
    assert new_region_name in sbis_page.get_title()


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
    footer.find_element(By.PARTIAL_LINK_TEXT, "Скачать локальные версии").click()

    download_sbis_plugin_link = sbis_page.find_element(
        (By.XPATH, "//div[text()='СБИС Плагин']/../../..")
    )

    # для того, чтобы клик прошел через робота, нажимаем два раза
    download_sbis_plugin_link.click()
    time.sleep(2)
    download_sbis_plugin_link.click()
    time.sleep(1)  # подождать загрузки js

    download_file_link = sbis_page.find_element((By.PARTIAL_LINK_TEXT, "Скачать (Exe"))
    download_file_link.click()

    file_size_from_page = float(re.findall(r"\d*\.\d+|\d+", download_file_link.text)[0])
    file_size_from_file = file_tools.get_file_size(
        file_tools.get_latest_file_path(DOWNLOAD_FOLDER)
    )

    assert file_size_from_page == round(file_size_from_file, 1)
