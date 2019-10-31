from bs4 import BeautifulSoup
import requests

# GET MOVIE POSTER PAGE FOR SCRAPING
base_url = 'https://www.harkins.com/movies/now-showing'
r = requests.get(base_url)
soup = BeautifulSoup(r.text, "html.parser")

all_movies = soup.find_all('li', class_="posters-container") # find all movies now playing

# ****** FUNCTION TO GET MOVIE POSTER IMAGES ***** #
def getInfo(movieName):
	movies = {}

	for item in all_movies:
		movie_poster = item.find("img", {"class": "block-image"})
		movie_poster = movie_poster['src']

		movie_name = item.find("h2", {"class":None})
		movie_name = movie_name.text.replace('\n', "").strip()

		movie_link = item.find("a").get('href')
		movie_link = "harkins.com/" + movie_link

		if movieName not in movie_name:
			continue
		else:
			movies[movie_name] = [movie_poster,movie_link]
			#movieLink = movie_name + "_link"
			#print(movieLink)
			#movies[movie_name + "_link"] = movie_link

	return movies

if __name__ == "__main__":
	print(scrape())


