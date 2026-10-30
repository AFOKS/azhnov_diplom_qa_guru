
from selene import browser, be, have


class BookPage:
    def open(self, book):
        browser.open(f"book/{book.url}")
        return self

    # ---------- Избранное ----------

    def adding_book_to_favorites(self):
        buttons = browser.driver.find_elements(
            'css selector',
            '[data-analytics-id="wishlist-button"]'
        )

        print('Количество найденных кнопок:', len(buttons))

        for index, button in enumerate(buttons):
            print(
                f'Кнопка {index}:',
                'Видима:', button.is_displayed(),
                'Текст:', button.text
            )

        return self

    def removing_book_from_favorites(self):
        browser.element(
            '[data-testid="icon_favoritesThin"]'
        ).should(be.visible).click()

        browser.driver.refresh()
        return self

    def open_favorites_from_menu(self):
        browser.element(
            '[data-testid="tab__link"][href="/my-books/purchased/"]'
        ).should(be.visible).click()

        print(browser.driver.current_url)

        with open('/tmp/my_books_page.html', 'w', encoding='utf-8') as file:
            file.write(browser.driver.page_source)

        return self

    def book_must_be_added_to_favorites(self, book):
        self.open_favorites_from_menu()

        browser.element(
            f'[data-testid="art__wrapper"] a[href="/book/{book.url}"][data-testid="art__title"]'
        ).should(have.text(book.name))

        return self

    def book_must_be_removed_from_favorites(self, book):
        self.open_favorites_from_menu()

        browser.element(
            f'[data-testid="art__wrapper"] a[href="/book/{book.url}"][data-testid="art__title"]'
        ).should(be.absent)

        return self

    # ---------- Корзина ----------

    def adding_book_to_cart(self):
        browser.element(
            '[data-test-id="book__addToCartButton--desktop"]'
        ).should(be.visible).click()

        browser.driver.refresh()
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

        browser.driver.refresh()
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

    def cleanup_favorite(self, book):
        self.open(book)

        favorite_button = browser.element(
            '[data-testid="icon_favoritesThin"]'
        )

        if favorite_button.matching(be.visible):
            favorite_button.click()
            browser.driver.refresh()

        return self

book_page = BookPage()
