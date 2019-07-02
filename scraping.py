from bs4 import BeautifulSoup
import requests

# GET MOVIE POSTER PAGE FOR SCRAPING
base_url = 'https://www.harkins.com/movies/now-showing'
r = requests.get(base_url)
soup = BeautifulSoup(r.text, "html.parser")

all_movies = soup.find_all('li', class_="posters-container") # find all movies now playing

# ********************************************************* #
# GET LOCATIONS PAGE FOR SCRAPING

base_url_locations = 'https://www.harkins.com/locations'
locations = requests.get(base_url_locations)
locations_soup = BeautifulSoup(locations.text, "html.parser")

all_theatres = locations_soup.find_all('li', class_="col-1/2") # find all Harkins theatres containers

 # ********************************************************* #
#GET SHOWTIMES PAGE FOR SCRAPING
base_url_showtimes = 'https://www.harkins.com/locations/arizona-mills-25-w-imax'
showtimes = requests.get(base_url_showtimes)
showtimes_soup = BeautifulSoup(showtimes.text, "html.parser")

all_showtimes = showtimes_soup.find_all('li',class_="ease-in-up") # find all movies now playing

# ****** FUNCTION TO GET MOVIE POSTER IMAGES ***** #
def scrape():
	l = []

	for item in all_movies:
		movie_poster = item.find("img", {"class": "block-image"})
		movie_poster = movie_poster['src']
		l.append(movie_poster)

	return l

# ***** FUNCTION TO FIND ALL HARKINS MOVIE THEATRES ***** #
def get_theatres():
	theatres = {}

	for theatre in all_theatres:
		theatre_name = theatre.find("h3", {"class":"underlined"})
		theatre_name = theatre_name.text.replace('\n', "").strip()

		theatre_link = theatre.find("a", {"class":None})
		theatre_link = "https://harkins.com" + str(theatre_link.get('href'))

		theatres[theatre_name] = theatre_link

	return theatres

def get_showtimes():
	times = {}

	for time in all_showtimes:
		showtime = time.find('ul', {"class":"showtimes"})
		showtime = showtime.text.replace('\n', " ").strip()
		
		name = time.find("a", {"class":None})
		name = name.text.replace('\n', "").strip()

		times[name] = showtime

	return times

def get_movie_name():
	movies = []
	for item in all_movies:
		movie_name = item.find("h2", {"class":None})
		movie_name = movie_name.text.replace('\n', "").strip()
		movies.append(movie_name)

	return movies

if __name__ == "__main__":
	print(scrape())