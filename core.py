# import requests
# from bs4 import BeautifulSoup
from uszipcode import SearchEngine
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

search_results = {}


class MovietimeCollector:
    def __init__(self):
        self.search_results = {}
        self.zip_code_search = SearchEngine(simple_zipcode=True)

    def check_valid_zip(self, zip_code):
        zip_code_results = self.zip_code_search.by_zipcode(zip_code).to_dict()
        return bool(zip_code_results['zipcode'])

    def search_via_zip_code(self, zip_code: str, browser):
        browser.get(f"https://www.fandango.com/{zip_code}_movietimes")
        try:
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME,
                                                "fd-showtimes")))
            self.search_results['selected_zip_code'] = zip_code
            self.build_list_of_theaters(browser)
            return True
        except:
            return False

    def build_list_of_theaters(self, browser):
        list_of_nearby_theaters_elms = browser.find_elements_by_css_selector(
            "select.nearby-theaters__select option")
        self.search_results['nearby_theaters'] = [
            option.get_attribute("innerText")
            for option in list_of_nearby_theaters_elms
        ][1:]

    def search_via_theater(self, theater: str, browser):
        list_of_nearby_theaters_elms = browser.find_elements_by_css_selector(
            "select.nearby-theaters__select option")
        for option in list_of_nearby_theaters_elms:
            if theater == option.get_attribute("innerText").lower():
                self.search_results['selected_theater'] = dict(
                    theater_path=option.get_attribute("value"),
                    theater_name=option.get_attribute("innerText"))
                browser.get("https://www.fandango.com/" + self.
                            search_results['selected_theater']['theater_path'])
                self.build_list_of_dates(browser)
                return True
        return False

    def build_list_of_dates(self, browser):
        list_of_dates_elms = list(filter((
            lambda elm: not ("date-picker__date--no-showtime" in elm.get_attribute("class"))
        ),
        browser.find_elements_by_css_selector \
        (".date-picker__wrap li.date-picker__date")))

        self.search_results['latest_possible_date'] = list_of_dates_elms[
            -1].get_attribute("data-show-time-date")

    def search_via_date(self, date: str, browser):
        # import pdb
        # pdb.set_trace()
        if date:
            list_of_dates_elms = list(filter((
                lambda elm: not ("date-picker__date--no-showtime" in elm.get_attribute("class"))
            ),
            browser.find_elements_by_css_selector \
            (".date-picker__wrap li.date-picker__date")))

            for available_date in \
            [elm.get_attribute("data-show-time-date") \
            for elm in list_of_dates_elms]:
                if date == available_date:
                    self.search_results['selected_date'] = date
                    self.build_movie_url(browser)
                    self.build_list_of_movies(browser)
                    return True
            return False
        else:
            self.build_list_of_movies(browser)
            return True

    def build_movie_url(self, browser):
        movie_date = self.search_results['selected_date']
        # formats the date to so it can be passed as a url
        theater_path = self.search_results['selected_theater'][
            'theater_path'].split("?")[0]
        #gets the part of the theater path that specifies the name of the theater
        browser.get(
            f"https://www.fandango.com{theater_path}?date={movie_date}")
        #fills an https request to the correct theater on the correct date

    def build_list_of_movies(self, browser):
        list_of_movies_elms = browser.find_elements_by_css_selector(
            "li.fd-theater .fd-movie")
        self.search_results['available_movies'] = []
        for movie_elm in list_of_movies_elms:
            movie = {}
            movie['movie_title'] = movie_elm.find_element_by_css_selector(
                ".fd-movie__title").get_attribute('innerText')
            movie['available_showtimes'] = [
                date.get_attribute("innerText")
                for date in movie_elm.find_elements_by_css_selector(
                    "ol.fd-movie__btn-list .showtime-btn--available")
            ]
            self.search_results['available_movies'].append(movie)

    def test_full_search(self):
        browser = Firefox()
        self.search_via_zip_code("38655", browser)
        self.search_via_theater("Malco Oxford Commons Cinema Grill", browser)
        self.search_via_date("2018-11-14", browser)
        self.search_via_movie()

        print(self.search_results)
