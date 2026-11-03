import os

import allure
import jsonschema

from litres_test_project.utils.api_requests import api_post
from litres_test_project.utils.load_schema import load_schema


@allure.epic('API. Authorized')
@allure.label('owner', 'flowerfrog')
@allure.feature('Checking the authorization of the user')
@allure.label('microservice', 'API')
@allure.tag('regress', 'api', 'normal')
@allure.label('layer', 'api')
@allure.severity('normal')
def test_authorization_registered_user():
    email = os.getenv('USER_EMAIL')
    password = os.getenv('USER_PASSWORD')
    assert email and password, 'USER_EMAIL / USER_PASSWORD не загружены из .env'
    request_body = {'login': email, 'password': password}
    jsonschema.validate(request_body, load_schema('auth_request.json'))

    result = api_post('/auth/login', json=request_body)

    assert result.status_code == 200
    jsonschema.validate(result.json(), load_schema('successful_authorization.json'))
    assert result.json()['error'] is None


@allure.epic('API. Authorized')
@allure.label('owner', 'flowerfrog')
@allure.feature('Checking the authorization of the user')
@allure.label('microservice', 'API')
@allure.tag('regress', 'api', 'normal')
@allure.label('layer', 'api')
@allure.severity('normal')
def test_authorization_unregistered_user():
    email = os.getenv('USER_EMAIL')
    invalid_password = os.getenv('UNREGISTERED_USER_PASSWORD')
    assert email and invalid_password, 'USER_EMAIL / UNREGISTERED_USER_PASSWORD не загружены из .env'
    request_body = {'login': email, 'password': invalid_password}
    jsonschema.validate(request_body, load_schema('auth_request.json'))

    result = api_post('/auth/login', json=request_body)

    assert result.status_code == 401
    jsonschema.validate(result.json(), load_schema('unsuccessful_authorization.json'))
    assert result.json()['error']['type'] == 'Unauthorized'
    assert result.json()['error']['title'] == 'Incorrect user data'