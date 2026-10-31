from selene import browser, be, have


class BookPage:

    def open(self, book):
        browser.open(f"book/{book.url}")
        return self

    # ---------- Избранное ----------

    def open_favorites_from_menu(self):
        browser.open('my-books/liked/')

        browser.should(
            have.url_containing('/my-books/liked/')
        )

        return self

    def is_book_in_favorites(self, book):
        self.open_favorites_from_menu()

        return browser.element(
            f'a[data-testid="art__title"][href="/book/{book.url}"]'
        ).matching(be.visible)

    def adding_book_to_favorites(self):
        favorite_icon = browser.element(
            '[data-testid="icon_favoritesFilled"]'
        )

        if not favorite_icon.matching(be.visible):
            browser.element(
                '[data-analytics-id="wishlist-button"]'
            ).should(be.visible).click()

            browser.element(
                '[data-testid="icon_favoritesFilled"]'
            ).should(be.visible)

        return self

    def removing_book_from_favorites(self):
        favorite_icon = browser.element(
            '[data-testid="icon_favoritesFilled"]'
        )

        if favorite_icon.matching(be.visible):
            browser.element(
                '[data-analytics-id="wishlist-button"]'
            ).should(be.visible).click()

            browser.element(
                '[data-testid="icon_favorites"]'
            ).should(be.visible)

        return self

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

    def cleanup_favorite(self, book):
        self.open(book)

        self.removing_book_from_favorites()

        return self

    # ---------- Корзина ----------

    def adding_book_to_cart(self):
        browser.element(
            '[data-test-id="book__addToCartButton--desktop"]'
        ).should(be.visible).click()

        return self

    def book_must_be_added_to_cart(self, book):
        browser.open("my-books/cart/")

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
        browser.element(
            '[data-test-id="book__addToCartButton--desktop"]'
        ).should(be.visible).click()

        return self

    def books_must_be_added_to_cart(self, book1, book2):
        browser.open("my-books/cart/")

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