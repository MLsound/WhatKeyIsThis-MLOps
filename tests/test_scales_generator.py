# tests/test_scales_generator.py
import pytest
from src.scales_generator import (
    notes, 
    flat_notes, 
    generate_scale, 
    generate_chords, 
    get_relative_key, 
    fix_scales, 
    intervals_major, 
    intervals_minor,
    chords_major,
    chords_minor
)


# Using a fixture to generate the scales once
@pytest.fixture(scope="module")
def all_scales():
    """Generates all scales to be used by the tests."""
    scales = {}
    for note in notes:
        major_scale = generate_scale(note, intervals_major)
        minor_scale = generate_scale(note, intervals_minor)
        
        # Apply the fix_scales function
        major_scale, minor_scale = fix_scales(major_scale, minor_scale)
        
        scales[note] = {
            'major': major_scale,
            'minor': minor_scale
        }
    return scales

# --- Test Cases ---

def test_generate_scale_major(all_scales):
    """Test major scales."""
    assert all_scales['C']['major'] == ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    assert all_scales['G']['major'] == ['G', 'A', 'B', 'C', 'D', 'E', 'F#']
    assert all_scales['F']['major'] == ['F', 'G', 'A', 'B♭', 'C', 'D', 'E']
    assert all_scales['A#']['major'] == ['B♭', 'C', 'D', 'E♭', 'F', 'G', 'A']
    assert all_scales['C#']['major'] == ['D♭', 'E♭', 'F', 'G♭', 'A♭', 'B♭', 'C']
    assert all_scales['F#']['major'] == ['G♭', 'A♭', 'B♭', 'C♭', 'D♭', 'E♭', 'F']
    assert all_scales['G#']['major'] == ['A♭', 'B♭', 'C', 'D♭', 'E♭', 'F', 'G']

def test_generate_scale_minor(all_scales):
    """Test minor scales."""
    assert all_scales['C']['minor'] == ['C', 'D', 'E♭', 'F', 'G', 'A♭', 'B♭']
    assert all_scales['E']['minor'] == ['E', 'F#', 'G', 'A', 'B', 'C', 'D']
    assert all_scales['A']['minor'] == ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    assert all_scales['F']['minor'] == ['F', 'G', 'A♭', 'B♭', 'C', 'D♭', 'E♭']
    assert all_scales['D#']['minor'] == ['D#', 'E#', 'F#', 'G#', 'A#', 'B', 'C#']
    assert all_scales['F#']['minor'] == ['F#', 'G#', 'A', 'B', 'C#', 'D', 'E']


def test_fix_scales_function():
    """Test edge cases for the fix_scales function."""
    major_scale_to_fix = ['F#', 'G#', 'A#', 'C', 'C#', 'D#', 'F']
    minor_scale_to_fix = ['D#', 'F', 'F#', 'G#', 'A#', 'B', 'C#']
    
    # Note: fix_scales returns a tuple, so we need to unpack it
    fixed_major, fixed_minor = fix_scales(major_scale_to_fix, minor_scale_to_fix)
    
    assert fixed_major == ['G♭', 'A♭', 'B♭', 'C♭', 'D♭', 'E♭', 'F']
    # D# minor should have E#, not F
    assert fixed_minor[1] == 'E#'

def test_generate_chords_major():
    """Test major chords."""
    c_major_scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    assert generate_chords(c_major_scale, chords_major) == ['C', 'Dm', 'Em', 'F', 'G', 'Am', 'Bdim']

def test_generate_chords_minor():
    """Test minor chords."""
    a_minor_scale = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    assert generate_chords(a_minor_scale, chords_minor) == ['Am', 'Bdim', 'C', 'Dm', 'Em', 'F', 'G']

def test_get_relative_key():
    """Test relative key calculations."""
    assert get_relative_key('C', 'major') == 'A'
    assert get_relative_key('A', 'minor') == 'C'
    assert get_relative_key('G', 'major') == 'E'
    assert get_relative_key('C#', 'major') == 'A#'
    assert get_relative_key('F#', 'minor') == 'A'