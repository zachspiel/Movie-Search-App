# app.py
from flask import Flask, jsonify
import json

# to display to html to make output prettier
# https://markhneedham.com/blog/2017/04/27/python-flask-generating-a-static-html-page/
from scraping import scrape, get_movie_name
app = Flask(__name__)
@app.route('/')
def index():
	images = []
	scrape_length = len(scrape())
	for i in range(scrape_length):
		images.append('<div style="display:inline-block">')
		images.append( "<img src=%s style='width:200;height:250;'></img> " % scrape()[i])
		images.append(get_movie_name()[i])
		images.append('</div>')
	 # image = scrape()[0]
	return json.dumps(images)
	

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)