#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
base_url = 'https://www.harkins.com/movies/now-showing'

# Request URL and Beautiful Parser
r = requests.get(base_url)
soup = BeautifulSoup(r.text, "html.parser")
all_movies = soup.find_all('li', class_="posters-container")

def scrape():
	l = []

	for item in all_movies:

		movie_poster = item.find("img", {"class": "block-image"})
		movie_poster = movie_poster['src']
		l.append(movie_poster)

#		movie_name = item.find("div", {"class":"tabel-cell"})
#		d['movie_name'] = movie_name


	return l

def get_movie_name():
	movies = []
	for item in all_movies:
		movie_name = item.find("h2", {"class":None})
		movie_name = movie_name.text.replace('\n', "").strip()
		movies.append(movie_name)

	return movies

	'''
	movies = soup.find_all('h2', {"class":None})
	names = []
	for item in movies:
		item = movies.text.strip()
		names.append(name)

	return names
	'''
if __name__ == "__main__":
	print(scrape())