# tests/test_api.py
import pytest
import io
from unittest.mock import patch
from flask import Flask, json

# Import the Blueprint from the api.py script
from app.api import api as api_blueprint

# Create a test application and register the blueprint
@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = Flask(__name__)
    app.config.update({"TESTING": True})
    app.register_blueprint(api_blueprint, url_prefix='/api')
    return app

# Create a test client using the app fixture
@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_root_endpoint(client):
    """Test the root endpoint of the API blueprint."""
    response = client.get('/api/')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == "Welcome dear human…"

@patch('app.api.detect_pitch')
def test_detect_tone_valid_audio(mock_detect_pitch, client):
    """Test the /detect endpoint with a valid audio file."""
    # Mock the pitch detection function to return a predictable value
    mock_detect_pitch.return_value = ("C", "major")

    # Create a mock audio file in memory
    data = {
        'audio': (io.BytesIO(b"fake audio data"), 'test.mp3')
    }
    
    response = client.post('/api/detect', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['pitch'] == "C"
    assert data['mode'] == "major"
            
@patch('app.api.detect_pitch')
def test_detect_tone_no_audio_file(mock_detect_pitch, client):
    """Test the /detect endpoint with no audio file."""
    response = client.post('/api/detect')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'No audio file has been sent' in data['error']

@patch('app.api.detect_pitch')
def test_detect_tone_unsupported_file_type(mock_detect_pitch, client):
    """Test the /detect endpoint with an unsupported file type."""
    # Create a mock text file in memory
    data = {
        'audio': (io.BytesIO(b'this is not audio'), 'test.txt')
    }
    response = client.post('/api/detect', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 415
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Unsupported file type' in data['error']

def test_get_scale_valid_key(client):
    """Test the /scale/<key_name> endpoint with a valid key."""
    response = client.get('/api/scale/C')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['root'] == 'C'
    assert data['mode'] == 'major'

def test_get_scale_valid_key_with_minor_suffix(client):
    """Test the /scale/<key_name> endpoint with a valid key and minor suffix."""
    response = client.get('/api/scale/Am')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['root'] == 'A' 
    assert data['mode'] == 'minor'

def test_get_scale_enharmonic_note(client):
    """Test the /scale/<key_name> endpoint with an enharmonic note."""
    response = client.get('/api/scale/C-sharp')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['root'] == 'C#' 
    assert data['mode'] == 'major'

def test_get_scale_invalid_key(client):
    """Test the /scale/<key_name> endpoint with an invalid key."""
    response = client.get('/api/scale/invalid_key')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Information for key invalid_key not found' in data['error']