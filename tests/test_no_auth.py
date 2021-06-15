import re

import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from pages.main_google_page import MainGooglePage


@pytest.fixture(scope='function')
def driver(request):
    # Устанавливаем опции запуска для мобильной версии.
    mobile_emulation = {
        "deviceMetrics": {"width": 400, "height": 702},
        "userAgent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 "
                     "(KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36"
    }
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = webdriver.Chrome(options=chrome_options)

    def fin():
        driver.close()  # close driver after test
    request.addfinalizer(fin)

    return driver


@pytest.fixture(scope='function')
def ivi_search(driver):
    main_page = MainGooglePage(driver)
    main_page.get_driver()
    return main_page.do_search('ivi')


class TestGoogleSearch:
    def test_picture_search(self, ivi_search):
        """
        1. Неавторизованный пользователь заходит в https://www.google.com/
        2. ищет ivi
        3. переходит в картинки
        4. выбирает большие
        5. убеждается, что не менее 3 картинок в выдаче ведут на сайт ivi.ru
        """
        pictures_page = ivi_search.click_head_element('Картинки')
        pictures_page.click_preference()
        pictures_page.get_preferences_href('HD')

        big_pictures = pictures_page.get_result_items()
        ref_count = 0
        for pic in big_pictures:
            if pic.get_attribute('href').startswith('https://www.ivi.ru'):
                ref_count += 1
                if ref_count == 3:
                    return
        assert False, "big pictures count less than 3."

    def test_playmarket(self, ivi_search):
        """
        неавторизованный пользователь заходит в https://www.google.com/
        ищет ivi
        на первых 5 страницах находит ссылки на приложение ivi в play.google.com
        убеждается, что рейтинг приложения на кратком контенте страницы совпадает с рейтингом при переходе
        """
        rate_xpath = "//div[@id='rso']//a[contains(@href, 'play.google.com')]//div[@style]/div/span[1]"
        rate_play_xpath = "(//div[contains(@aria-label, 'Средняя оценка')])[1]"

        def scroll_down_and_get(name):
            search_page.scroll_down()
            search_page.get_preferences_href(name)

        def check_elements(elements):
            for elem in elements:
                rate_first = float(search_page.web_driver.find_element_by_xpath(rate_xpath).get_attribute('innerHTML'))
                search_page.go_href_for_element(elem)
                rate_second = search_page.web_driver.find_element_by_xpath(rate_play_xpath).get_attribute('aria-label')
                rate_second = float(re.search(r'Средняя оценка: (.*) из 5', rate_second).group(1).replace(',', '.'))
                assert rate_first == rate_second, 'ratings don`t matches'
                search_page.web_driver.back()

        search_page = ivi_search
        elements = search_page.get_search_play_response_items()
        check_elements(elements)
        scroll_down_and_get('Другие результаты')
        for _ in range(3):
            check_elements(elements)
            scroll_down_and_get('Следующая страница')

    def test_wiki(self, ivi_search):
        """
        неавторизованный пользователь заходит в https://www.google.com/
        ищет ivi
        на первых 5 страницах находит ссылку на статью в wikipedia об ivi
        убеждается, что в статье есть ссылка на официальный сайт ivi.ru
        """
        wiki_xpath = "(//a[contains(@href, 'wikipedia')])[1]"
        ivi_xpath = "(//*[contains(@href, 'http://www.ivi.ru')])[1]"

        search_page = ivi_search
        wiki_href = search_page.web_driver.find_element_by_xpath(wiki_xpath).get_attribute('href')
        search_page.web_driver.get(wiki_href)
        try:
            search_page.web_driver.find_element_by_xpath(ivi_xpath)
        except NoSuchElementException:
            assert False, 'ivi reference not found'
