# app.py
from flask import Flask, jsonify, render_template, request, Response, redirect, url_for
import json
from scraping import getInfo
# from scraping import topBoxOffice

app = Flask(__name__)


@app.route('/', methods = ["POST", "GET"])
def index():

	# info = topBoxOffice()

	# Render blank template
	#return render_template('index.html',
		#boxOffice = info,clearButton="none")
	return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

@app.route('/search', methods = ["POST","GET"])
def search():
	if request.method == 'POST':
		posts = request.form
		movie_name = posts['movie'].title()

		theatre = request.form.getlist('check')
		print(theatre)
		
		if(len(theatre) == 0):
			return render_template('search.html',clearButton="none")

		info = getInfo(movie_name,theatre)
		
		return render_template(
			'search.html',
			movies = info,
			clearButton = 'visible',
			className = 'py-5 bg-light',
			
		)

	return render_template('search.html',clearButton="none")
