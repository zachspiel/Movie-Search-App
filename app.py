# app.py
from flask import Flask, jsonify, render_template, request, Response, redirect, url_for
import json

# to display to html to make output prettier
# https://markhneedham.com/blog/2017/04/27/python-flask-generating-a-static-html-page/
from scraping import scrape, get_movie_name
app = Flask(__name__)


@app.route('/', methods = ["POST", "GET"])
def index():
	d = {}
	searched_movies = {}
	movie_keys=[]
	user_movie = []
	scrape_length = len(scrape())
	for i in range(scrape_length):
		d[get_movie_name()[i]] = scrape()[i]

	if request.method == "POST":
		# compound defined as value specified in form
		posts = request.form
		for post in posts.items():
			compound = post[1].title()

		

		# Create list of keys to find what one user searched for
		for key in d.keys():
			movie_keys.append(key)
			for i in range(len(movie_keys)):
				print(i)
				if compound in movie_keys[i]:
					searched_movies[get_movie_name()[i]] = d[get_movie_name()[i]]

		# Get the key of the searched movie to show the theatres to user
		for key in searched_movies.keys():
			user_movie.append(key)
		return render_template('index.html', movie=user_movie, search=compound, searched_movies=searched_movies)

	return render_template('index.html')


'''
@app.route("/", methods = ["POST", "GET"])
def move_forward():
    #Moving forward code
    forward_message = "Moving Forward..."
    return render_template('index.html', message=forward_message);
'''
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)