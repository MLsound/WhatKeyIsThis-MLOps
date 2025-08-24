import requests
import json
import src.scales_generator as sg

class Scale:
    """
    A class to represent a musical scale, its notes, and related musical data.
    """
    # Mapping for enharmonic and simplified input
    _key_name_mapping = {
        # URL style names
        'a': 'A',
        'b': 'B',
        'c': 'C',
        'd': 'D',
        'e': 'E',
        'f': 'F',
        'g': 'G',

        # Accidentals
        'a-flat': 'Ab',
        'a-sharp': 'A#',
        'b-flat': 'Bb',
        'c-sharp': 'C#',
        'd-flat': 'Db',
        'd-sharp': 'D#',
        'e-flat': 'Eb',
        'f-sharp': 'F#',
        'g-flat': 'Gb',
        'g-sharp': 'G#'
    }

    _api_mapping = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def __init__(self, key_name: str):
        """
        Initializes a Scale object with a given key name.

        Args:
            key_name: A string representing the key (e.g., 'C', 'am', 'f-sharp').
        """
        # Convert input to lowercase to handle case-insensitivity
        clean_key_name = key_name.lower()
        self.is_minor = False
        
        # Detects if it's minor
        if clean_key_name.endswith('m'):
            clean_key_name = clean_key_name[:-1]
            self.is_minor = True
        self.mode = 'minor' if self.is_minor else 'major'

        # Normalize the key_name using the mapping
        # If the key is in the map, use the mapped value; otherwise, use the original key
        self.root_note = self._key_name_mapping.get(clean_key_name, clean_key_name)
        
        # Fallback to the original input if not in mapping, and capitalize
        if self.root_note not in self._api_mapping:
            self.api_name = flip_accidentals(self.root_note)
        else:
            self.api_name = self.root_note

        scales_data = sg.run() # Generates scales / chords / relatives data
        # print(self.root_note, self.api_name)

        # Then, check if the normalized key exists in the comprehensive dictionary
        if self.api_name in scales_data:
            self.scale = scales_data[self.api_name]['scale'][self.mode]
            self.chords = scales_data[self.api_name]['chords'][self.mode]
            self.relative = scales_data[self.api_name]['relative'][self.mode]
        else:
            self.scale = None
            self.chords = None
            self.relative = None
            

def solfeggio(key_name):
    # Create a mapping for name variations
    key_mapping = {
        # Spanish
        # 'A': 'La',  'B': 'Si', 'C': 'Do', 'D': 'Re',
        # 'E': 'Mi', 'F': 'Fa', 'G': 'Sol',
        # 'b': 'Bemol', '#': 'Sostenido',
        # 'm': ' Menor', 'M': ' Mayor'

        # English
        'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D',
        'E': 'E', 'F': 'F','G': 'G',
        'b': '-flat', '#': '-sharp',
        'm': ' Minor', 'M': ' Major'
    }

    output = []
    input = list(key_name)
    # is_minor = False
    
    if key_name.endswith('m'):
        input.remove('m')
        # is_minor = True
    
    for v in input:
        output.append(key_mapping.get(v, v))
    # if is_minor:
    #     output.append(key_mapping['m'])
    # else:
    #     output.append(key_mapping['M'])

    # return ' '.join(output)
    return ''.join(output)

def get_url(key_name):
    key_mapping = {
        'b': '-flat',
        '#': '-sharp'
        }
    url = []
    for v in key_name:
        url.append(key_mapping.get(v, v))
    return ''.join(url).lower()

def flip_accidentals(key_name):
    acc_mapping = {
        # Pitch classes
        'A#': 'Bb',
        'B#': 'C',
        'C#': 'Db',
        'D#': 'Eb',
        'E#': 'F',
        'F#': 'Gb',
        'G#': 'Ab',
        'Ab': 'G#',
        'Bb': 'A#',
        'Cb': 'B',
        'Db': 'C#',
        'Eb': 'D#',
        'Fb': 'E',
        'Gb': 'F#',
        # API like
        'a-sharp': 'b-flat',
        'b-sharp': 'c',
        'c-sharp': 'd-flat',
        'd-sharp': 'e-flat',
        'e-sharp': 'f',
        'f-sharp': 'g-flat',
        'g-sharp': 'a-flat',
        'a-flat': 'g-sharp',
        'b-flat': 'a-sharp',
        'c-flat': 'b',
        'd-flat': 'c-sharp',
        'e-flat': 'd-sharp',
        'f-flat': 'e',
        'g-flat': 'f-sharp'
    }
    return acc_mapping.get(key_name, key_name)

# Call to the API
def get_scale_data(key_name):
    """
    Makes a GET request to the local API and returns JSON data.

    Args:
        key_name (str): The name of the musical key (e.g., 'c-sharp').

    Returns:
        dict: The JSON data from the API response, or None if an error occurs.
    """
    api_url = 'http://127.0.0.1:5000/api/'
    url = f'{api_url}scale/{key_name}'
        
    try:
        # Make the GET request
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        response.raise_for_status()
        
        # Return the JSON data as a Python dictionary
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error when making the request: {e}")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON from the response.")
        return None
    
if __name__ == '__main__':
    # Example usage:
    key = 'c-sharp'
    data = get_scale_data(key)
    print(data)
    solfeo = solfeggio('C#')
    print(data)
    url = 'F'
    print(get_url(url))