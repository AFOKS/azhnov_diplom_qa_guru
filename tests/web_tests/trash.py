import allure
from litres_test_project.data.books import Book
from litres_test_project.pages.web_pages.book_page import book_page


@allure.epic('Move book to/from favorites')
@allure.label("owner", "flowerfrog")
@allure.feature("Checking whether a book has been added or removed from favorites")
@allure.label('microservice', 'WEB')
@allure.tag('regress', 'web', 'normal')
@allure.severity('normal')
@allure.label('layer', 'web')
def test_adding_book_to_favorites():

    book = Book(
        name='Семь сестер. Потерянная сестра',
        author='Люсинда Райли',
        url='lusinda-rayli/sem-sester-poteryannaya-sestra-69175546/',
        price=''
    )

    with allure.step("Open the book page"):
        book_page.open(book)

    with allure.step("Adding a book to favorites"):
        book_page.adding_book_to_favorites()

    with allure.step("Checking that the book has been added to favorites"):
        book_page.book_must_be_added_to_favorites(book)


@allure.epic('Move book to/from favorites')
@allure.label("owner", "flowerfrog")
@allure.feature("Checking whether a book has been added or removed from favorites")
@allure.label('microservice', 'WEB')
@allure.tag('regress', 'web', 'normal')
@allure.severity('normal')
@allure.label('layer', 'web')
def test_removing_book_from_favorites():

    book = Book(
        name='Семь сестер. Потерянная сестра',
        author='Люсинда Райли',
        url='lusinda-rayli/sem-sester-poteryannaya-sestra-69175546/',
        price=''
    )

    with allure.step("Open the book page"):
        book_page.open(book)

    with allure.step("Adding a book to favorites"):
        book_page.adding_book_to_favorites()

    with allure.step("Removing a book to favorites"):
        book_page.removing_book_from_favorites()

    with allure.step("Checking that the book has been removed from favorites"):
        book_page.book_must_be_removed_from_favorites()



###

from selene import browser, be, have, command


class BookPage:
    actions = '[class*="book__actionButtons"]:not([class*="_mobile"])'
    favorite_button = f'{actions} button[data-analytics-id="wishlist-button"]'
    favorite_icon = f'{actions} [data-testid="icon_favorites"]'
    favorite_filled_icon = f'{actions} [data-testid="icon_favoritesFilled"]'
    favorite_any_icon = f'{actions} [data-testid^="icon_favorites"]'

    cart_button = 'button[data-testid="book__addToCartButton"]'

    @staticmethod
    def _visible(css):
        # первый ВИДИМЫЙ элемент среди совпадений
        return browser.all(css).element_by(be.visible)

    def open(self, book):
        browser.open(f'book/{book.url}')
        return self

    def open_favorites_from_menu(self):
        browser.open('my-books/liked/')
        browser.should(have.url_containing('/my-books/liked/'))
        return self

    def _set_favorite_state(self, filled: bool):
        target = self.favorite_filled_icon if filled else self.favorite_icon

        self._visible(self.favorite_any_icon).should(be.visible)

        if self._visible(target).matching(be.visible):
            return self

        self._visible(self.favorite_button).perform(command.js.click)
        self._visible(target).should(be.visible)
        return self

    def adding_book_to_favorites(self):
        return self._set_favorite_state(filled=True)

    def removing_book_from_favorites(self):
        return self._set_favorite_state(filled=False)

    def ensure_in_favorites(self):
        return self._set_favorite_state(filled=True)

    def ensure_not_in_favorites(self):
        return self._set_favorite_state(filled=False)

    def book_must_be_added_to_favorites(self, book):
        self.open_favorites_from_menu()
        browser.element(
            f'a[data-testid="art__title"][href="/book/{book.url}"]'
        ).should(be.visible).should(have.text(book.name))
        return self

    def book_must_be_removed_from_favorites(self, book):
        self.open_favorites_from_menu()
        browser.element(
            f'a[data-testid="art__title"][href="/book/{book.url}"]'
        ).should(be.absent)
        return self

    # ---------- Корзина ----------

    def adding_book_to_cart(self):
        browser.element(self.cart_button).should(be.visible).click()
        return self

    def book_must_be_added_to_cart(self, book):
        browser.open('my-books/cart/')

        browser.element(
            '[data-test-id="cart__bookCardTitle--wrapper"]'
        ).should(have.text(book.name))

        browser.element(
            '[data-test-id="cart__bookCardAuthor--wrapper"]'
        ).should(have.text(book.author))

        browser.element(
            '[data-test-id="cart__bookCardDiscount--wrapper"]'
        ).should(have.text(book.price))

        return self

    def adding_books_to_cart(self):
        browser.element(self.cart_button).should(be.visible).click()
        return self

    def books_must_be_added_to_cart(self, book1, book2):
        browser.open('my-books/cart/')

        browser.element(
            f'h3 > a[href="/book/{book2.url}"]'
        ).should(have.text(book2.name))

        browser.element(
            'div:nth-child(1) > div.Cart-module__bookCard__author_20vL8'
        ).should(have.text(book2.author))

        browser.element(
            'div:nth-child(1) > div.Cart-module__bookCard__price_336CO'
        ).should(have.text(book2.price))

        browser.element(
            f'h3 > a[href="/book/{book1.url}"]'
        ).should(have.text(book1.name))

        browser.element(
            'div:nth-child(2) > div.Cart-module__bookCard__author_20vL8'
        ).should(have.text(book1.author))

        browser.element(
            'div:nth-child(2) > div.Cart-module__bookCard__price_336CO'
        ).should(have.text(book1.price))

        return self


