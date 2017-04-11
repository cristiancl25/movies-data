import pandas as pd
def getGroupByRateCount(tmdbUser):
    "number of films grouped by rating"
    filmList = pd.DataFrame(tmdbUser.allRatedMovies)
    return filmList.groupby(['rating'])['title'].count()

def getGroupByYearCount(tmdbUser):
    "number of films grouped by year"
    filmList = pd.DataFrame(tmdbUser.allRatedMovies)
    if not "year" in filmList.columns:
        f = lambda s: int(s[:4])
        filmList['year'] = filmList.release_date.map(f)
    return filmList.groupby(['year'])['title'].count()

def getGroupByYearAvg(tmdbUser):
    "Average score of films grouped by year"
    filmList = pd.DataFrame(tmdbUser.allRatedMovies)
    if not "year" in filmList.columns:
        f = lambda s: int(s[:4])
        filmList['year'] = filmList.release_date.map(f)
    return filmList.groupby(['year'])['rating'].mean()
