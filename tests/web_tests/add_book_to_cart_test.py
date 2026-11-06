import allure
from litres_test_project.data.books import Book
from litres_test_project.pages.web_pages.book_page import book_page

@allure.epic('Add book to cart')
@allure.label("owner", "flowerfrog")
@allure.feature("Checking whether a books have been added")
@allure.label('microservice', 'WEB')
@allure.tag('regress', 'web', 'normal')
@allure.severity('normal')
@allure.label('layer', 'web')
def test_adding_book_to_cart():
    book = Book(
        name='Ведьмак',
        author='Анджей Сапковский',
        url='andzhey-sapkovskiy/vedmak-6375365/',
        price='1 599 ₽'
    )

    with allure.step("Open the book page"):
        book_page.open(book)

    with allure.step("Adding the selected book to the cart"):
        book_page.adding_book_to_cart()

    with allure.step("Checking that the book has been added to the cart"):
        book_page.book_must_be_added_to_cart(book)


@allure.epic('Add book to cart')
@allure.label("owner", "flowerfrog")
@allure.feature("Checking whether a books has been added to cart")
@allure.label('microservice', 'WEB')
@allure.tag('regress', 'web', 'normal')
@allure.severity('normal')
@allure.label('layer', 'web')
def test_adding_books_to_cart():
    book1 = Book(
        name='Ведьмак',
        author='Анджей Сапковский',
        url='andzhey-sapkovskiy/vedmak-6375365/',
        price='1 599 ₽'
    )

    book2 = Book(
        name='Ведьмак в озвучке Всеволода Кузнецова',
        author='Анджей Сапковский',
        url='andzhey-sapkovskiy/vedmak-v-ozvuchke-vsevoloda-kuznecova-70548067/',
        price='2 599 ₽'
    )

    with allure.step("Open the first book page"):
        book_page.open(book1)

    with allure.step("Adding the selected book to the cart"):
        book_page.adding_book_to_cart()

    with allure.step("Open the second book page"):
        book_page.open(book2)

    with allure.step("Adding the selected book to the cart"):
        book_page.adding_book_to_cart()

    with allure.step("Checking that the books has been added to the cart"):
        book_page.books_must_be_added_to_cart(book1, book2)