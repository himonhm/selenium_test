from pages import pages
from .conftest import NEW_REGION_NAME, NEW_REGION_PARTIAL_URL


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
    sbis_page = pages.SbisPage(driver=driver, timeout=10)
    sbis_page.open()
    sbis_page.should_be_in_title("СБИС")

    sbis_page.find_download_local_versions_link().click()

    sbis_download_page = pages.SbisDownloadPage(driver=driver, timeout=10)
    latest_downloaded_file_path = sbis_download_page.should_download_sbis_plugin()
    sbis_download_page.should_same_file_size(latest_downloaded_file_path)
