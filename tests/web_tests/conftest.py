import os

import pytest
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from litres_test_project.data.users import User
from litres_test_project.pages.web_pages.main_page import main_page
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

    browser.config.timeout = 10.0  # логин и поиск на сайте могут занимать больше 4 секунд
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    yield browser

    attach_web.add_screenshot(browser)
    # attach_web.add_logs(browser)
    attach_web.add_html(browser)
    attach_web.add_video(browser)

    browser.quit()


@pytest.fixture(scope='session')
def user():
    name = os.getenv('LITRES_NAME', '')
    email = os.getenv('USER_EMAIL')
    password = os.getenv('USER_PASSWORD')
    assert email and password, "Задайте USER_EMAIL и USER_PASSWORD в .env"
    return User(name=name, email=email, password=password)


@pytest.fixture(scope='function')
def authorized_user(setup_browser, user):
    main_page.open()
    main_page.accept_cookies()
    main_page.filling_authorization_form(user)
    main_page.user_must_be_authorized(user)
    main_page.open()
    return user
