# app/app.py
from flask import Flask, render_template, request
from .api import api
from src.utils import get_scale_data, get_url, flip_accidentals

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
    # # Ej: http://localhost:5000/scale/1?is_flat=True
    detected = request.args.get('detected') # ?detected='G Minor'
    mode = request.args.get('mode', 'Major').lower() # ?mode=Minor
    #if mode is None: mode = 'Major' # Default for Major scale
    is_flat = request.args.get('is_flat') == 'True'
    is_minor = True if mode.lower() == 'minor' else False
    # if key_name.endswith('m'):  # Option for accepting 'm' ending for minor scale
    #     mode, is_minor = 'minor', True
    #     key_name = key_name [:-1]
    print(f"URL parameters: '{detected}', '{mode}', '{is_flat}'") # For debugging

    if detected is not None:
        #key_name, mode, is_flat = parser(detected)
        print('Detection parameter received:',detected)
        scale = ''
        pass
    else:
        if is_flat: key_name = flip_accidentals(key_name)
        scale =  get_scale_data(f'{key_name}', is_minor) # API Call
    if scale is None:
        print("ALERT: Scale has not been detected!")
        return render_template('404.html'), 404
    else:
        scale_name = get_url(scale['name']).capitalize()
        # print(scale, scale_name)
        data = {
            'title': f'Scale {key_name.capitalize()}',
            'key_name': key_name,
            'name': scale_name,
            'mode': scale['mode'],
            'relative': get_url(scale['relative']),
            'is_flat': is_flat,
            'scale': scale
            }
        return render_template('scale.html', data=data)

def page_not_found(error):
    return render_template('404.html'), 404

app.register_error_handler(404, page_not_found)

if __name__=='__main__':
    app.run(debug=True)