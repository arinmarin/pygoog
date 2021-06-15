from pages.base_page import MyPage
from pages.search_google_page import SearchAllGooglePage


class MainGooglePage(MyPage):
    url = 'https://www.google.com/'
    # Main search field name
    search_name = 'q'
    # Search run button xpath
    search_run_button_xpath = 'btnK'
    # Random Search button
    search_random_button_xpath = 'btnI'

    def get_driver(self, init_url=url):
        self.web_driver.get(init_url)

    def do_search(self, search_str):
        search = self.web_driver.find_element_by_name(self.search_name)
        search.send_keys(search_str)
        search.submit()
        return SearchAllGooglePage(driver=self.web_driver)
