from bs4 import BeautifulSoup
import requests

# ****** FUNCTION TO GET MOVIE POSTER IMAGES ***** #
def getInfo(movieName,theatre):

	now_showing_url = 'https://www.harkins.com/movies/now-showing'
	now_showing_amc = 'https://www.amctheatres.com/movies'

	r = requests.get(now_showing_url)
	amcR = requests.get(now_showing_amc)

	soup = BeautifulSoup(r.text, "html.parser")
	amcSoup = BeautifulSoup(amcR.text, "html.parser")

	all_movies = soup.find_all('li', class_="posters-container") # find all movies now playing
	amc_movies = amcSoup.find_all('div', class_="Slide")

	movies = {}

	for item in all_movies:
		movie_poster = item.find("img", {"class": "block-image"})
		movie_poster = movie_poster['src']

		movie_name = item.find("h2", {"class":None})
		movie_name = movie_name.text.replace('\n', "").strip()

		movie_link = item.find("a").get('href')
		movie_link = "http://harkins.com" + movie_link

		scrapeDetails(movie_link, "harkins")

		if movieName not in movie_name:
			continue
		else:
			if 'harkins' in theatre:
				movies[movie_name] = [movie_poster,movie_link, "Harkins"]


	for movie in amc_movies:
		poster = movie.find("img", {"class":None})
		poster = poster['src']

		name = movie.find("h3", {"class":None})
		name = name.text.replace('\n', "").strip()

		link = movie.find("a").get("href")
		link = "http://amctheatres.com" + link

		scrapeDetails(link, "amc")

		if movieName not in name:
			continue
		else:
			if 'amc' in theatre:
				movies[name] = [poster,link,"AMC Theatres"]

	return movies

def scrapeDetails(link, theatre):
	request = requests.get(link)

	soup = BeautifulSoup(request.text, "html.parser")
	time = ""

	if theatre == "amc":
		time = soup.find("span", itemprop="duration")
	else:
		time = soup.find("time", datetime="")
		time = time.get_text()

	return time

def getLatestReleases():
	base_url = "https://www.fandango.com/movies-in-theaters"
	request = requests.get(base_url)
	soup = BeautifulSoup(request.text, "html.parser")

	movies = soup.find_all('li', class_="poster-card")

	movieList = {}

	index = 0

	for item in movies:
		movieTitle = item.find("span", {"class":"heading-style-1"})
		movieTitle = movieTitle.text.replace('\n', "").strip()

		movieImage = item.find("img", {"class":"poster-card--img"})
		movieImage = movieImage["src"]

		movieUrl = item.find("a").get("href")
		movieUrl = "https://www.fandango.com/" + movieUrl

		if(index < 8):
			movieList[movieTitle] = [movieTitle,movieImage,movieUrl]
			index += 1

	return movieList

if __name__ == "__main__":
	print(scrape())
