# tests/test_utils.py
import pytest, sys, os, music21
from unittest.mock import patch, MagicMock

# Add the project's root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import (
    Scale, 
    get_url, 
    format_music21, 
    get_music_score, 
    flip_accidentals, 
    user_repr, 
    solfeggio,
    get_scale_data
)
from requests.exceptions import RequestException

# Mock the scales_generator module as it's an external dependency
@pytest.fixture
def mock_scales_generator():
    """Mock the scales_generator.run() function."""
    mock_data = {
        'C': {
            'scale': {'major': ['C', 'D', 'E', 'F', 'G', 'A', 'B']},
            'chords': {'major': ['C', 'Dm', 'Em', 'F', 'G', 'Am', 'Bdim']},
            'relative': {'major': 'Am'}
        },
        'A': {
            'scale': {'minor': ['A', 'B', 'C', 'D', 'E', 'F', 'G']},
            'chords': {'minor': ['Am', 'Bdim', 'C', 'Dm', 'Em', 'F', 'G']},
            'relative': {'minor': 'C'}
        },
        'F#': {
            'scale': {'major': ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#']},
            'chords': {'major': ['F#', 'G#m', 'A#m', 'B', 'C#', 'D#m', 'E#dim']},
            'relative': {'major': 'D#m'}
        }
    }
    with patch('src.scales_generator.run', return_value=mock_data) as mock_run:
        yield mock_run

### Tests for the Scale Class ###

def test_scale_init_major(mock_scales_generator):
    """Test initialization for a major scale."""
    s = Scale('C')
    assert s.is_minor is False
    assert s.mode == 'major'
    assert s.root_note == 'C'
    assert s.api_name == 'C'
    assert s.scale == ['C', 'D', 'E', 'F', 'G', 'A', 'B']

def test_scale_init_minor(mock_scales_generator):
    """Test initialization for a minor scale."""
    s = Scale('Am')
    assert s.is_minor is True
    assert s.mode == 'minor'
    assert s.root_note == 'A'
    assert s.api_name == 'A'
    assert s.scale == ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def test_scale_init_with_sharps(mock_scales_generator):
    """Test initialization for a sharp scale."""
    s = Scale('f-sharp')
    assert s.is_sharp is True
    assert s.is_flat is False
    assert s.root_note == 'F#'
    assert s.enharmonic == 'g-flat'
    assert s.api_name == 'F#'

def test_scale_init_with_flats(mock_scales_generator):
    """Test initialization for a flat scale."""
    s = Scale('d-flat')
    assert s.is_sharp is False
    assert s.is_flat is True
    assert s.root_note == 'Db'
    assert s.enharmonic == 'c-sharp'
    assert s.api_name == 'C#' # api_name should be enharmonic for db since its not in the _api_mapping list

def test_scale_init_invalid_key(mock_scales_generator):
    """Test initialization with a key not in the mock data."""
    s = Scale('invalid')
    assert s.scale is None
    assert s.chords is None
    assert s.relative is None

### Tests for Helper Functions ###

@pytest.mark.parametrize('key_name, expected_url', [
    ('C#', 'c-sharp'),
    ('Ab', 'a-flat'),
    ('C', 'c'),
    ('a', 'a')
])
def test_get_url(key_name, expected_url):
    """Test the get_url function."""
    assert get_url(key_name) == expected_url

@pytest.mark.parametrize('key_name, expected_format', [
    ('c', 'C'),
    ('a-flat', 'A-'),
    ('c-sharp', 'C#')
])
def test_format_music21(key_name, expected_format):
    """Test the format_music21 function."""
    assert format_music21(key_name) == expected_format

@patch('src.utils.os.makedirs')
@patch('src.utils.os.path.exists', return_value=True)
@patch('src.utils.stream.Stream.write')
@patch('src.utils.scale.MajorScale', return_value=MagicMock(pitches=[
    music21.pitch.Pitch('C4'),
    music21.pitch.Pitch('D4'),
    music21.pitch.Pitch('E4'),
    music21.pitch.Pitch('F4'),
    music21.pitch.Pitch('G4'),
    music21.pitch.Pitch('A4'),
    music21.pitch.Pitch('B4'),
    music21.pitch.Pitch('C5')
]))
def test_get_music_score(mock_scale, mock_write, mock_exists, mock_makedirs):
    """Test get_music_score function, mocking file system and music21 calls."""
    result = get_music_score('C', 'major')
    assert result == os.path.join('output', 'scale.png')
    mock_scale.assert_called_once_with('C')
    mock_write.assert_called_once_with('musicxml.png', fp='./app/static/images/output/scale.png')

@pytest.mark.parametrize('key_name, expected_flip', [
    ('A#', 'Bb'),
    ('Ab', 'G#'),
    ('C', 'C'),
    ('c-sharp', 'd-flat')
])
def test_flip_accidentals(key_name, expected_flip):
    """Test the flip_accidentals function."""
    assert flip_accidentals(key_name) == expected_flip

@pytest.mark.parametrize('note, expected_repr', [
    ('C', 'Do'),
    ('C#', 'Do♯'),
    ('Bb', 'Si♭')
])
def test_user_repr(note, expected_repr):
    """Test the user_repr function."""
    assert user_repr(note) == expected_repr
    
def test_solfeggio():
    """Test the solfeggio function."""
    # Assuming 'note_mapping' is made available to the function,
    # this test would work as follows.
    notes = ['C', 'D', 'E']
    expected_notes = ['Do', 'Re', 'Mi']
    assert solfeggio(notes) == expected_notes

@patch('src.utils.requests.get')
def test_get_scale_data_success(mock_get):
    """Test successful API call."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'scale': 'data'}
    mock_get.return_value = mock_response

    result = get_scale_data('c')
    assert result == {'scale': 'data'}
    mock_get.assert_called_once_with('http://127.0.0.1:5000/api/scale/c')

@patch('src.utils.requests.get')
def test_get_scale_data_minor(mock_get):
    """Test API call for a minor key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'scale': 'data'}
    mock_get.return_value = mock_response

    result = get_scale_data('am', is_minor=True)
    assert result == {'scale': 'data'}
    mock_get.assert_called_once_with('http://127.0.0.1:5000/api/scale/am')

@patch('src.utils.requests.get', side_effect=RequestException("Test connection error"))
def test_get_scale_data_request_failure(mock_get):
    """Test handling of a failed network request."""
    result = get_scale_data('c')
    assert result is None
    mock_get.assert_called_once_with('http://127.0.0.1:5000/api/scale/c')