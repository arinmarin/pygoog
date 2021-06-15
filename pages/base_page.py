from selenium.webdriver.chrome.webdriver import WebDriver


class MyPage:
    def __init__(self, driver: WebDriver):
        self.web_driver = driver

    def scroll_down(self):
        self.web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
