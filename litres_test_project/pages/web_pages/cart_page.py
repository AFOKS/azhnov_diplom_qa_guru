import time

from selene import browser, be, command
from selene.core.exceptions import TimeoutException



class CartPage:
    cart_items = '[data-testid^="cart__listItem--"]'
    delete_button = '[data-testid="cart__listDeleteButton"]'
    confirm_delete_button = '[data-testid="cart__modalDeleteArt--button-primary"]'
    move_to_favorites_and_delete_button = '[data-testid="cart__modalDeleteArt--button-secondary"]'
    empty_state = '[data-testid="cart__emptyState--wrapper"]'
    modal = '[data-testid="modal--wrapper"]'

    @staticmethod
    def _card(book):
        return browser.element(f'[data-testid="cart__listItem--{book.id}"]')

    def open(self):
        browser.open('my-books/cart/')
        return self

    def _confirm_in_modal(self, button_locator):
        button = browser.element(button_locator).should(be.visible)
        modal = browser.element(self.modal)

        deadline = time.time() + 20
        while True:
            button.perform(command.js.click)
            try:
                modal.with_(timeout=4).should(be.not_.present)
                break
            except TimeoutException:
                if time.time() > deadline:
                    raise
        return self

    def _open_delete_modal(self, book):
        card = self._card(book).should(be.visible)
        delete_button = card.element(self.delete_button).should(be.visible)
        delete_button.perform(command.js.click)
        # убеждаемся, что модалка открылась, до клика по её кнопкам
        browser.element(self.confirm_delete_button).should(be.visible)
        return self

    def removing_book_from_cart(self, book):
        self._open_delete_modal(book)
        return self._confirm_in_modal(self.confirm_delete_button)

    def removing_book_from_cart_and_adding_to_favorites(self, book):
        self._open_delete_modal(book)
        return self._confirm_in_modal(self.move_to_favorites_and_delete_button)

    def book_must_be_removed_from_cart(self, book):
        self._card(book).should(be.absent)
        return self

    def cart_must_be_empty(self):
        browser.element(self.empty_state).should(be.visible)
        return self

    def ensure_book_not_in_cart(self, book):
        self.open()
        # ждём, пока загрузится либо список книг, либо экран пустой корзины
        browser.element(f'{self.cart_items}, {self.empty_state}').should(be.visible)
        if self._card(book).matching(be.visible):
            self.removing_book_from_cart(book)
            self.book_must_be_removed_from_cart(book)
        return self


cart_page = CartPage()