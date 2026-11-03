import json

import allure
from allure_commons.types import AttachmentType


def mask_secrets(body):
    if isinstance(body, dict):
        return {key: '***' if key == 'password' else value for key, value in body.items()}
    return body


def add_request(response, body=None):
    allure.attach(f'{response.request.method} {response.request.url}', 'request_url', AttachmentType.TEXT, '.txt')
    if body is not None:
        allure.attach(json.dumps(mask_secrets(body), indent=4, ensure_ascii=False), 'request_body', AttachmentType.JSON, '.json')


def add_response(response):
    allure.attach(f'Status code: {response.status_code}', 'response_status', AttachmentType.TEXT, '.txt')
    try:
        body = json.dumps(response.json(), indent=4, ensure_ascii=False)
        attachment_type, extension = AttachmentType.JSON, '.json'
    except ValueError:
        body = response.text
        attachment_type, extension = AttachmentType.TEXT, '.txt'
    allure.attach(body, 'response_body', attachment_type, extension)