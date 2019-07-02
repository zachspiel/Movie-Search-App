# app.py
from flask import Flask, jsonify, render_template, request, Response, redirect, url_for
import json

from scraping import scrape,get_theatres,get_showtimes, get_movie_name
app = Flask(__name__)


@app.route('/', methods = ["POST", "GET"])
def index():
	# d stores movie name and image
	d = {}
	
	# searched_movies is the movie the user searched for and every showing availible
	searched_movies = {}

	# The movie titles in d
	movie_keys=[]
	show_keys =[]
	# Every showing of searched movie
	user_movie = []
	# All theatres
	theatres = {}
	#All showtimes
	showtimes = {}
	searched_shows = {}

	# length of all movies and theatres
	scrape_length = len(scrape())
	showtime_length = len(get_showtimes())

	# initialize all showings and theatres
	for i in range(scrape_length):
		d[get_movie_name()[i]] = scrape()[i]

	for theatre in get_theatres():
		theatres[theatre] =get_theatres()[theatre];
	
	for show in get_showtimes():
		showtimes[show] = get_showtimes()[show];

	# Checks when form is submitted
	if request.method == "POST":

		posts = request.form
		movie_name = posts['movie'].title()
		theatre_name = posts['theatre'].title()

		# showtime = get_showtimes()[movie_name]
		#check if user search is in kets
		for key in showtimes.keys():
			if movie_name in key:
				showtimes[key] = get_showtimes()[key]
				print(showtimes[key])

		# Create list of keys to find what one user searched for
		for key in d.keys():
			movie_keys.append(key)
			# loop through all movies and check if users search exists in that list
			for i in range(len(movie_keys)):
				if movie_name in movie_keys[i]:
					searched_movies[get_movie_name()[i]] = d[get_movie_name()[i]]

		# Get the key of the searched movie to show the theatres to user
		for key in searched_movies.keys():
			user_movie.append(key)

		# render template with results
		return render_template('index.html', 
			movie=user_movie, 
			search=movie_name, 
			searched_movies=searched_movies, 
			theatres=theatres, 
			theatre_name=theatre_name,showtimes=showtimes)

	# Render blank template
	return render_template('index.html',theatres=theatres)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)