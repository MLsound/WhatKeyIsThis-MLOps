from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
from collections import Counter
from itertools import combinations
debug = True

# Mapping from pitch class numbers to note names
PITCH_CLASSES = ["C", "C#", "D", "D#", "E", "F", 
                    "F#", "G", "G#", "A", "A#", "B"]

def find_common_notes(midi_notes, k):
    #k = 10 # number of most common notes

    # Count the frequency of each MIDI note
    note_counts = Counter(midi_notes)

    # Get the top k most common notes
    top_k_notes = note_counts.most_common(k)

    results = []
    if debug: print(f"The {k} most common notes are:")
    for note_midi, count in top_k_notes:
        # Convert MIDI number to pitch class
        pitch_class_number = note_midi % 12
        pitch_class_name = PITCH_CLASSES[pitch_class_number]
        
        results.append(note_midi)
        if debug: print(f"  - Note: {pitch_class_name} (MIDI: {note_midi}) | Frequency: {count} times")

    return results

def find_chord_from_notes(notes, just_thirds=False):
    """
    Identifies a major or minor chord from a list of notes.

    Args:
        notes (list): A list of three MIDI numbers.

    Returns:
        str: The name of the chord if a match is found, otherwise "No match".
    """
    # Sort notes for consistent interval calculation
    notes.sort()
    
    root_note = notes[0]
    second_note = notes[1]

    # Calculate intervals in half-steps (semitones)
    interval_1 = second_note - root_note
    if not just_thirds: 
        third_note = notes[2]
        interval_2 = third_note - second_note

        # Check for a major chord (4, 3)
        if interval_1 == 4 and interval_2 == 3:
            return f"{get_pitch_class_name(root_note)} Major"

        # Check for a minor chord (3, 4)
        if interval_1 == 3 and interval_2 == 4:
            return f"{get_pitch_class_name(root_note)} Minor"
    else:
        # Check for a major chord (4, 3)
        if interval_1 == 4:
            return f"{get_pitch_class_name(root_note)} Major"

        # Check for a minor chord (3, 4)
        if interval_1 == 3:
            return f"{get_pitch_class_name(root_note)} Minor"

    return None

def get_pitch_class_name(midi_num):
    """Converts a MIDI number to its pitch class name."""
    return PITCH_CLASSES[midi_num % 12]

def detect_pitch(midi_data, k):
    common_notes = find_common_notes(midi_data, k)

    # Try to find triads
    found_chords = []
    chord_options = list(combinations(common_notes, 3))
    for chord in chord_options:
        found = find_chord_from_notes(list(chord))
        if found:
            if debug: print('Chord detected:', found)
            found_chords.append(found)
    if found_chords:
        return True, found_chords
    
    # Try to find thirds
    found_thirds = []
    thirds_options = list(combinations(common_notes, 2))
    for third in thirds_options:
        found = find_chord_from_notes(list(third), just_thirds=True)
        if found:
            if debug: print('Third detected:', found)
            found_thirds.append(found)
    if found_thirds:
        return True, found_thirds
    
    if debug: print("No tonality detected.")
    if common_notes:
        if debug: print("Assuming most repeated note is the root.")
        return False, get_pitch_class_name(common_notes[0])
    
    return False, None

def run(audio_file_path):
    # Make the prediction
    model_output, midi_data, note_events = predict(audio_file_path, ICASSP_2022_MODEL_PATH)
    #if debug: print(note_events)
    # midi_data: The transcribed MIDI file.
    # note_events: A list of note events (frequency, start, end, etc.).

    # Extract MIDI notes from the list
    midi_notes = [event[2] for event in note_events]
    # Count the frequency of each note
    note_counts = Counter(midi_notes)
    # Get the most common note
    most_common_notes = note_counts.most_common(1)

    if debug: print(most_common_notes)
    # Result: [(76, 5)] -> Note 76 was repeated 5 times.

    print()
    detected_pitch = []
    # while detected_pitch == []:
    #     for k in range(3,10+1):
    #         print(f"Trying detection for k = {k}")
    #         detected_pitch = detect_pitch(midi_notes, k)
    #         print(detected_pitch)
    k = 3
    while not detected_pitch and k <= 10:
        print(f"Trying detection for k = {k}")
        is_detected, detected_pitch = detect_pitch(midi_notes, k)
        k += 1 # Incrementa k manualmente
        if not is_detected:
            detected_pitch = []
        else:
            print(detected_pitch)
        
    return detected_pitch

def show(list_values):
    for value in list_values:
        print(value)

if __name__=="__main__":
    # For testing
    files = ['test.wav', '2test.wav', '3test.mp3']
    for file in files:
        print("\n\nARCHIVO:", file)
        audio_file_path = f"media/{file}"
        #audio_file_path = "media/test.wav"
        #audio_file_path = "media/2test.wav"
        #audio_file_path = "media/3test.mp3"

        detected_pitch = run(audio_file_path)
        if detected_pitch is not None:
            if len(detected_pitch)>1:
                print("\nPossible tonalities:")
                show(detected_pitch)
            else:
                print("\nDetected tonality:")
                show(detected_pitch)
        else:
            print("\nIt was not possible to detect the tonality. Please try again with another music fragment.")
