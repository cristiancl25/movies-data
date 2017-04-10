import urllib2 as url
import urllib
import json

def exportToJson(data, nameFile):
    "Creates a file (in Json format) called nameFile in the current directory with the information of the data"
    filmsInJson = json.dumps(data)
    fileFilms = open(nameFile + ".json", "w+")
    fileFilms.write(filmsInJson)
    fileFilms.close()

def stringToUrl(s):
    "Replace the spaces in a string. The parameters in the TheMovieDB api require this."
    return s.replace(" ", "%20")

class TheMovieDBException(Exception):
    def __init(self, message):
        super(TheMovieDBException, self).__init__(message)

class TheMovieDBUser():
    def __init__(self, api_key, user, password):
        self.__API_KEY=api_key
        self.__USER_NAME=user
        self.__PASSWORD=password
        self.__autenticateUser__()

    def __autenticateUser__(self):
        "Autenticates the user by username and password in TheMovieDB"
        requestToken = url.urlopen("https://api.themoviedb.org/3/authentication/token/new?api_key=" + self.__API_KEY)
        if requestToken.getcode() != 200:
            error = json.loads(requestToken.read()).get("status_message")
            raise TheMovieDBException(error)

        self.__token = json.loads(requestToken.read()).get("request_token")
        confirmToken = url.urlopen("https://api.themoviedb.org/3/authentication/token/validate_with_login?api_key=" + self.__API_KEY + "&username=" + self.__USER_NAME + "&password=" + self.__PASSWORD + "&request_token=" + self.__token)
        createSession = url.urlopen("https://api.themoviedb.org/3/authentication/session/new?api_key=" + self.__API_KEY + "&request_token=" + self.__token)
        self.__sessionId = json.loads(createSession.read()).get("session_id")

    def rateMovie(self, movieId, score):
        "Rate a movie in TheMovieDB"
        data = urllib.urlencode({"value":score})
        return json.loads(url.urlopen("https://api.themoviedb.org/3/movie/" + str(movieId) + "/rating?api_key=" + self.__API_KEY + "&session_id=" + self.__sessionId, data).read())

    def getRatedMovies(self, credits=False):
        "Returns a dictionary with all the rated movies by the user in TheMovieDB"
        films = json.loads(url.urlopen("https://api.themoviedb.org/3/account/{account_id}/rated/movies?api_key=" + self.__API_KEY + "&language=en-US&session_id=" + self.__sessionId + "&sort_by=created_at.asc").read())
        if credits:
            for film in films.get("results"):
                credits = json.loads(url.urlopen("https://api.themoviedb.org/3/movie/" + str(film.get("id")) + "/credits?api_key=" + self.__API_KEY).read())
                film["cast"] = credits.get("cast")
                film["crew"] = credits.get("crew")
        self.ratedMovies = films
        return films

    def getMovieCredits(self, movieId):
        "Returns a dictionary with the cast and crew of a movie"
        return json.loads(url.urlopen("https://api.themoviedb.org/3/movie/" + str(movieId) + "/credits?api_key=" + self.__API_KEY).read())

    def searchMovieById(self, movieId):
        "Returns a dictionary with the information about a movie"
        return json.loads(url.urlopen("https://api.themoviedb.org/3/movie/" + str(movieId) + "?api_key=" + self.__API_KEY + "&language=en-US").read())

    def searchMovieByName(self, name, year=0):
        "Returns a dictionary with the information about a movie. IMPORTANT: If the name contains spaces put %20 in its place"
        if year == 0:
            return json.loads(url.urlopen("https://api.themoviedb.org/3/search/movie?api_key=" + self.__API_KEY + "&language=en-US&query=" + name + "&page=1&include_adult=false").read())
        else:
            return json.loads(url.urlopen("https://api.themoviedb.org/3/search/movie?api_key=" + self.__API_KEY + "&language=en-US&query=" + name + "&page=1&include_adult=false&year=" + str(year)).read())

    def getSimilarMovies(self, movieId):
        return json.loads(url.urlopen("https://api.themoviedb.org/3/movie/" + str(movieId) + "/similar?api_key=" + self.__API_KEY + "&language=en-US&page=1").read())

    def getRecommendedMovies(self, movieId):
        return json.loads(url.urlopen("https://api.themoviedb.org/3/movie/" + str(movieId) + "/recommendations?api_key=" + self.__API_KEY + "&language=en-US&page=1").read())

    def getPopularMovies(self):
        return json.loads(url.urlopen("https://api.themoviedb.org/3/movie/popular?api_key=" + self.__API_KEY + "&language=en-US&page=1").read())

    def getTopRatedMovies(self):
        return json.loads(url.urlopen("https://api.themoviedb.org/3/movie/top_rated?api_key=" + self.__API_KEY + "&language=en-US&page=1").read())

    def getUpcomingMovies(self):
        return json.loads(url.urlopen("https://api.themoviedb.org/3/movie/upcoming?api_key=" + self.__API_KEY + "&language=en-US&page=1").read())

    def getLatestMovie(self):
        "Get the most newly created movie on The MovieDB"
        return json.loads(url.urlopen("https://api.themoviedb.org/3/movie/latest?api_key=" + self.__API_KEY + "&language=en-US").read())

    def searchPeopleByID(self, personId):
        "Returns a dictionary with the movies in which he participated or directed"
        return json.loads(url.urlopen("https://api.themoviedb.org/3/person/" + str(personId) + "/movie_credits?api_key=" + self.__API_KEY + "&language=en-US").read())

    def searchPeopleByName(self, name):
        "Returns a dictionary with the information about the person searched. IMPORTANT: If the name contains spaces put %20 in its place"
        return json.loads(url.urlopen("https://api.themoviedb.org/3/search/person?api_key=" + self.__API_KEY + "&language=en-US&query=" + name + "&page=1&include_adult=false").read())
