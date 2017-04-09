from __future__ import print_function
from selenium import webdriver
import json

def getRatedFilms():
    "Opens Firefox for introduce the user and password and returns a dictionary with the rated films and series"
    films = []
    series = []
    login_url = "https://www.filmaffinity.com/en/login.php?rp=http%3A%2F%2Fwww.filmaffinity.com%2Fes%2Fmain.html"

    driver = webdriver.Firefox()
    driver.get(login_url)

    while(driver.current_url == login_url):
        pass

    driver.get("http://www.filmaffinity.com/en/myvotes.php")

    pages = driver.find_elements_by_class_name("pager")[0].find_elements_by_tag_name("a")
    numb_pages = int(pages[len(pages)-2].text)

    for films_page in range(1,numb_pages + 1):
        driver.get("http://www.filmaffinity.com/en/myvotes.php?p=" + str(films_page) + "&orderby=4")

        table = driver.find_elements_by_class_name("my-votes-movie-wrapper")
        for film in table:
            title = film.find_elements_by_class_name("mc-title")[0].text
            rate = film.find_elements_by_class_name("rate-movie-box")[0].get_attribute("data-user-rating")
            title = str(title.encode('utf8'))
            if '(TV)' in title or '(TV Series)' in title:
                series.append({ 'title':title[:-6], 'year':int(title[-6:][1:-1]), 'rate':int(rate)})
            else:
                films.append({ 'title':title[:-6], 'year':int(title[-6:][1:-1]), 'rate':int(rate)})

    driver.quit()
    return {"films":films , "series":series}

def getRatedFilmsJson():
    "Creates a file called filmsF.json in the current directory with the information of the getRatedFilms"
    filmsInJson = json.dumps(getRatedFilms())
    fileFilms = open("filmsF.json", "w+")
    fileFilms.write(filmsInJson)
    fileFilms.close()
