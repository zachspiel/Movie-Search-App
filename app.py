from flask import Flask, render_template, request, Response, redirect, url_for
from scraping import getInfo

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)


@app.route('/search', methods=["POST", "GET"])
def search():
    if request.method == 'POST':
        posts = request.form
        movie_name = posts['movie'].title()

        theaters = request.form.get('theater_list')

        searchResults = getInfo(movie_name, theaters)

        if len(searchResults) == 0:
            return render_template(
                'search.html',
                noResults=True,
            )
        else:
            return render_template(
                'search.html',
                movies=searchResults,
                clearButton='visible',
                className='py-5 bg-light',

            )

    return render_template('search.html', clearButton="none")
