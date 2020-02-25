from bs4 import BeautifulSoup
import requests

# ****** FUNCTION TO GET MOVIE POSTER IMAGES ***** #

def getInfo(movieName,theatre):
	moviesFound = {}

	if(theatre[0] == "harkins"):
		moviesFound =  scrapeNowShowing(movieName, "https://www.harkins.com", "https://www.harkins.com/movies/now-showing", "li", "posters-container", "block-image", "h2", "Harkins")
	elif( theatre[0] == "amc"):
		moviesFound = scrapeNowShowing(movieName, "https://www.amctheatres.com", "https://www.amctheatres.com/movies", "div", "Slide", None, "h3", "AMC Theatres")
	elif(theatre[0] == "harkins" and theatre[1] == "amc"):
		moviesFound = scrapeNowShowing(movieName, "https://www.harkins.com", "https://www.harkins.com/movies/now-showing", "li", "posters-container", "block-image", "h2", "Harkins")

	return moviesFound


def scrapeNowShowing(movieName, baseUrl,searchUrl, container, containerClass, imgClass, heading, theatre):
	request = requests.get(searchUrl)
	htmlParser = BeautifulSoup(request.text, "html.parser")

	movieContainers = htmlParser.find_all(container, class_=containerClass)

	moviesFound = {}

	for container in movieContainers:
		movie_poster = container.find("img", {"class": imgClass})
		movie_poster = movie_poster['src']

		movie_name = container.find(heading, {"class":None})
		movie_name = movie_name.text.replace('\n', "").strip()

		movie_link = container.find("a").get('href')
		movie_link = baseUrl + movie_link

		if movieName not in movie_name:
			continue
		else:
			moviesFound[movie_name] = [movie_poster,movie_link, theatre]

	return moviesFound

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

if __name__ == "__main__":
	print(scrape())
