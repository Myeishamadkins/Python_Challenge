import core
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


def get_zipcode(movie_helper, browser):
    while True:
        zip_code = input(
            "What zipcode would you like to search for?\nPress 'q' at anytime to exit the application.\n\n>>> "
        ).strip().lower()
        if zip_code == "q":
            quit()
        if movie_helper.check_valid_zip(zip_code):
            # initial zip code validiator to avoid broken requests (also faster to reject)

            print("\nSearching Fandango...\n", flush=True)
            if movie_helper.search_via_zip_code(zip_code, browser):
                # because func returns true or false, it can be used as a test
                # any side effects also occur when the function is run like search_results being changed
                print(
                    '-----------------------------------------------------------------'
                )
                print(
                    f"Ok there are {len(movie_helper.search_results['nearby_theaters'])} nearby:\n"
                )

                return
                # exits the while loop and function

            print("There are no theaters near that location")
        else:
            print("Not a valid zipcode")


def get_theater(movie_helper, browser):
    while True:
        nearby_theaters = '\n'.join(
            movie_helper.search_results['nearby_theaters'])
        print(nearby_theaters)
        theater = input(
            "\nWhat theater are you looking for?\n>>> ").lower().strip()
        if theater == "q":
            quit()
        print("Searching...\n")
        print(
            '-----------------------------------------------------------------'
        )
        if movie_helper.search_via_theater(theater, browser):
            print \
                (f"\nOk, you have selected {movie_helper.search_results['selected_theater']['theater_name']}\n")
            return
        print("That theater cannot be selected, please try again")


def get_date(movie_helper, browser):
    while True:
        print(
            '-----------------------------------------------------------------'
        )
        print(
            f"Here is the latest showing date for this theater: {movie_helper.search_results['latest_possible_date']}"
        )
        date = input('''Please enter a date in this format: "'year-month-day'" (eg. 1999-04-01) or
Just press enter to get a list of movie showings for today.\nWhat date are you looking for? \n\n>>> ''').strip()
        if date == "q":
            quit()
        if movie_helper.search_via_date(date, browser):
            print(
                "Ok, here are the movies and available showtimes for that date:\n"
            )
            return
        print(
            f"\n Sorry, either no movies are available on {date} or that is not a valid date. Please try again\n\n"
        )


def display_movies(movies_showtimes):
    # movie_showtimes is a list of dictionaries
    print('-----------------------------------------------------------------')
    for movie in movies_showtimes:
        showtimes = ", ".join(movie['available_showtimes'])
        print(f"{movie['movie_title']}: {showtimes}" + "\n")


def find_movietimes(movie_helper, browser):
    get_zipcode(movie_helper, browser)
    get_theater(movie_helper, browser)
    get_date(movie_helper, browser)
    display_movies(movie_helper.search_results['available_movies'])


def retry_results(movie_helper, browser):
    while True:
        print(
            '-----------------------------------------------------------------'
        )
        selection = input(
            '''Would you like to retry your results with different parameters or stop the application?
1: Restart the entire search
2: Restart the search with a different theater under the same zip code
3: Restart the search with a different date under the same theater
4: Leave the application\n\n>>> ''').strip()
        if selection == "1":
            find_movietimes(movie_helper, browser)
        if selection == "2":
            browser.get(
                f"https://www.fandango.com/{movie_helper.search_results['selected_zip_code']}_movietimes"
            )
            get_theater(movie_helper, browser)
            get_date(movie_helper, browser)
            display_movies(movie_helper.search_results['available_movies'])
        if selection == "3":
            get_date(movie_helper, browser)
            display_movies(movie_helper.search_results['available_movies'])
        if selection == "4":
            quit()
        else:
            print("Invalid input\n")


def main():
    options = Options()
    options.headless = True
    browser = Firefox(options=options)
    movie_helper = core.MovietimeCollector()
    # movie_helper is an object in the MovietimeCollector class
    find_movietimes(movie_helper, browser)
    retry_results(movie_helper, browser)


if __name__ == '__main__':
    main()
