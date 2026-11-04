import allure
import jsonschema

from litres_test_project.utils.api_requests import api_get
from litres_test_project.utils.load_schema import load_schema


@allure.epic('API. Search')
@allure.label('owner', 'flowerfrog')
@allure.feature('Checking the book search on the main page')
@allure.label('microservice', 'API')
@allure.tag('regress', 'api', 'normal')
@allure.label('layer', 'api')
@allure.severity('normal')
def test_successful_searching_of_book_by_title():
    params = {'q': 'Ведьмак', 'art_types': 'text_book', 'types': 'text_book'}

    result = api_get('/search', params=params)

    assert result.status_code == 200
    jsonschema.validate(result.json(), load_schema('successful_searching_book.json'))
    books = result.json()['payload']['data']
    assert books
    assert all(book['type'] == 'text_book' for book in books)
    assert any('ведьмак' in book['instance']['title'].lower() for book in books)


@allure.epic('API. Search')
@allure.label('owner', 'flowerfrog')
@allure.feature('Checking the book search on the main page')
@allure.label('microservice', 'API')
@allure.tag('regress', 'api', 'normal')
@allure.label('layer', 'api')
@allure.severity('normal')
def test_unsuccessful_searching_of_book_by_title():
    params = {'q': 'nbmcgfhmghm', 'types': 'text_book'}

    result = api_get('/search', params=params)

    assert result.status_code == 200
    jsonschema.validate(result.json(), load_schema('unsuccessful_searching_book.json'))
    assert result.json()['payload']['data'] == []