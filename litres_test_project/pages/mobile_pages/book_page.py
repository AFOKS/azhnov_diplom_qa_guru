from appium.webdriver.common.appiumby import AppiumBy
from selene import be, browser, have


class AndroidBookPage:

    def adding_book_to_saved(self):
        browser.element((AppiumBy.ID, "ru.litres.android:id/imageViewBookCardFavourite")).should(be.visible).click()
        return self

    def go_to_saved_tab(self):
        browser.element((AppiumBy.ID, "ru.litres.android:id/nav_my_audiobooks")).should(be.visible).click()
        return self

    def open_saved_for_later(self):
        (browser.all((AppiumBy.ID, "ru.litres.android:id/textViewBookSectionTitle"))
         .element_by(have.exact_text("Saved for Later")).click())
        return self

    def book_must_be_added_to_saved(self, title):
        browser.element((AppiumBy.XPATH, f'//*[@text="{title}"]')).should(be.visible)
        return self

    def removing_book_from_saved(self, title):
        browser.element((AppiumBy.XPATH, f'//*[@text="{title}"]')).click()
        browser.element((AppiumBy.ID, "ru.litres.android:id/imageViewBookCardFavourite")).click()
        return self

    def book_must_be_removed_from_saved(self):
        browser.element((AppiumBy.ID, "ru.litres.android:id/empty_view")).should(be.visible)
        return self


book_page = AndroidBookPage()