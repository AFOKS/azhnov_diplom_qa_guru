import allure
import jsonschema

from litres_test_project.utils.api_requests import api_put
from litres_test_project.utils.load_schema import load_schema


@allure.epic('API. Cart')
@allure.label('owner', 'flowerfrog')
@allure.feature('Checking whether a book has been added to cart')
@allure.label('microservice', 'API')
@allure.tag('regress', 'api', 'normal')
@allure.label('layer', 'api')
@allure.severity('normal')
def test_adding_book_to_cart():
    art_ids = [6375365]
    request_body = {'art_ids': art_ids}
    jsonschema.validate(request_body, load_schema('add_to_cart_request.json'))

    result = api_put('/cart/arts/add', json=request_body)

    assert result.status_code == 200
    jsonschema.validate(result.json(), load_schema('successful_adding_book_to_cart.json'))
    assert result.json()['payload']['data']['added_art_ids'] == art_ids
    assert result.json()['payload']['data']['failed_art_ids'] == []

@allure.epic('API. Cart')
@allure.label('owner', 'flowerfrog')
@allure.feature('Checking the removal of a book from cart')
@allure.label('microservice', 'API')
@allure.tag('regress', 'api', 'normal')
@allure.label('layer', 'api')
@allure.severity('normal')
def test_removing_book_from_cart(auth_headers):
    request_body = {'art_ids': [6375365]}
    jsonschema.validate(request_body, load_schema('add_to_cart_request.json'))
    api_put('/cart/arts/add', headers=auth_headers, json=request_body)

    result = api_put('/cart/arts/remove', headers=auth_headers, json=request_body)

    assert result.status_code == 204
    assert result.text == ''