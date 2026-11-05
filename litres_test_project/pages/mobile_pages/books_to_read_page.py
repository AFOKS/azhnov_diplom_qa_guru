from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, be, have


class AndroidSearchBookPage:

    def searching_book(self):
        self._search('Witcher')
        return self

    def book_must_be_found(self):
        results = browser.all((AppiumBy.ID, 'ru.litres.android:id/clArtLayout'))
        results.should(have.size_greater_than(0))
        (browser.all((AppiumBy.ID, "ru.litres.android:id/textViewBookName")).first
         .should(have.text('Witcher')))
        return self

    def searching_non_existent_book(self):
        self._search('sdflksd')
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
    def _search(query):
        browser.element((AppiumBy.ID, "ru.litres.android:id/search")).click()
        browser.element((AppiumBy.ID, "ru.litres.android:id/et_search_query")).type(query)
        suggestion = browser.element((AppiumBy.ID, "ru.litres.android:id/textViewItemSearchSuggestText"))
        suggestion.should(have.text(query)).click()


book_search_page = AndroidSearchBookPage()