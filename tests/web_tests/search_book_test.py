
import allure

from litres_test_project.data.books import Book
from litres_test_project.pages.web_pages.main_page import main_page


@allure.epic('Search')
@allure.label("owner", "flowerfrog")
@allure.feature("Checking the book search on the main page")
@allure.label('microservice', 'WEB')
@allure.tag('regress', 'web', 'normal')
@allure.severity('normal')
@allure.label('layer', 'web')
def test_searching_of_book_by_title():
    book = Book(
        name='Ведьмак',
        author='Анджей Сапковский',
        url='',
        price=''
    )

    with allure.step("Open the main page"):
        main_page.open()

    with allure.step("Search for a book by title"):
        main_page.search_book_by_title(book)

    with allure.step("Check that the specified book is found"):
        main_page.book_with_specified_title_must_be_found()


@allure.epic('Search')
@allure.label("owner", "flowerfrog")
@allure.feature("Checking the book search on the main page")
@allure.label('microservice', 'WEB')
@allure.tag('regress', 'web', 'normal')
@allure.severity('normal')
@allure.label('layer', 'web')
def test_searching_of_book_by_author():
    book = Book(
        name='',
        author='Джордж Р. Р. Мартин',
        url='',
        price=''
    )

    with allure.step("Open the main page"):
        main_page.open()

    with allure.step("Search for an author by name"):
        main_page.search_book_by_author(book)

    with allure.step("Select the Authors tab"):
        main_page.select_authors_tab()

    with allure.step("Check that the specified author is found"):
        main_page.author_with_specified_name_must_be_found()
