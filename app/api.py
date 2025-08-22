# app/api.py
import sys
import os

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the project root to the system path
sys.path.insert(0, project_root)

# Now your import will work correctly
from flask import Blueprint, request, jsonify
from src.pitch_detector import run as detect_pitch

# For input sanitization
import tempfile  # Import the tempfile library
from werkzeug.utils import secure_filename

# Change this line to create a Blueprint
api = Blueprint('api', __name__)

@api.route("/")
def root():
    return "Wellcome dear human…"

@api.route('/detect', methods=['POST'])
def detectar_tono():
    if 'audio' not in request.files:
        return jsonify({'error': 'No se ha enviado ningún archivo de audio'}), 400

    audio_file = request.files['audio']
    # audio_file.save('audio_recibido.mp3') # guarda el archivo

    # Check the file type to ensure it's a supported audio format
    if audio_file.mimetype not in ['audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/flac']:
        return jsonify({'error': 'Tipo de archivo no soportado. Por favor suba un archivo de audio válido.'}), 415

    # Use a try-finally block to ensure the temporary file is deleted
    try:
        # Create a temporary file with a specific extension
        # 'suffix' is important for libraries that rely on the file type
        with tempfile.NamedTemporaryFile(suffix=f'.{secure_filename(audio_file.filename).split(".")[-1]}', delete=False) as temp_file:
            # Write the content of the uploaded file to the temporary file
            audio_file.save(temp_file)
            temp_file_path = temp_file.name
            # print(">>Temp file created:", temp_file_path)

        # Pass the path of the temporary file to your pitch detection function
        pitch = detect_pitch(temp_file_path)
        return jsonify({'pitch': pitch}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # This block ensures the temporary file is deleted, even if an error occurs
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            # print(">>Temp file successfully deleted!")


# THIS SECTION WILL BE REPLACED LATER BY A GENERATOR FUNCTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create a mapping for enharmonic notes and common name variations
key_name_mapping = {
    'C-sharp': 'C#',
    'D-flat': 'Db',
    'D-sharp': 'D#',
    'E-flat': 'Eb',
    'F-sharp': 'F#',
    'G-flat': 'Gb',
    'G-sharp': 'G#',
    'A-flat': 'Ab',
    'A-sharp': 'A#',
    'B-flat': 'Bb',
}
sharp_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
flat_notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
notes = list(set(sharp_notes + flat_notes))
info_musical = {note: {'scale': note} for note in notes} # Handler for future development
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# The Flask endpoint is now correct and will work with this dictionary.
@api.route('/scale/<string:key_name>', methods=['GET'])
def get_scale(key_name):
    print('GET method for', key_name)
    is_minor = False
    
    # Handle the minor key suffix first
    if key_name.endswith('m'):
        key_name = key_name[:-1]
        is_minor = True

    # Normalize the key_name using the mapping
    # If the key is in the map, use the mapped value; otherwise, use the original key
    normalized_key_name = key_name_mapping.get(key_name, key_name)
    print(normalized_key_name)
    
    # Now, check if the normalized key exists in the comprehensive dictionary
    if normalized_key_name in info_musical:
        data = {
            'scale': info_musical[normalized_key_name]['scale'],
            'mode': 'minor' if is_minor else 'major'
        }
        return jsonify(data), 200
    else:
        return jsonify({'error': f'Información para la clave {key_name} no encontrada.'}), 404


# if __name__=='__main__':
#     api.run(debug=True,port=4400) #38516 (music)