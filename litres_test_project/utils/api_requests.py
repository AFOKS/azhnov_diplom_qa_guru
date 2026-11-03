import logging
import os

import allure
import requests

from litres_test_project.utils.attach_api import add_request, add_response


DEFAULT_HEADERS = {
    'app-id': '115',
    'client-host': 'www.litres.ru',
    'origin': 'https://www.litres.ru',
    'referer': 'https://www.litres.ru/',
    'user-agent': 'Mozilla/5.0',
}


def _request(method, endpoint, **kwargs):
    base_url = os.getenv('API_BASE_URL', 'https://api.litres.ru/foundation/api')
    headers = {**DEFAULT_HEADERS, **kwargs.pop('headers', {})}
    with allure.step(f'{method} {endpoint}'):
        response = requests.request(method, base_url + endpoint, headers=headers, **kwargs)
        add_request(response, kwargs.get('json'))
        add_response(response)
        logging.info('%s %s', method, response.request.url)
        logging.info(response.status_code)
        logging.info(response.text)
        return response


def api_get(endpoint, **kwargs):
    return _request('GET', endpoint, **kwargs)


def api_post(endpoint, **kwargs):
    return _request('POST', endpoint, **kwargs)


def api_delete(endpoint, **kwargs):
    return _request('DELETE', endpoint, **kwargs)