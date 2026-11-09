import time

from selene import browser, be, have, command
from selene.core.exceptions import TimeoutException
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException as SeleniumTimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from litres_test_project.pages.web_pages.main_page import main_page


class BookPage:

    actions = '[class*="book__actionButtons"]'
    favorite_button = f'{actions} button[data-analytics-id="wishlist-button"]'
    favorite_icon = '[data-testid="icon_favorites"]'
    favorite_filled_icon = '[data-testid="icon_favoritesFilled"]'

    cart_button = 'button[data-testid="book__addToCartButton"]'
    go_to_cart_button = 'button[data-testid="book__goToCartButton"]'

    popup = '[data-testid="modal--wrapper"]'
    popup_close_icon = f'{popup} [data-testid="icon_close"]'

    cart_items = '[data-testid^="cart__listItem--"]'
    cart_title = '[data-testid="cart__bookCardTitle--wrapper"]'
    cart_author = '[data-testid="art__authorName--link"]'
    cart_price = '[data-testid="art__finalPrice"]'

    def open(self, book):
        browser.open(f'book/{book.url}')
        main_page.accept_cookies()
        return self

    def open_favorites_from_menu(self):
        browser.open('my-books/liked/')
        browser.should(have.url_containing('/my-books/liked/'))
        return self

    def _get_favorite_button(self):
        buttons = browser.driver.find_elements(
            By.CSS_SELECTOR, self.favorite_button
        )

        suitable = [
            button for button in buttons
            if button.is_displayed() and button.find_elements(
                By.CSS_SELECTOR,
                f'{self.favorite_icon}, {self.favorite_filled_icon}'
            )
        ]

        if len(suitable) != 1:
            details = [
                {
                    'visible': button.is_displayed(),
                    'html': button.get_attribute('outerHTML'),
                }
                for button in buttons
            ]
            raise AssertionError(
                f'Ожидалась одна видимая кнопка избранного, '
                f'найдено: {len(suitable)}. Найденные кнопки: {details}'
            )

        return suitable[0]

    def _is_book_in_favorites(self):
        button = self._get_favorite_button()
        filled = button.find_elements(
            By.CSS_SELECTOR, self.favorite_filled_icon
        )
        if any(icon.is_displayed() for icon in filled):
            return True

        empty = button.find_elements(By.CSS_SELECTOR, self.favorite_icon)
        if any(icon.is_displayed() for icon in empty):
            return False

        raise AssertionError(
            f'Не удалось определить состояние избранного. '
            f'HTML кнопки: {button.get_attribute("outerHTML")}'
        )

    def _safe_favorite_state(self):
        try:
            return self._is_book_in_favorites()
        except (
            NoSuchElementException,
            StaleElementReferenceException,
            AssertionError,
        ):
            return None

    def _set_favorite_state(self, filled: bool):

        deadline = time.time() + 30

        while True:
            state = self._safe_favorite_state()
            if state == filled:
                return self

            if time.time() > deadline:
                raise AssertionError(
                    f'Не удалось привести избранное к состоянию {filled}, '
                    f'последнее состояние: {state}'
                )

            if state is None:
                time.sleep(0.5)
                continue

            button = self._get_favorite_button()
            browser.driver.execute_script('arguments[0].click();', button)

            try:
                WebDriverWait(browser.driver, 5).until(
                    lambda d: self._safe_favorite_state() == filled
                )
            except SeleniumTimeoutException:
                pass

    def adding_book_to_favorites(self):
        return self._set_favorite_state(filled=True)

    def removing_book_from_favorites(self):
        return self._set_favorite_state(filled=False)

    def ensure_in_favorites(self):
        return self._set_favorite_state(filled=True)

    def ensure_not_in_favorites(self):
        return self._set_favorite_state(filled=False)

    def book_must_not_be_in_favorites_yet(self):
        WebDriverWait(browser.driver, 10).until(
            lambda d: self._safe_favorite_state() is False,
            message='Книга уже в избранном до начала теста'
        )
        return self

    def book_must_be_added_to_favorites(self, book):
        self.open_favorites_from_menu()
        browser.element(f'a[href*="-{book.id}/"]').with_(timeout=10).should(
            be.visible
        )
        return self

    def book_must_be_removed_from_favorites(self, book):
        self.open(book)
        WebDriverWait(browser.driver, 10).until(
            lambda d: self._safe_favorite_state() is False,
            message='Книга всё ещё в избранном'
        )
        return self

    def _close_gift_popup_if_shown(self):
        close_button = browser.element(self.popup_close_icon)
        if close_button.with_(timeout=6).matching(be.visible):
            close_button.perform(command.js.click)
            browser.element(self.popup).should(be.not_.present)
        return self

    def adding_book_to_cart(self):
        add_button = browser.element(self.cart_button).should(be.visible)
        go_to_cart = browser.element(self.go_to_cart_button)

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
        browser.element(self.go_to_cart_button).should(be.visible).perform(
            command.js.click
        )
        browser.should(have.url_containing('/my-books/cart/'))
        return self

    def _book_card_must_be_in_cart(self, book):
        card = browser.element(
            f'[data-testid="cart__listItem--{book.id}"]'
        ).should(be.visible)

        card.element(self.cart_title).should(have.exact_text(book.name))
        card.element(self.cart_author).should(have.exact_text(book.author))
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