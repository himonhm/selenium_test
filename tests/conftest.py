import pytest
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


DOWNLOAD_FOLDER = "C:\\test_downloads"


@pytest.fixture(scope="function")
def driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "--allow-running-insecure-content"
    )  # Allow insecure content
    chrome_options.add_argument(
        "--unsafely-treat-insecure-origin-as-secure=http://example.com"
    )  # Replace example.com with your site's domain
    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": DOWNLOAD_FOLDER,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=chrome_options
    )
    yield driver
    driver.close()
    driver.quit()
