# app.py
from flask import Flask, jsonify, render_template, request, Response, redirect, url_for
import json
from scraping import getInfo

app = Flask(__name__)


@app.route('/', methods = ["POST", "GET"])
def index():
	if request.method == "POST":
		posts = request.form
		movie_name = posts['movie'].title()

		info = getInfo(movie_name)
		
		return render_template(
			'index.html',
			movies = info,
			clearButton = 'visible'
		)

	# Render blank template
	return render_template('index.html',clearButton="none")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
