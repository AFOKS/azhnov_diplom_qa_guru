import allure

from litres_test_project.data.books import Book
from litres_test_project.pages.web_pages.book_page import book_page
from litres_test_project.pages.web_pages.cart_page import cart_page


@allure.epic('Remove book from cart')
@allure.label("owner", "flowerfrog")
@allure.feature("Checking whether a book has been removed from cart")
@allure.label('microservice', 'WEB')
@allure.tag('regress', 'web', 'normal')
@allure.severity('normal')
@allure.label('layer', 'web')
def test_removing_book_from_cart():
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

    with allure.step("Go to the cart page"):
        book_page.go_to_cart()

    with allure.step("Removing the selected book from cart"):
        cart_page.removing_book_from_cart(book)

    with allure.step("Checking that the book has been removed from cart"):
        cart_page.book_must_be_removed_from_cart(book)

    with allure.step("Checking that the cart is empty"):
        cart_page.cart_must_be_empty()


@allure.epic('Remove book from cart')
@allure.label("owner", "flowerfrog")
@allure.feature("Checking whether a book has been moved from cart to favorites")
@allure.label('microservice', 'WEB')
@allure.tag('regress', 'web', 'normal')
@allure.severity('normal')
@allure.label('layer', 'web')
def test_removing_book_from_cart_and_adding_to_favorites(authorized_user):
    book = Book(
        name='Ведьмак в озвучке Всеволода Кузнецова',
        author='Анджей Сапковский',
        url='andzhey-sapkovskiy/vedmak-v-ozvuchke-vsevoloda-kuznecova-70548067/',
        price='2 599 ₽'
    )

    with allure.step("Make sure the book is not in the cart"):
        cart_page.ensure_book_not_in_cart(book)

    with allure.step("Open the book page"):
        book_page.open(book)

    with allure.step("Make sure the book is not in favorites"):
        book_page.ensure_not_in_favorites()

    with allure.step("Adding the selected book to the cart"):
        book_page.adding_book_to_cart()

    with allure.step("Go to the cart page"):
        book_page.go_to_cart()

    with allure.step("Removing the selected book from cart and adding it to favorites"):
        cart_page.removing_book_from_cart_and_adding_to_favorites(book)

    with allure.step("Checking that the book has been removed from cart"):
        cart_page.book_must_be_removed_from_cart(book)

    with allure.step("Checking that the book has been added to favorites"):
        book_page.book_must_be_added_to_favorites(book)