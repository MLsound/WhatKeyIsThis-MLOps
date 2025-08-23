# app/app.py
from flask import Flask, render_template
from .api import api

app = Flask(__name__)

# Register the blueprint with a URL prefix
# All endpoints in api.py will be prefixed with /api
app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def index():
    data = {'title': 'What Key is This?'}
    return render_template('index.html', data=data)

@app.route('/detect')
def key_detect():
    data = {'title': 'Key detection'}
    return render_template('upload.html', data=data)

@app.route('/scales')
def choose_scale():
    data = {'title': 'Scales & Chords'}
    return render_template('keyboard.html', data=data)


def page_not_found(error):
    return render_template('404.html'), 404

app.register_error_handler(404, page_not_found)

if __name__=='__main__':
    app.run(debug=True)