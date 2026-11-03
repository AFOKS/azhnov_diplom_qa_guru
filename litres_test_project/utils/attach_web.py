import os

import allure
from allure_commons.types import AttachmentType
from selenium.common.exceptions import WebDriverException


def add_screenshot(browser):
    png = browser.driver.get_screenshot_as_png()
    allure.attach(body=png, name='screenshot', attachment_type=AttachmentType.PNG, extension='.png')


def add_logs(browser):
    try:
        entries = browser.driver.execute('getLog', {'type': 'browser'})['value']
    except (WebDriverException, KeyError, TypeError) as error:
        log = f'Browser logs are not available: {error}'
    else:
        log = '\n'.join(
            f"{entry.get('level')}: {entry.get('message')}" for entry in entries
        ) or 'Browser log is empty'

    allure.attach(log, 'browser_logs', AttachmentType.TEXT, '.log')


def add_html(browser):
    html = browser.driver.page_source
    allure.attach(html, 'page_source', AttachmentType.HTML, '.html')


def add_video(browser):
    selenoid_url = os.getenv('SELENOID_URL', 'selenoid.autotests.cloud')
    video_url = f'https://{selenoid_url}/video/{browser.driver.session_id}.mp4'
    html = (
        "<html><body><video width='100%' height='100%' controls autoplay>"
        f"<source src='{video_url}' type='video/mp4'></video></body></html>"
    )
    allure.attach(html, 'video', AttachmentType.HTML, '.html')