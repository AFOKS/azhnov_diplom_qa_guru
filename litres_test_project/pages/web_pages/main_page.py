from selene import browser, be, by, have, command


class MainPage:
    def open(self):
        browser.open("")
        return self

    def accept_cookies(self):
        button = browser.element(by.text('Принять'))
        if button.matching(be.visible):
            button.click()
        return self

    def filling_authorization_form(self, user):
        # Открываем форму входа
        browser.element(
            '[data-testid="tab__link"][href="/auth/login/"]'
        ).should(be.visible).click()

        # Вводим email зарегистрированного пользователя
        browser.element(
            '[data-testid="auth__input--enterEmailOrLogin"]'
        ).should(be.visible).type(user.email)

        # Нажимаем «Продолжить»
        browser.element(
            '[data-testid="auth__button--continue"]'
        ).should(be.visible).click()

        # Ожидаем поле пароля
        browser.element(
            '[data-testid="auth__input--enterPassword"]'
        ).should(be.visible).type(user.password)

        # Подтверждаем вход
        browser.element(
            '[data-testid="auth__button--enter"]'
        ).should(be.visible).click()

        return self

    def user_must_be_authorized(self, user):
        # Проверяем, что после входа появилась кнопка профиля
        browser.element(
            '[data-testid="header__profile-button"]'
        ).should(be.visible)

        # Открываем актуальную страницу профиля
        browser.open("/me/profile/")

        # Проверяем email авторизованного пользователя
        browser.element(
            '[data-testid="profile__userNameMain"]'
        ).should(be.visible).should(have.text(user.email))

        return self

    def filling_unregistered_user_email(self, user):
        # Открываем форму входа
        browser.element(
            '[data-testid="tab__link"][href="/auth/login/"]'
        ).should(be.visible).click()

        # Вводим незарегистрированный email
        browser.element(
            '[data-testid="auth__input--enterEmailOrLogin"]'
        ).should(be.visible).type(user.email)

        # Продолжаем, чтобы сайт проверил email
        browser.element(
            '[data-testid="auth__button--continue"]'
        ).should(be.visible).click()

        return self

    def user_must_not_be_authorized(self, user):
        # Проверяем окно создания профиля
        browser.element(
            '[data-testid="auth__title"]'
        ).should(be.visible).should(
            have.text('Создать профиль')
        )

        # Проверяем сообщение о доступности email
        browser.element(
            '[class*="emailRegistrationContainer__freeEmailMessage"]'
        ).should(be.visible).should(
            have.text('Адрес свободен для регистрации')
        )

        # Проверяем кнопку продолжения регистрации
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

        # ждём выдачу по признаку, который работает в тесте поиска
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
