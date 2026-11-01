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