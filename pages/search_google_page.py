from pages.base_page import MyPage


class SearchGooglePage(MyPage):
    # Head_elements xpath
    head_element_xpath = "//div[@class='hdtb-mitem']//a[text()='{}']"
    aria_labels_xpath = "//a[@aria-label='{}']"

    def click_head_element(self, head_element_name):
        pictures = self.web_driver.find_element_by_xpath(self.head_element_xpath.format(head_element_name))
        pictures.click()
        return SearchPicturesGooglePage(driver=self.web_driver)

    def go_href_for_element(self, element):
        self.web_driver.get(element.get_attribute('href'))

    def get_preferences_href(self, label_name):
        hd_selector = self.web_driver.find_element_by_xpath(self.aria_labels_xpath.format(label_name))
        self.go_href_for_element(hd_selector)


class SearchAllGooglePage(SearchGooglePage):
    # Search response with play google
    search_answers_xpath = "//div[@id='rso']//a[contains(@href, 'play.google.com')]"

    def get_search_play_response_items(self):
        return self.web_driver.find_elements_by_xpath(self.search_answers_xpath)


class SearchPicturesGooglePage(SearchGooglePage):
    # Preferences xpath
    preferences_xpath = "//div[@role='navigation']//*[local-name() = 'svg']"
    # Search result items xpath
    search_result_items_xpath = "//div[@role='listitem']//a[@rel='noopener']"

    def click_preference(self):
        preference = self.web_driver.find_elements_by_xpath(self.preferences_xpath)[0]
        preference.click()

    def get_result_items(self):
        return self.web_driver.find_elements_by_xpath(self.search_result_items_xpath)
