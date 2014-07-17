from flask import Flask, render_template
from app.controllers import search

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/results')
def results():
        return search.Search().keyword()


@app.route('/results/json')
def results_json():
        return search.Search().keyword('json')

if __name__ == '__main__':
    app.debug = False
    app.run()
