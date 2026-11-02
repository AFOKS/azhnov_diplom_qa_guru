
import time

from selene import browser, be, have, command
from selene.core.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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

    # Открытие страницы книги

    def open(self, book):
        browser.open(f'book/{book.url}')
        main_page.accept_cookies()
        return self

    def open_favorites_from_menu(self):
        browser.open('my-books/liked/')
        browser.should(have.url_containing('/my-books/liked/'))
        return self

    # Избранное

    def _get_favorite_button(self):
        """
        Находит единственную видимую кнопку избранного
        с иконкой состояния.
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
                f'Ожидалась одна видимая кнопка избранного, '
                f'найдено: {len(suitable_buttons)}. '
                f'Найденные кнопки: {details}'
            )

        return suitable_buttons[0]

    def _is_book_in_favorites(self):
        """
        Проверяет, добавлена ли книга в избранное.
        """

        button = self._get_favorite_button()

        filled_icons = button.find_elements(
            By.CSS_SELECTOR,
            self.favorite_filled_icon
        )

        if any(icon.is_displayed() for icon in filled_icons):
            return True

        empty_icons = button.find_elements(
            By.CSS_SELECTOR,
            self.favorite_icon
        )

        if any(icon.is_displayed() for icon in empty_icons):
            return False

        raise AssertionError(
            f'Не удалось определить состояние избранного. '
            f'HTML кнопки: {button.get_attribute("outerHTML")}'
        )

    def _set_favorite_state(self, filled: bool):
        """
        Устанавливает нужное состояние избранного.

        filled=True — книга добавлена.
        filled=False — книга удалена.
        """

        current_state = self._is_book_in_favorites()

        print(f'Текущее состояние избранного: {current_state}')
        print(f'Ожидаемое состояние избранного: {filled}')

        if current_state == filled:
            print('Книга уже находится в нужном состоянии')
            return self

        button = self._get_favorite_button()

        print(f'Кнопка избранного до клика: {button.get_attribute("outerHTML")}')

        button.click()

        def favorite_state_is_correct(driver):
            try:
                actual_state = self._is_book_in_favorites()

                print(f'Текущее состояние после клика: {actual_state}')

                return actual_state == filled

            except (
                    NoSuchElementException,
                    StaleElementReferenceException,
            ):
                return False

        WebDriverWait(
            browser.driver,
            10
        ).until(favorite_state_is_correct)

        return self

        def favorite_state_is_correct(driver):
            try:
                return self._is_book_in_favorites() == filled

            except (
                NoSuchElementException,
                StaleElementReferenceException,
                AssertionError,
            ):
                return False

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
        """
        Проверяет наличие книги в списке избранного.
        """

        self.open_favorites_from_menu()

        browser.element(
            f'a[href*="-{book.id}/"]'
        ).with_(timeout=10).should(be.visible)

        return self

    def book_must_be_removed_from_favorites(self, book):
        """
        Проверяет отсутствие книги в списке избранного.
        """

        self.open_favorites_from_menu()

        browser.element(
            f'a[data-testid="art__title"][href="/book/{book.url}"]'
        ).with_(timeout=10).should(be.absent)

        return self

    # Поп-ап

    def _close_gift_popup_if_shown(self):
        """
        Закрывает поп-ап, если он появился.
        """

        try:
            close_button = browser.element(
                self.popup_close_icon
            ).with_(timeout=6).should(be.visible)

        except TimeoutException:
            return self

        close_button.perform(command.js.click)

        browser.element(
            self.popup
        ).should(be.not_.present)

        return self

    # Корзина

    def adding_book_to_cart(self):
        """
        Добавляет книгу в корзину и ожидает появления
        кнопки перехода в корзину.
        """

        browser.element(
            self.cart_button
        ).should(be.visible).click()

        browser.element(
            self.go_to_cart_button
        ).with_(timeout=10).should(be.visible)

        self._close_gift_popup_if_shown()

        return self

    def go_to_cart(self):
        """
        Переходит в корзину.
        """

        browser.element(
            self.go_to_cart_button
        ).should(be.visible).perform(command.js.click)

        browser.should(have.url_containing('/my-books/cart/'))

        return self

    def _book_card_must_be_in_cart(self, book):
        """
        Проверяет информацию о книге в корзине.
        """

        card = browser.element(
            f'[data-testid="cart__listItem--{book.id}"]'
        ).should(be.visible)

        card.element(
            self.cart_title
        ).should(have.exact_text(book.name))

        card.element(
            self.cart_author
        ).should(have.exact_text(book.author))

        card.element(
            self.cart_price
        ).should(
            have.attribute('aria-label').value(book.price_aria)
        )

        return self

    def book_must_be_added_to_cart(self, book):
        """
        Проверяет, что в корзине находится одна книга.
        """

        self.go_to_cart()

        browser.all(
            self.cart_items
        ).should(have.size(1))

        self._book_card_must_be_in_cart(book)

        return self

    def books_must_be_added_to_cart(self, book1, book2):
        """
        Проверяет, что в корзине находятся две книги.
        """

        self.go_to_cart()

        browser.all(
            self.cart_items
        ).should(have.size(2))

        for book in (book1, book2):
            self._book_card_must_be_in_cart(book)

        return self


book_page = BookPage()
