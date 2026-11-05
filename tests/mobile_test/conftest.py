import os

import allure
import allure_commons
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv
from selene import browser, support

from litres_test_project.utils import attach_mobile

load_dotenv()

username = os.getenv('USER_NAME')
access_key = os.getenv('ACCESS_KEY')
remote_browser_url = os.getenv('REMOTE_BROWSER_URL', 'http://hub.browserstack.com/wd/hub')
bstack_app_id = os.getenv('BSTACK_APP_ID')


@pytest.fixture(scope='function')
def android_mobile_management():
    options = UiAutomator2Options().load_capabilities({
        "platformName": "android",
        "platformVersion": "12.0",
        "deviceName": "Samsung Galaxy S22 Ultra",
        "app": bstack_app_id,
        "appium:language": "en",
        "appium:locale": "US",
        'bstack:options': {
            "projectName": "Android tests",
            "buildName": "browserstack-litres-build",
            "sessionName": "BStack litres_test",
            "appiumVersion": "2.0.1",
            "userName": username,
            "accessKey": access_key
        }
    })

    with allure.step('setup app session'):
        browser.config.driver = webdriver.Remote(remote_browser_url, options=options)

    browser.config.timeout = 10.0
    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext)

    yield

    attach_mobile.screenshot()
    attach_mobile.page_source_xml()
    session_id = browser.driver.session_id

    with allure.step('tear down app session'):
        browser.quit()

    attach_mobile.bstack_video(session_id)