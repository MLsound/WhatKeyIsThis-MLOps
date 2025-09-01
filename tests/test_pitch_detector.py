# tests/test_pitch_detector.py
import pytest
from src.pitch_detector import find_chord_from_notes, get_pitch_class_name, find_common_notes

# Example test for a major chord
def test_find_chord_from_notes_major():
    # Arrange: Set up the input data
    notes = [60, 64, 67] # MIDI numbers for C, E, G

    # Act: Call the function you are testing
    result = find_chord_from_notes(notes)

    # Assert: Check if the output is what you expect
    assert result == "C Major"

# Example test for a minor chord
def test_find_chord_from_notes_minor():
    # Arrange
    notes = [60, 63, 67] # MIDI numbers for C, Eb, G

    # Act
    result = find_chord_from_notes(notes)

    # Assert
    assert result == "C Minor"

# Example test for no match
def test_find_chord_from_notes_no_match():
    # Arrange
    notes = [60, 62, 65] # C, D, F

    # Act
    result = find_chord_from_notes(notes)

    # Assert
    assert result is None

# A test for the get_pitch_class_name function
def test_get_pitch_class_name():
    # Arrange
    midi_num = 60 # C4

    # Act
    result = get_pitch_class_name(midi_num)

    # Assert
    assert result == "C"

# A test for the find_common_notes function with a simple list
def test_find_common_notes():
    # Arrange
    midi_notes = [60, 60, 64, 67, 60, 64]
    k = 2

    # Act
    result = find_common_notes(midi_notes, k)

    # Assert
    assert result == [60, 64]