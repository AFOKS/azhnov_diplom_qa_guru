from appium.webdriver.common.appiumby import AppiumBy
from selene import be, browser


class AndroidMainPage:

    def selecting_application_language(self):
        language_title = browser.element((AppiumBy.ID, "ru.litres.android:id/title"))
        if language_title.with_(timeout=3).wait_until(be.visible):
            language_title.click()
            browser.element((AppiumBy.ID, "ru.litres.android:id/choosebutton")).click()
        return self

    def hiding_adult_content(self):
        disable_button = browser.element((AppiumBy.ID, "ru.litres.android:id/btnDisableAdultContent"))
        if disable_button.with_(timeout=3).wait_until(be.visible):
            disable_button.click()
            browser.element((AppiumBy.ID, "ru.litres.android:id/btnConfirmDisableAdultContent")).click()
        return self


main_page = AndroidMainPage()