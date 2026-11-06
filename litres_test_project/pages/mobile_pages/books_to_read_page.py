from appium.webdriver.common.appiumby import AppiumBy
from selene import be, browser, have, query

SEARCH_BOOK_TITLE = 'The Witcher'
NON_EXISTENT_BOOK_TITLE = 'sdflksd'


class AndroidSearchBookPage:

    def searching_book(self):
        self._search(SEARCH_BOOK_TITLE)
        return self

    def book_must_be_found(self):
        browser.all((AppiumBy.ID, 'ru.litres.android:id/clArtLayout')).should(have.size_greater_than(0))
        self._first_book_name().should(have.text(SEARCH_BOOK_TITLE))
        return self

    def first_book_title(self):
        return self._first_book_name().should(be.visible).get(query.text)

    def searching_non_existent_book(self):
        self._search(NON_EXISTENT_BOOK_TITLE)
        return self

    def book_must_not_be_found(self):
        browser.element((AppiumBy.ID, "ru.litres.android:id/empty_view")).should(be.visible)
        browser.element((AppiumBy.ID, "ru.litres.android:id/title")).should(have.text('No matches found'))
        (browser.element((AppiumBy.ID, "ru.litres.android:id/tv_books_search_empty_message"))
         .should(have.text('Make sure you entered the correct search query')))
        return self

    def choosing_book(self):
        browser.all((AppiumBy.ID, "ru.litres.android:id/clArtLayout")).first.click()
        return self

    @staticmethod
    def _first_book_name():
        return browser.all((AppiumBy.ID, "ru.litres.android:id/textViewBookName")).first

    @staticmethod
    def _search(text):
        browser.element((AppiumBy.ID, "ru.litres.android:id/search")).click()
        browser.element((AppiumBy.ID, "ru.litres.android:id/et_search_query")).type(text)
        browser.element((AppiumBy.ID, "ru.litres.android:id/textViewItemSearchSuggestText")).should(be.visible).click()


book_search_page = AndroidSearchBookPage()