# src/scales_generator.py
info_musical = {}

# Definición de las 12 notas
# Las representamos como bemoles y sostenidos para manejar ambas notaciones
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
flat_notes = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B']

# Los intervalos de semitonos para cada tipo de escala (Mayor y Menor Natural)
intervals_major = [0, 2, 4, 5, 7, 9, 11]  # W-W-H-W-W-W-H
intervals_minor = [0, 2, 3, 5, 7, 8, 10]  # W-H-W-W-H-W-W

# Estructura de los acordes triada (ej. C, Dm, Em...)
chords_major = ['M', 'm', 'm', 'M', 'M', 'm', 'dim']
chords_minor = ['m', 'dim', 'M', 'm', 'm', 'M', 'M']

# Función para generar la escala
def generate_scale(root_note, intervals):
    scale = []
    root_index = notes.index(root_note)
    for interval in intervals:
        scale_note_index = (root_index + interval) % 12
        new_note = notes[scale_note_index]
        scale.append(new_note)
    return scale

# Función para corregir escalas escritas con bemoles
def fix_scales(major_scale, minor_scale):
    # Escalas tradicionalmente escritas con bemoles
    flat_majors = ['F', 'A#', 'D#','G#','C#', 'F#']
    flat_minors = ['Dm', 'Gm', 'Cm', 'Fm', 'A#m']
    if major_scale[0] in flat_majors:
        for i, note in enumerate(major_scale):
            if '#' in note:
                major_scale[i] = flat_notes[notes.index(note)]
    if minor_scale[0] in [n[:-1] for n in flat_minors]:
        for i, note in enumerate(minor_scale):
            if '#' in note:
                minor_scale[i] = flat_notes[notes.index(note)]
    # Finally, fix problematic enharmonic scales
    # F# Maj => Cb (Not B)
    if major_scale[0] == 'G♭':
        major_scale[3] = 'C♭'
    # D# min => E# (Not F)
    if minor_scale[0] == 'D#':
        minor_scale[1] = 'E#'
    return major_scale, minor_scale

# Función para generar los acordes (diatónicos)
def generate_chords(scale, chord_types):
    chords = []
    for i in range(len(scale)):
        note = scale[i]
        chord_type = chord_types[i]
        
        # Manejar el sufijo para cada tipo de acorde
        if chord_type == 'M':
            chords.append(note) # Acorde Mayor (sin sufijo)
        elif chord_type == 'm':
            chords.append(f"{note}m") # Acorde menor
        elif chord_type == 'dim':
            chords.append(f"{note}dim") # Acorde disminuido
    return chords

# Función para obtener la nota relativa
def get_relative_key(root_note, mode):
    root_index = notes.index(root_note)
    if mode == 'major':
        relative_index = (root_index - 3 + 12) % 12
        return notes[relative_index] + 'm'
    elif mode == 'minor':
        relative_index = (root_index + 3) % 12
        return notes[relative_index]

# Testing
def test(scales):
    for key, data in scales.items():
        for mode in ['major', 'minor']:
            scale_notes = data['scale'][mode]
            # Get only the letter part (A-G) of each note
            letters = [note[0] for note in scale_notes]
            # Check if all letters A-G appear exactly once
            unique_letters = set(letters)
            if len(scale_notes) == 7 and unique_letters == set('ABCDEFG'):
                print(f"{key} {mode}: OK")
            else:
                print(f"{key} {mode}: ERROR - Letters: {letters}")
                print('-> Notes: ',scale_notes)

# Showing structured data for debugging
def show_scales(scales):
    for scale in scales:
        print('Escala', scale)
        print('MAYOR:')
        print('- Notas:',scales[scale]['scale']['major'])
        print('- Acordes:',scales[scale]['chords']['major'])
        print('- Relativas:',scales[scale]['relative']['major'])
        print('MENOR:')
        print('- Notas:',scales[scale]['scale']['minor'])
        print('- Acordes:',scales[scale]['chords']['minor'])
        print('- Relativas:',scales[scale]['relative']['minor'])
        print('\n')

def run():
    # Generar el diccionario completo
    for note in notes:
        # Generar escalas
        major_scale = generate_scale(note, intervals_major)
        minor_scale = generate_scale(note, intervals_minor)

        # Fix for flat scales
        major_scale, minor_scale = fix_scales(major_scale,minor_scale)

        # Generar acordes
        major_chords = generate_chords(major_scale, chords_major)
        minor_chords = generate_chords(minor_scale, chords_minor)

        # Obtener relativas
        relative_major = get_relative_key(note, 'major')
        relative_minor = get_relative_key(note, 'minor')

        # Añadir a la estructura del diccionario
        info_musical[note] = {
            'scale': {
                'major': major_scale,
                'minor': minor_scale
            },
            'chords': {
                'major': major_chords,
                'minor': minor_chords
            },
            'relative': {
                'major': relative_major,
                'minor': relative_minor
            }
        }
    return info_musical

if __name__=='__main__':
    scales = run()
    #show_scales(scales)
    test(scales)
