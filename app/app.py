from flask import Flask, render_template
from api import api

app = Flask(__name__)

# Register the blueprint with a URL prefix
# This means all endpoints in api.py will be prefixed with /api
app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def index():
    cursos = ['PHP', 'Python','Rust','Go','JavaScript']
    data = {
        'title': 'What Key is This?',
        'bienvenida': 'Saludos!',
        'cursos': cursos,
        'num': len(cursos)
    }
    return render_template('index.html', data=data)

@app.route('/detect')
def key_detect():
    data = {
        'title': 'Key detection'
    }
    return render_template('upload.html', data=data)

def page_not_found(error):
    return render_template('404.html'), 404 # Página de error

if __name__=='__main__':
    app.register_error_handler(404, page_not_found)
    app.run(debug=True)