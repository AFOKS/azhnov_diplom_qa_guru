import os

import pytest
from dotenv import find_dotenv, load_dotenv

from litres_test_project.utils.api_requests import api_post


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv(find_dotenv())


@pytest.fixture(scope='session')
def auth_headers():
    response = api_post('/auth/login', json={
        'login': os.getenv('USER_EMAIL'),
        'password': os.getenv('USER_PASSWORD'),
    })
    assert response.status_code == 200
    return {'session-id': response.json()['payload']['data']['sid']}