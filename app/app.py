# app/app.py
from flask import Flask, render_template, request
from .api import api
from src.utils import get_scale_data, solfeggio, flip_accidentals

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

@app.route('/scale/<string:key_name>')
def show_scale(key_name):
    print('User asked for', key_name.upper())

    # Obtiene el valor de los parámetros de la URL.
    # # Ej: http://localhost:5000/scale/1?is_flat=True=True
    detected = request.args.get('detected') # ?detected='G Minor'
    mode = request.args.get('mode') # ?mode=Minor
    is_flat = request.args.get('is_flat') # ?is_flat=True=True
    print(detected, mode, is_flat, sep=",") # For debugging

    if is_flat is not None:
        print('EN BEMOLES!')
        print(key_name)
        key_name = flip_accidentals(key_name)
        print(key_name)
    if mode.lower() == 'minor':
        print('ES MENOR')
        scale =  get_scale_data(f'{key_name}m')
    else:
        print('ES MAYOR')
        scale =  get_scale_data(key_name)
    scale_name =  solfeggio(scale['scale'])
    # print(scale, scale_name)
    data = {
        'title': f'Scale {key_name.upper()}',
        'name': scale_name,
        'mode': scale['mode'].capitalize()
        }
    return render_template('scale.html', data=data)

def page_not_found(error):
    return render_template('404.html'), 404

app.register_error_handler(404, page_not_found)

if __name__=='__main__':
    app.run(debug=True)