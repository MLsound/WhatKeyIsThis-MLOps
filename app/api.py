# app/api.py
import sys
import os

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the project root to the system path
sys.path.insert(0, project_root)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from flask import Blueprint, request, jsonify
from src.pitch_detector import run as detect_pitch
from utils import Scale

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
        return jsonify({'error': 'No audio file has been sent'}), 400

    audio_file = request.files['audio']
    # audio_file.save('audio_recibido.mp3') # guarda el archivo

    # Check the file type to ensure it's a supported audio format
    if audio_file.mimetype not in ['audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/flac']:
        return jsonify({'error': 'Unsupported file type. Please upload a valid audio file.'}), 415

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

# The Flask endpoint is now correct and will work with this dictionary.
@api.route('/scale/<string:key_name>', methods=['GET'])
def get_scale(key_name):
    print(f"GET method for '{key_name}'")
    new_scale = Scale(key_name) # Creates scale object
    # print(new_scale.root_note, new_scale.api_name)

    # Then, check if the normalized key exists in the comprehensive dictionary
    if new_scale.scale is not None:
        data = {
            'name': new_scale.root_note,
            'mode': new_scale.mode,
            'scale': new_scale.scale,
            'chords': new_scale.chords,
            'relative': new_scale.relative,
        }
        return jsonify(data), 200
    else:
        return jsonify({'error': f'Information for key {key_name} not found.'}), 404

# if __name__=='__main__':
#     api.run(debug=True,port=4400) #38516 (music)