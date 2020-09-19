from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import requests


class MovieTheater(object):

    def __init__(self, baseUrl, movieListUrl, movieContainer, movieContainerClass, moviePosterClass, movieTitleElement):
        self.baseUrl = baseUrl
        self.movieListUrl = movieListUrl
        self.movieContainer = movieContainer
        self.movieContainerClass = movieContainerClass
        self.moviePosterClass = moviePosterClass
        self.movieTitleElement = movieTitleElement

    def getWebsiteHtml(self, websiteUrl=None):
        if websiteUrl is None:
            websiteUrl = self.movieListUrl

        request = requests.get(websiteUrl)
        websiteHtml = BeautifulSoup(request.text, "html.parser")

        return websiteHtml


class Harkins(MovieTheater):

    def getTheaterName(self):
        return "Harkins"


class Amc(MovieTheater):

    def getTheaterName(self):
        return "AMC"


def getInfo(movieName, theatre):
    moviesFound = {}

    harkins = Harkins("https://www.harkins.com", "https://www.harkins.com/movies/now-showing",
                      "li", "posters-container", "block-image", "h2")
    amc = Amc("https://www.amctheatres.com",
              "https://www.amctheatres.com/movies", "div", "Slide", None, "h3")

    if(theatre == "HARKINS"):
        moviesFound = scrapeNowShowing(harkins, movieName)

    elif(theatre == "AMC"):
        moviesFound = scrapeNowShowing(amc, movieName)

    elif(theatre == "H_AMC"):
        harkinsMovies = scrapeNowShowing(harkins, movieName)
        amcMovies = scrapeNowShowing(amc, movieName)

        moviesFound = Merge(harkinsMovies, amcMovies)

    return moviesFound


def scrapeNowShowing(movieTheaterClass, movieInput):
    html = movieTheaterClass.getWebsiteHtml()

    movieContainer = movieTheaterClass.movieContainer
    movieContainerClass = movieTheaterClass.movieContainerClass

    allMovies = html.find_all(movieContainer, class_=movieContainerClass)

    matchingMoviesFound = {}

    for container in allMovies:
        movie_poster = container.find(
            "img", {"class": movieTheaterClass.moviePosterClass})
        movie_poster = movie_poster['src']

        movie_name = container.find(
            movieTheaterClass.movieTitleElement, {"class": None})
        movie_name = movie_name.text.replace('\n', "").strip()

        movie_link = container.find("a").get('href')
        movie_link = movieTheaterClass.baseUrl + movie_link

        ratio = fuzz.ratio(movieInput, movie_name.lower())

        if ratio > 70 or movieInput == '' or movieInput in movie_name:
            matchingMoviesFound[movie_name] = [movie_poster,
                                               movie_link, movieTheaterClass.getTheaterName()]

    return matchingMoviesFound


def Merge(dict1, dict2):
    combinedDictionary = {**dict1, **dict2}
    return combinedDictionary
