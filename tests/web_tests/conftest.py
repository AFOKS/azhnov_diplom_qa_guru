import os

import pytest
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.client_config import ClientConfig

from litres_test_project.data.users import User
from litres_test_project.pages.web_pages.main_page import main_page
from litres_test_project.utils import attach_web

DEFAULT_VERSIONS = {'chrome': '156.0', 'firefox': '158.0'}


def get_options(browser_name, headless):
    if browser_name == 'firefox':
        options = FirefoxOptions()
        if headless:
            options.add_argument('-headless')
    else:
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
        if headless:
            options.add_argument('--headless=new')
    return options


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def setup_browser(request):
    browser_name = request.config.getoption('--browser')
    browser_version = (
        request.config.getoption('--browser_version') or DEFAULT_VERSIONS[browser_name]
    )
    headless = request.config.getoption('--headless')

    options = get_options(browser_name, headless)
    options.set_capability('browserName', browser_name)
    options.set_capability('browserVersion', browser_version)
    options.set_capability('selenoid:options', {
        'enableVNC': True,
        'enableVideo': True,
    })

    selenoid_url = f"https://{os.getenv('SELENOID_URL')}/wd/hub"
    client_config = ClientConfig(
        remote_server_addr=selenoid_url,
        username=os.getenv('SELENOID_LOGIN'),
        password=os.getenv('SELENOID_PASSWORD'),
    )
    driver = webdriver.Remote(
        command_executor=selenoid_url,
        options=options,
        client_config=client_config,
    )

    browser.config.base_url = "https://www.litres.ru/"
    browser.config.driver = driver
    browser.config.timeout = 10.0
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    yield browser

    try:
        attach_web.add_screenshot(browser)
        if browser_name == 'chrome':
            attach_web.add_logs(browser)
        attach_web.add_html(browser)
        attach_web.add_video(browser)
    finally:
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
    main_page.user_must_be_logged_in()
    return user