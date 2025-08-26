# app/app.py
from flask import Flask, render_template, request
from .api import api
from src.utils import get_scale_data, get_url, get_music_score

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
    mode = request.args.get('mode', 'major').lower() # ?mode=minor
    is_minor = True if mode.lower() == 'minor' else False
    print(f"URL parameters: '{detected}', '{mode}'") # For debugging

    if detected is not None:
        print('Detection parameter received:',detected)
        scale = ''
        pass
    else:
        scale =  get_scale_data(f'{key_name}', is_minor) # API Call
    if scale is None:
        print("ALERT: Scale has not been detected!")
        return render_template('404.html'), 404
    else:
        data = {
            'title': f'Scale {key_name.capitalize()}',
            'key_name': key_name,
            'enharmonic': scale['enharmonic'],
            'name': get_url(scale['root']).capitalize(),
            'is_flat': scale['is_flat'],
            'mode': scale['mode'],
            'relative': get_url(scale['relative']),
            'scale': scale,
            # Generate the music score and get its path
            'score_path': get_music_score(key_name, mode)
            }
        return render_template('scale.html', data=data)

from flask import redirect, url_for
@app.route('/scale/detected/<string:pitch>')
def parser(pitch):
    print('Detection parameter received:', pitch)
    # Split the pitch string into the root note and the mode.
    # Example: 'C_minor' -> ['c', 'minor']
    root, mode = pitch.lower().split('_')

    # Default to major if the mode is not recognized.
    if not (mode == 'major' or mode == 'minor'):
        print("Unrecognized mode:", mode)
        mode = 'major'

    is_minor = mode == 'minor'
    key_name = get_url(root)
    
    # Build the URL for redirection
    if is_minor:
        redirect_url = url_for('show_scale', key_name=key_name, mode='minor')
    else:
        redirect_url = url_for('show_scale', key_name=key_name)

    print(f"Redirecting to: {redirect_url}")
    return redirect(redirect_url)

def page_not_found(error):
    return render_template('404.html'), 404

app.register_error_handler(404, page_not_found)

if __name__=='__main__':
    app.run(debug=True)