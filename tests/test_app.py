# tests/test_app.py
import pytest
import sys
import os

# Add the project's root directory to the Python path
# This allows imports like 'from app.app import ...' and 'from api import ...' to work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.app import app as flask_app # Import the app instance from app.py

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    return flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_index_route(client):
    """Test the main index route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'What Key is This?' in response.data

def test_key_detect_route(client):
    """Test the key detection route."""
    response = client.get('/detect')
    assert response.status_code == 200
    assert b'Key detection' in response.data

def test_scales_route(client):
    """Test the /scales route."""
    response = client.get('/scales')
    assert response.status_code == 200
    assert b'Scales &amp; Chords' in response.data

def test_show_scale_route_major(client):
    """Test the /scale route for a major key."""
    response = client.get('/scale/c')
    assert response.status_code == 200
    assert b'Scale C' in response.data

def test_show_scale_route_minor(client):
    """Test the /scale route for a minor key."""
    response = client.get('/scale/a?mode=minor')
    assert response.status_code == 200
    assert b'Scale A' in response.data

def test_show_scale_route_not_found(client):
    """Test the /scale route with an invalid key."""
    # Assuming 'invalidkey' is not handled by get_scale_data
    response = client.get('/scale/invalidkey')
    assert response.status_code == 404

def test_parser_route_redirect_major(client):
    """Test the /scale/detected route for a major key redirect."""
    response = client.get('/scale/detected/C_major')
    assert response.status_code == 302 # 302 is the redirect status code
    assert '/scale/c' in response.location # Check if it redirects to the correct URL

def test_parser_route_redirect_minor(client):
    """Test the /scale/detected route for a minor key redirect."""
    response = client.get('/scale/detected/A_minor')
    assert response.status_code == 302
    assert '/scale/a?mode=minor' in response.location

def test_parser_route_redirect_unknown_mode(client):
    """Test the /scale/detected route with an unrecognized mode, which should default to major."""
    response = client.get('/scale/detected/D_unknown')
    assert response.status_code == 302
    assert '/scale/d' in response.location
    assert 'mode=minor' not in response.location # Ensure it does not include the mode parameter

def test_page_not_found(client):
    """Test the 404 error handler."""
    response = client.get('/this-is-not-a-valid-route')
    assert response.status_code == 404
    assert b'Page not found' in response.data