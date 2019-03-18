from core import *
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestZipCode:
    def setup_method(self):
        self.browser = Firefox()

    def teardown_method(self):
        self.browser.quit()

    def test_invalid_fandango_zip(self):
        MovietimeCollector().search_via_zip_code("386", self.browser)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME,
                                            "fd-showtimes__error-msg")))

        MovietimeCollector().search_via_zip_code('555555', self.browser)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME,
                                                 'date-picker__error')))

    def test_valid_fandango_zip(self):
        MovietimeCollector().search_via_zip_code('12345', self.browser)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME,
                                                 'nearby-theaters__select')))

        MovietimeCollector().search_via_zip_code("38655", self.browser)
        WebDriverWait(self.browser, 10).until_not(
            EC.presence_of_element_located((By.CLASS_NAME,
                                            "fd-showtimes__error-msg")))

    def test_valid_library_zip(self):
        MovietimeCollector().search_via_zip_code('38655', self.browser)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME,
                                                 'nearby-theaters__select')))

    def test_invalid_library_zip(self):
        MovietimeCollector().search_via_zip_code('1234', self.browser)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME,
                                                 'fd-showtimes__error-msg')))

    def test_valid_library_zip_valid_fandango_zip(self):
        MovietimeCollector().search_via_zip_code('5555', self.browser)
        WebDriverWait(self.browser, 10).until_not(
            EC.presence_of_all_elements_located((By.CLASS_NAME,
                                                 'nearby-theaters__select')))


class TestUsZipCode:
    def setup_method(self):
        self.zip_code_collector = MovietimeCollector().check_valid_zip
        # this variable references the check_valid_zip function
        # so it can be called with an argument

    def test_valid_library_zip(self):
        assert self.zip_code_collector("38655")
        # Here's an example

    def test_check_valid_zip(self):
        assert self.zip_code_collector('55555')


class TestCheckTheater:
    def test_valid_theater_name(self):
        list_of_nearby_theaters_elms = '''<select class="nearby-theaters__select">
        <option>Malco Oxford Studio Cinema</option>
        <option>Malco Oxford Commons Cinema Grill</option>
        </select>'''

    def test_invalid_theater_name(self):
        list_of_nearby_theaters_elms = '''<select class="nearby-theaters__select">
        <option>Malco Oxford Studio Cinema</option>
        <option>Malco Oxford Commons Cinema Grill</option>
        <option>Myeisha was here!</option>
        </select>'''


class TestCheckDates:
    def test_valid_show_date(self):
        list_of_dates_elms = '''<div class="date-picker__wrap">
        <li class="date-picker__date">2018-11-15</li>
        <li class="date-picker__date">2018-11-17</li>
        <li class="date-picker__date">2018-11-22</li>
        </div>'''

    def test_invalid_show_date(self):
        list_of_dates_elms = '''<div class="date-picker__wrap">
        <li class="date-picker__date">2018-11-15</li>
        <li class="date-picker__date">2018-11-17</li>
        <li class="date-picker__date">1998-10-28</li>
        </div>'''


class TestCheckMovies:
    def test_valid_movie_option(self):
        list_of_movies_elms = '''<li class="fd-theater">
        <li class="fd-movie">Dr. Seuss' The Grinch (2018)</li>
        <li class="fd-movie">Bohemian Rhapsody</li>
        </li>'''

    def test_invalid_movie_option(self):
        list_of_movies_elms = '''<li class="fd-theater">
        <li class="fd-movie">Dr. Seuss' The Grinch (2018)</li>
        <li class="fd-movie">Bohemian Rhapsody</li>
        <li class="fd-movie">Myeisha was here!</li>
        </li>'''


# def test_check_valid_zip():
#     #should all return True
#     zip_code = 38655
#     assert check_valid_zip(zip_code) == True

#     zip_code = 55555
#     assert check_valid_zip(zip_code) == True

#     zip_code = 12345
#     assert check_valid_zip(zip_code) == True

# def test_check_invalid_zip():
#     #should all return False
#     zip_code = 555555
#     assert check_valid_zip(zip_code) == False

#     zip_code = 38
#     assert check_valid_zip(zip_code) == False

#     zip_code = 123
#     assert check_valid_zip(zip_code) == False

# def test_search_via_zip_code():
#     # should all return False
#     code = 123
#     assert search_via_zip_code(code) == False

#     code = 227
#     assert search_via_zip_code(code) == False

#     code = 555555
#     assert check_valid_zip(code) == False

# # def test_search_via_zip_code():
# #     # should all return True
# #     code = 38655
# #     assert search_via_zip_code(code) == False

# def test_search_finds_first_option():
#     html = '''<select class="nearby-theaters__select">
#         <option>Malco Oxford Studio Cinema</option>
#         <option>Malco Oxford Commons Cinema Grill</option>
#         </select>'''

#     soup = BeautifulSoup(html, 'html.parser')
#     option = 'Malco Oxford Studio Cinema'
#     assert search_via_theater(option, soup)

# def test_non_present_theater():
#     html = '''<select class="nearby-theaters__select">
#         <option>Malco Oxford Studio Cinema</option>
#         <option>Malco Oxford Commons Cinema Grill</option>
#         </select>'''

#     soup = BeautifulSoup(html, 'html.parser')
#     option = 'nates theater'
#     assert not search_via_theater(option, soup)

# def test_find_last_theater():
#     html = '''<select class="nearby-theaters__select">
#         <option>Malco Oxford Studio Cinema</option>
#         <option>Malco Oxford Commons Cinema Grill</option>
#         <option>Myeisha was here</option>
#         </select>'''

#     soup = BeautifulSoup(html, 'html.parser')
#     option = 'Myeisha was here'
#     assert search_via_theater(option, soup)

# def test_find_middle_theater():
#     html = '''<select class="nearby-theaters__select">
#         <option>Malco Oxford Studio Cinema</option>
#         <option>Malco Oxford Commons Cinema Grill</option>
#         <option>Myeisha was here</option>
#         </select>'''

#     soup = BeautifulSoup(html, 'html.parser')
#     option = 'Malco Oxford Commons Cinema Grill'
#     assert search_via_theater(option, soup)
