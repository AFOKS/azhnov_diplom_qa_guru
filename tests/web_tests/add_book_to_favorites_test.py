import allure
from litres_test_project.data.books import Book
from litres_test_project.pages.web_pages.main_page import main_page
from litres_test_project.pages.web_pages.book_page import book_page

book = Book(
    name='Ведьмак',
    author='Анджей Сапковский',
    url='andzhey-sapkovskiy/vedmak-6375365/',
    price=''
)


@allure.epic('Move book to/from favorites')
@allure.label("owner", "flowerfrog")
@allure.feature("Checking whether a book has been added or removed from favorites")
@allure.label('microservice', 'WEB')
@allure.tag('regress', 'web', 'normal')
@allure.severity('normal')
@allure.label('layer', 'web')
def test_adding_book_to_favorites(authorized_user):
    with allure.step("Search for the book by title"):
        main_page.open()
        main_page.search_book_by_title(book)

    with allure.step("Open the book page from search results"):
        main_page.open_book_from_search(book)

    with allure.step("Click the heart on the book page"):
        book_page.adding_book_to_favorites()

    with allure.step("Open 'My books' -> 'Отложено'"):
        book_page.open_favorites_from_menu()

    with allure.step("Check that the book is in favorites"):
        book_page.book_must_be_added_to_favorites(book)

    with allure.step("Cleanup: remove the book from favorites"):
        book_page.cleanup_favorite(book)


@allure.epic('Move book to/from favorites')
@allure.label("owner", "flowerfrog")
@allure.feature("Checking whether a book has been added or removed from favorites")
@allure.label('microservice', 'WEB')
@allure.tag('regress', 'web', 'normal')
@allure.severity('normal')
@allure.label('layer', 'web')
def test_removing_book_from_favorites(authorized_user):
    with allure.step("Search for the book by title"):
        main_page.open()
        main_page.search_book_by_title(book)

    with allure.step("Open the book page from search results"):
        main_page.open_book_from_search(book)

    with allure.step("Add the book to favorites"):
        book_page.adding_book_to_favorites()

    with allure.step("Remove the book from favorites"):
        book_page.removing_book_from_favorites()

    with allure.step("Open 'My books' -> 'Отложено'"):
        book_page.open_favorites_from_menu()

    with allure.step("Check that the book is not in favorites"):
        book_page.book_must_be_removed_from_favorites(book)