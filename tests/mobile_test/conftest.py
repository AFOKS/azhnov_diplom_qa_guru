import allure
import allure_commons
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selene import browser, support

from litres_test_project.config import CONTEXT, load_config
from litres_test_project.utils import attach_mobile


def _bstack_options(config):
    return UiAutomator2Options().load_capabilities({
        'platformName': 'android',
        'platformVersion': config.platform_version,
        'deviceName': config.device_name,
        'app': config.bstack_app_id,
        'appium:language': 'en',
        'appium:locale': 'US',
        'bstack:options': {
            'projectName': 'Android tests',
            'buildName': 'browserstack-litres-build',
            'sessionName': 'BStack litres_test',
            'appiumVersion': config.appium_version,
            'userName': config.user_name,
            'accessKey': config.access_key,
        },
    })


def _local_options(config):
    return UiAutomator2Options().load_capabilities({
        'platformName': 'android',
        'platformVersion': config.platform_version,
        'deviceName': config.device_name,
        'app': config.app_path,
        'appium:language': 'en',
        'appium:locale': 'US',
    })


@pytest.fixture(scope='function')
def android_mobile_management():
    config = load_config()
    is_local = CONTEXT == 'local'
    options = _local_options(config) if is_local else _bstack_options(config)

    with allure.step('setup app session'):
        browser.config.driver = webdriver.Remote(config.remote_browser_url, options=options)

    browser.config.timeout = 10.0
    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext)

    yield

    attach_mobile.screenshot()
    attach_mobile.page_source_xml()
    session_id = browser.driver.session_id

    with allure.step('tear down app session'):
        browser.quit()

    if not is_local:
        attach_mobile.bstack_video(session_id)