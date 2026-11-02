from selene import browser, be, by, have, command
from selene.core.exceptions import TimeoutException

class MainPage:
    def open(self):
        browser.open("")
        return self

    def accept_cookies(self):
        button = browser.element(by.text('Принять'))
        try:
            button.with_(timeout=3).should(be.visible)
            button.click()
        except TimeoutException:
            pass  # баннера нет, это нормально
        return self

    def filling_authorization_form(self, user):
        browser.element(
            '[data-testid="tab__link"][href="/auth/login/"]'
        ).should(be.visible).click()

        browser.element(
            '[data-testid="auth__input--enterEmailOrLogin"]'
        ).should(be.visible).type(user.email)

        browser.element(
            '[data-testid="auth__button--continue"]'
        ).should(be.visible).click()

        browser.element(
            '[data-testid="auth__input--enterPassword"]'
        ).should(be.visible).type(user.password)

        browser.element(
            '[data-testid="auth__button--enter"]'
        ).should(be.visible).click()

        return self

    def user_must_be_authorized(self, user):
        browser.element(
            '[data-testid="header__profile-button"]'
        ).should(be.visible)

        browser.open("/me/profile/")

        browser.element(
            '[data-testid="profile__userNameMain"]'
        ).should(be.visible).should(have.text(user.email))

        return self

    def filling_unregistered_user_email(self, user):
        browser.element(
            '[data-testid="tab__link"][href="/auth/login/"]'
        ).should(be.visible).click()

        browser.element(
            '[data-testid="auth__input--enterEmailOrLogin"]'
        ).should(be.visible).type(user.email)

        browser.element(
            '[data-testid="auth__button--continue"]'
        ).should(be.visible).click()

        return self

    def user_must_not_be_authorized(self, user):
        browser.element(
            '[data-testid="auth__title"]'
        ).should(be.visible).should(
            have.text('Создать профиль')
        )

        browser.element(
            '[class*="emailRegistrationContainer__freeEmailMessage"]'
        ).should(be.visible).should(
            have.text('Адрес свободен для регистрации')
        )
        browser.element(
            'button[type="button"]'
        ).should(be.visible).should(
            have.text('Продолжить')
        )

        return self

    def user_must_see_invalid_credentials_error(self):
        browser.element(
            '[data-testid="textbox--input__error"]'
        ).should(be.visible).should(
            have.text('Неверное сочетание логина и пароля')
        )

        return self

    def search_book_by_title(self, book):
        browser.element(
            '[data-testid="search__input"]'
        ).should(be.visible).type(book.name)

        browser.element(
            '[data-testid="search__button"]'
        ).should(be.visible).click()

        browser.element(f'a[aria-label="{book.name}"]').should(be.present)
        return self

    def open_book_from_search(self, book):
        path = book.url.strip('/')
        card = browser.element(f'a[href*="/book/{path}"]')
        card.should(be.present)
        card.perform(command.js.click)
        browser.should(have.url_containing(f'/book/{path}'))
        return self

    def book_with_specified_title_must_be_found(self):
        browser.element(
            'a[aria-label="Ведьмак"]'
        ).should(be.visible)

        return self

    def search_book_by_author(self, book):
        browser.element(
            '[data-testid="search__input"]'
        ).should(be.visible).type(book.author)

        browser.element(
            '[data-testid="search__button"]'
        ).should(be.visible).click()

        return self

    def select_authors_tab(self):
        browser.all(
            '[data-testid="navigation__tabItem__label"]'
        ).element_by(
            have.text('Авторы')
        ).should(be.visible).click()

        return self

    def author_with_specified_name_must_be_found(self):
        browser.element(
            '[data-testid="search__personName"]'
            '[href="/author/dzhordzh-r-r-martin-45006/"]'
        ).should(be.visible)

        return self

main_page = MainPage()
