from selenium.webdriver.common.by import By

from tests.conftest import NEW_REGION_NAME


class SbisPageLocators:
    LINK_CONTACTS = (By.LINK_TEXT, "Контакты")
    CURRENT_REGION_ELEMENT = (
        By.XPATH,
        "//div[@class='sbisru-Contacts']//span[contains(@class, 'sbis_ru-Region-Chooser__text')]",
    )
    NEW_REGION_LINK = (By.XPATH, f"//span[@title='{NEW_REGION_NAME}']/span")
    PARTNERS_LIST = (By.XPATH, "//div[contains(@class, 'sbisru-Contacts-List__item')]")
    TENSOR_BANNER = (
        By.XPATH,
        "//a[@href='https://tensor.ru/' and @title='tensor.ru']/img",
    )
    BLOCK_FOOTER = (By.XPATH, "//div[@class='sbisru-Footer__container']")
    BLOCK_FOOTER_DOWNLOAD_LINK = (By.PARTIAL_LINK_TEXT, "Скачать локальные версии")
    DOWNLOAD_SBIS_PLUGIN_LINK = (By.XPATH, "//div[text()='СБИС Плагин']/../../..")
    DOWNLOAD_FILE_LINK = (By.PARTIAL_LINK_TEXT, "Скачать (Exe")


class TensorPageLocators:
    POWER_OF_PEOPLE = (By.XPATH, "//p[text()='Сила в людях']")
    DETAILS_BLOCK_ABOUT_LINK = (
        By.XPATH,
        f"{POWER_OF_PEOPLE[1]}/following::a[@href='/about' and text()='Подробнее']",
    )
    BLOCK_WORKING = (By.XPATH, "//h2[text()='Работаем']")
    BLOCK_WORKING_PHOTOS = (
        By.XPATH,
        f"{BLOCK_WORKING[1]}/parent::*/following-sibling::*//img",
    )
