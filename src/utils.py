import requests
import json

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
    
def solfeggio(key_name):
    # Create a mapping for name variations
    key_mapping = {
        # Spanish
        # 'A': 'La',
        # 'B': 'Si',
        # 'C': 'Do',
        # 'D': 'Re',
        # 'E': 'Mi',
        # 'F': 'Fa',
        # 'G': 'Sol',
        # 'b': 'Bemol',
        # '#': 'Sostenido',
        # 'm': ' Menor',
        # 'M': ' Mayor'

        # English
        'A': 'A',
        'B': 'B',
        'C': 'C',
        'D': 'D',
        'E': 'E',
        'F': 'F',
        'G': 'G',
        'b': '-flat',
        '#': '-sharp',
        'm': ' Minor',
        'M': ' Major'
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

if __name__ == '__main__':
    # Example usage:
    key = 'c-sharp'
    data = get_scale_data(key)
    print(data)
    solfeo = solfeggio('C#')
    print(data)