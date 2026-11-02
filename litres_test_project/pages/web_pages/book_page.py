import time

from selene import browser, be, have, command
from selene.core.exceptions import TimeoutException
from litres_test_project.pages.web_pages.main_page import main_page

class BookPage:
    actions = '[class*="book__actionButtons"]:not([class*="_mobile"])'
    favorite_button = '[data-testid="wishlist__button"]'
    favorite_icon = '[data-testid="icon_favorites"]'
    favorite_filled_icon = '[data-testid="icon_favoritesFilled"]'
    favorite_any_icon = f'{actions} [data-testid^="icon_favorites"]'

    cart_button = 'button[data-testid="book__addToCartButton"]'
    go_to_cart_button = 'button[data-testid="book__goToCartButton"]'
    popup = '[data-testid="modal--wrapper"]'
    popup_close_icon = '[data-testid="modal--wrapper"] [data-testid="icon_close"]'

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

    def _set_favorite_state(self, filled: bool):
        self._visible(self.favorite_any_icon).should(be.visible)

        is_filled = self._visible(
            self.favorite_filled_icon
        ).matching(be.visible)

        # Если книга уже находится в нужном состоянии,
        # ничего не делаем
        if is_filled == filled:
            return self

        # Переключаем состояние избранного
        self._visible(self.favorite_button).perform(command.js.click)

        if filled:
            self._visible(self.favorite_filled_icon).should(be.visible)
        else:
            browser.element(
                self.favorite_filled_icon
            ).should(be.absent)

        return self

    def adding_book_to_favorites(self):
        self._visible(self.favorite_button).click()

        self._visible(self.favorite_filled_icon).should(be.visible)

        return self

    def removing_book_from_favorites(self):
        self._visible(self.favorite_button).click()

        self._visible(self.favorite_icon).should(be.visible)

        return self

    def ensure_in_favorites(self):
        return self._set_favorite_state(filled=True)

    def ensure_not_in_favorites(self):
        return self._set_favorite_state(filled=False)

    def book_must_be_added_to_favorites(self, book):
        link = browser.element(f'a[href*="-{book.id}/"]')

        deadline = time.time() + 20
        while True:
            self.open_favorites_from_menu()
            try:
                link.with_(timeout=4).should(be.visible)
                break
            except TimeoutException:
                if time.time() > deadline:
                    raise
        return self

    def book_must_be_removed_from_favorites(self, book):
        self.open_favorites_from_menu()
        browser.element(
            f'a[data-testid="art__title"][href="/book/{book.url}"]'
        ).should(be.absent)
        return self

    def _close_gift_popup_if_shown(self):
        # поп-ап «Книга в подарок» появляется с задержкой и не всегда
        try:
            browser.element(self.popup_close_icon).with_(timeout=6).should(be.visible)
        except TimeoutException:
            return self
        browser.element(self.popup_close_icon).perform(command.js.click)
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
        browser.element(self.go_to_cart_button).should(be.visible).perform(command.js.click)
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