book_page = BookPage()


#### book_page



import time

from selene import browser, be, have, command
from selene.core.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)

from litres_test_project.pages.web_pages.main_page import main_page


class BookPage:
    # Кнопки действий на странице книги
    actions = '[class*="book__actionButtons"]'

    favorite_button = (
        f'{actions} button[data-analytics-id="wishlist-button"]'
    )
    favorite_icon = '[data-testid="icon_favorites"]'
    favorite_filled_icon = '[data-testid="icon_favoritesFilled"]'

    # Корзина
    cart_button = 'button[data-testid="book__addToCartButton"]'
    go_to_cart_button = 'button[data-testid="book__goToCartButton"]'

    # Поп-ап
    popup = '[data-testid="modal--wrapper"]'
    popup_close_icon = (
        '[data-testid="modal--wrapper"] [data-testid="icon_close"]'
    )

    # Элементы карточек в корзине
    cart_items = '[data-testid^="cart__listItem--"]'
    cart_title = '[data-testid="cart__bookCardTitle--wrapper"]'
    cart_author = '[data-testid="art__authorName--link"]'
    cart_price = '[data-testid="art__finalPrice"]'

    @staticmethod
    def _visible(selector):
        return browser.all(selector).element_by(be.visible)

    def open(self, book):
        browser.open(f'book/{book.url}')
        main_page.accept_cookies()
        return self

    def open_favorites_from_menu(self):
        browser.open('my-books/liked/')
        browser.should(have.url_containing('/my-books/liked/'))
        return self

    # Избранное

    # Избранное

    def _get_favorite_button(self):
        """
        Находит видимую кнопку избранного,
        внутри которой присутствует одна из иконок состояния.
        """

        buttons = browser.driver.find_elements(
            By.CSS_SELECTOR,
            self.favorite_button
        )

        suitable_buttons = []

        for button in buttons:
            if not button.is_displayed():
                continue

            icons = button.find_elements(
                By.CSS_SELECTOR,
                f'{self.favorite_icon}, {self.favorite_filled_icon}'
            )

            if icons:
                suitable_buttons.append(button)

        if len(suitable_buttons) != 1:
            details = [
                {
                    'visible': button.is_displayed(),
                    'html': button.get_attribute('outerHTML')
                }
                for button in buttons
            ]

            raise AssertionError(
                f'Ожидалась одна видимая кнопка избранного '
                f'с иконкой, найдено: {len(suitable_buttons)}. '
                f'Все найденные кнопки: {details}'
            )

        return suitable_buttons[0]

    def _is_book_in_favorites(self):
        """
        Проверяет, добавлена ли книга в избранное.
        """

        button = self._get_favorite_button()

        filled_icon = button.find_elements(
            By.CSS_SELECTOR,
            self.favorite_filled_icon
        )

        return bool(filled_icon)

    def _set_favorite_state(self, filled: bool):
        """
        Устанавливает нужное состояние избранного.

        filled=True — книга должна быть добавлена.
        filled=False — книга должна быть удалена.
        """

        if self._is_book_in_favorites() == filled:
            return self

        button = self._get_favorite_button()
        button.click()

        def favorite_state_is_correct(driver):
            try:
                return self._is_book_in_favorites() == filled
            except (
                    NoSuchElementException,
                    StaleElementReferenceException,
                    AssertionError,
            ):
                return False

        from selenium.webdriver.support.ui import WebDriverWait

        WebDriverWait(
            browser.driver,
            10
        ).until(favorite_state_is_correct)

        return self

    def adding_book_to_favorites(self):
        return self._set_favorite_state(filled=True)

    def removing_book_from_favorites(self):
        return self._set_favorite_state(filled=False)

    def ensure_not_in_favorites(self):
        return self._set_favorite_state(filled=False)


    def book_must_be_added_to_favorites(self, book):
        """Проверяет наличие книги в списке избранного."""
        deadline = time.time() + 20

        while True:
            self.open_favorites_from_menu()

            try:
                browser.element(
                    f'a[href*="-{book.id}/"]'
                ).with_(timeout=4).should(be.visible)

                break

            except TimeoutException:
                if time.time() > deadline:
                    raise

        return self

    def book_must_be_removed_from_favorites(self, book):
        """Проверяет отсутствие книги в списке избранного."""
        self.open_favorites_from_menu()

        browser.element(
            f'a[data-testid="art__title"][href="/book/{book.url}"]'
        ).should(be.absent)

        return self

    # Поп-ап

    def _close_gift_popup_if_shown(self):
        try:
            browser.element(
                self.popup_close_icon
            ).with_(timeout=6).should(be.visible)

        except TimeoutException:
            return self

        browser.element(
            self.popup_close_icon
        ).perform(command.js.click)

        browser.element(self.popup).should(be.not_.present)

        return self

    # Корзина

    def adding_book_to_cart(self):
        add_button = browser.element(
            self.cart_button
        ).should(be.visible)

        go_to_cart = browser.element(
            self.go_to_cart_button
        )

        deadline = time.time() + 20

        while True:
            add_button.perform(command.js.click)

            try:
                go_to_cart.with_(timeout=4).should(be.visible)
                break

            except TimeoutException:
                if time.time() > deadline:
                    raise

        self._close_gift_popup_if_shown()

        return self

    def go_to_cart(self):
        browser.element(
            self.go_to_cart_button
        ).should(be.visible).perform(command.js.click)

        browser.should(have.url_containing('/my-books/cart/'))

        return self

    def _book_card_must_be_in_cart(self, book):
        card = browser.element(
            f'[data-testid="cart__listItem--{book.id}"]'
        ).should(be.visible)

        card.element(self.cart_title).should(
            have.exact_text(book.name)
        )

        card.element(self.cart_author).should(
            have.exact_text(book.author)
        )

        card.element(self.cart_price).should(
            have.attribute('aria-label').value(book.price_aria)
        )

        return self

    def book_must_be_added_to_cart(self, book):
        self.go_to_cart()

        browser.all(self.cart_items).should(have.size(1))

        self._book_card_must_be_in_cart(book)

        return self

    def books_must_be_added_to_cart(self, book1, book2):
        self.go_to_cart()

        browser.all(self.cart_items).should(have.size(2))

        for book in (book1, book2):
            self._book_card_must_be_in_cart(book)

        return self


book_page = BookPage()
