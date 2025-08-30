# WhatKeyIsThis-MLOps
An MLOps project for detecting the key of musical fragments from audio. This demo uses the Spotify model `basic_pitch` and showcases a simple MLOps architecture with a Flask-based API and UI.

The web application is designed to analyze audio files and determine their musical key. Users can upload a song or a musical piece, and the application will return the detected tonality (e.g., C Major, A Minor). It also provides functionalities to generate musical scales and their corresponding chords.

This tool is perfect for musicians, music students, and producers who want to quickly identify the key of a song or explore music theory concepts.

## Features

* **Musical Key Detection**: Upload an audio file (`.wav`, `.mp3`) to detect its key.
* **Scale and Chord Generation**: Provides information about major and minor scales, including the notes and diatonic chords for each key.
* **Web Interface**: A simple and user-friendly interface to interact with the detection engine.
* **REST API**: Exposes endpoints for programmatic access to the key detection and scale generation features.

## Project Structure

The project is organized into several directories to separate concerns:
```
.
├── app/
│   ├── static/
│   │   ├── css/layout.css
│   │   ├── images/
│   │   │   └── output/
│   │   └── js/
│   │       ├── scale.js
│   │       └── upload.js
│   ├── templates/
│   │   ├── index.html
│   │   ├── upload.html
│   │   └── ...
│   ├── __init__.py
│   ├── api.py
│   └── app.py
├── src/
│   ├── __init__.py
│   ├── pitch_detector.py
│   ├── scales_generator.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_app.py
│   ├── test_pitch_detector.py
│   ├── test_scales_generator.py
│   └── test_utils.py
├── .gitignore
├── README.md
└── requirements.txt
````

* `app/`: Contains the Flask web application, including static files (CSS, JS, images), HTML templates, and the main application logic (`app.py` and `api.py`).
* `src/`: The core logic for music theory operations resides here.
    * `pitch_detector.py`: Uses the `basic-pitch` library to analyze audio and identify the most prominent notes and chords.
    * `scales_generator.py`: Generates musical scales, chords, and relative keys.
* `tests/`: Includes unit tests for the core logic to ensure correctness.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

This project requires Python >= 3.6, < 3.12 and pip.

### Installation
1.  **Clone the repository:**
    ```sh
    git clone https://github.com/MLsound/WhatKeyIsThis-MLOps.git
    cd WhatKeyIsThis
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
    *(Note: You will need to create a `requirements.txt` file. Based on your code, it should include `Flask`, `basic-pitch`, and `pytest`)*

4.  **Reset virtual environment:**
    ```sh
    deactivate source
    source .venv/bin/activate
    ```

### Running the Application

1.  **Start the Flask server:**
    ```sh
    flask run
    ```
    Or directly run the main application file:
    ```sh
    python app/app.py
    ```

2.  **Open your browser** and navigate to [`http://127.0.0.1:5000`](http://127.0.0.1:5000).

## Usage

### Web Interface

1.  Navigate to the home page.
2.  Go to the "Key listener" page.
3.  Upload your audio file using the form (supported formats are MP3, WAV, OGG, and FLAC, with a maximum size of 10MB).
4.  The application will process the file and display the possible musical keys.
5. Click on 'Show scale' to view the notes, chords, and musical score for that tonality.
6. For other scales, navigate to the "Scales" page and click on a key on the virtual keyboard.

### UI Endpoints
The web interface is built around several routes that serve different pages.

* Scale Details: `GET /scale/<key_name>`
    * `<key_name>`: The musical key (e.g., `c`, `d-flat`, `f-sharp`).
    * `?mode=<mode>`: _(Optional)_ The scale's mode. If `?mode=minor` is included, the minor scale is displayed. The default is major.

* Detected Scale: `GET /scale/detected/<pitch>`
    * `<pitch>`: The detected pitch string from the API (e.g., `g_major`, `e-flat_minor`).
    * This endpoint redirects to the Scale Details page with the correct "key_name" and mode parameters.

### API Endpoints

The application also provides a REST API for developers.

* **Detect Key**: `POST /api/detect`
    * Send a `POST` request with a multipart/form-data payload containing the audio file under the key `audio`.
    * **Success Response (200)**:
        ```json
        {
        "pitch": "G",
        "mode": "major"
        }
        ```
    * **Error Response (400/500)**:
        ```json
        {
          "error": "Error message details."
        }
        ```

* **Get Scale Information**: `GET /api/scale/<key_name>`
    * Replace `<key_name>` with the desired musical key (e.g., 'f-sharp`).
    * **Success Response (200)**: Returns a JSON object with notes, chords, enharmonic equivalents, and relative keys.
        ```json
        {
            "root": "C",
            "enharmonic": "C",
            "is_flat": false,
            "mode": "major",
            "scale": [
                "C", "D", "E", "F", "G", "A", "B"
            ],
            "chords": [
                "C", "Dm", "Em", "F", "G", "Am", "Bdim"
            ],
            "relative": "Am"
        }
        ```

# Acknowledgements
The core audio analysis capability of this project is powered by Spotify's Basic Pitch library:
* [Basic Pitch: A lightweight yet powerful audio-to-MIDI converter](https://basicpitch.spotify.com/)