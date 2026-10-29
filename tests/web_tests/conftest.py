import os
import pytest
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from litres_test_project.utils import attach_web

DEFAULT_BROWSER_VERSION = "152.0"


def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default='155.0'
    )


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def setup_browser(request):
    browser_version = request.config.getoption('--browser_version')
    browser_version = browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)
    load_dotenv()
    login = os.getenv('SELENOID_LOGIN')
    password = os.getenv('SELENOID_PASSWORD')
    selenoid_url = os.getenv('SELENOID_URL')
    driver = webdriver.Remote(command_executor=f"https://{login}:{password}@{selenoid_url}/wd/hub",
                              options=options)
    browser.config.base_url = "https://www.litres.ru/"
    browser.config.driver = driver
    browser.config.driver_options = options

    browser.config.timeout = 4.0
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    yield browser

    attach_web.add_screenshot(browser)
    #attach_web.add_logs(browser)
    attach_web.add_html(browser)
    attach_web.add_video(browser)

    browser.quit()