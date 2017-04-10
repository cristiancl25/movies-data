import TheMovieDBUser as user
import FilmaffinityData as ffd

def importMoviestoTMDB(TMDBUser, fileJson=None):
    "imports the data generated by FilmaffinityData.py to TheMovieDB. fileJson is a file generated by getRatedFilmsJson(), if is None calls to getRatedFilms()"
    duplicates = []
    empty = []


    if fileJson == None:
        data = ffd.getRatedFilms()
    else:
        archivo = open(fileJson + ".json", "r")
        data = json.loads(archivo.read())
        archivo.close()

    for film in data.get("films"):
        name = str(film.get("title").encode('utf8'))
        year = film.get("year")
        rate = film.get("rate")
        print("################################################################################")
        print(name)

        movies = TMDBUser.searchMovieByName(user.stringToUrl(name), year)
        movies = movies.get("results")
        if len(movies) > 1: 
            #if the search return more than one movie, ask to the user what is the correct
            i=0
            for movie in movies:
                print(str(i) + "-----------------------------")
                i = i+1
                print(movie)
            print("Select the correct movie->")
            a = int(raw_input())
            print(movies[a])
            TMDBUser.rateMovie(movies[a].get("id"),rate)
            duplicates.append({"film":film, "search":movies})
        elif len(movies) < 1:
            #If no one movie is found insert the searched title in a error file (json)
            empty.append({"film":film, "search":movies})
        else:
            #if find one movie import it in TheMovieDB
            TMDBUser.rateMovie(movies[0].get("id"),rate)

    #ImportErrors.json contains duplicate films and those that were not found
    user.exportToJson({"duplicates":duplicates, "empty":empty}, "ImportErrors")
