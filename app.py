# app.py
from flask import Flask, jsonify, render_template, request, Response, redirect, url_for
import json
from scraping import getInfo
from scraping import getLatestReleases

app = Flask(__name__)

NO_MOVIES_FOUND = 0

@app.route('/', methods = ["POST", "GET"])
def index():
	latestMovies = getLatestReleases()

	searchResults = getInfo("","harkins,amc")

	print(set(latestMovies) and set(searchResults))

	return render_template('index.html', movies = latestMovies)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

@app.route('/search', methods=["POST", "GET"])
def search():
	if request.method == 'POST':
		posts = request.form
		movie_name = posts['movie'].title()

		theatre = request.form.getlist('check')

		if(len(theatre) == 0):
			return render_template('search.html',clearButton="none")

		info = getInfo(movie_name,theatre)

		if len(info) == NO_MOVIES_FOUND:
			return render_template(
				'search.html',
				noResults = True,
			)
		else:
			return render_template(
				'search.html',
				movies = info,
				clearButton = 'visible',
				className = 'py-5 bg-light',

			)

	return render_template('search.html',clearButton="none")
