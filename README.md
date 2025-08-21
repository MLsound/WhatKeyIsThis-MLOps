# WhatKeyIsThis-MLOps
An MLOps project for detecting the key of musical fragments from audio. This demo uses an Spotify model (aka `basic_pitch`) and showcases a simple MLOps architecture with a Flask-based API and UI.

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
│   │   ├── css/
│   │   ├── images/
│   │   └── js/
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
│   └── scales_generator.py
├── tests/
│   ├── __init__.py
│   ├── test_pitch_detector.py
│   └── test_scales_generator.py
├── .gitignore
└── README.md
````

* `app/`: Contains the Flask web application, including static files (CSS, JS, images), HTML templates, and the main application logic (`app.py` and `api.py`).
* `src/`: The core logic for music theory operations resides here.
    * `pitch_detector.py`: Uses the `basic-pitch` library to analyze audio and identify the most prominent notes and chords.
    * `scales_generator.py`: Generates musical scales, chords, and relative keys.
* `tests/`: Includes unit tests for the core logic to ensure correctness.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

This project requires Python 3.8+ and `pip`.

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your_username/your_project_name.git](https://github.com/your_username/your_project_name.git)
    cd your_project_name
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

### Running the Application

1.  **Start the Flask server:**
    ```sh
    flask run
    ```
    Or directly run the main application file:
    ```sh
    python app/app.py
    ```

2.  **Open your browser** and navigate to `http://127.0.0.1:5000`.

## Usage

### Web Interface

1.  Navigate to the home page.
2.  Go to the "Key Detection" page.
3.  Upload your audio file using the form.
4.  The application will process the file and display the possible musical keys.

### API Endpoints

The application also provides a REST API for developers.

* **Detect Key**: `POST /api/detect`
    * Send a `POST` request with a multipart/form-data payload containing the audio file under the key `audio`.
    * **Success Response (200)**:
        ```json
        {
          "pitch": ["G Major", "E Minor"]
        }
        ```
    * **Error Response (400/500)**:
        ```json
        {
          "error": "Error message details."
        }
        ```

* **Get Scale Information**: `GET /api/scale/<key_name>`
    * Replace `<key_name>` with the desired musical key (e.g., `C`, `Gm`, `F-sharp`).
    * **Success Response (200)**:
        ```json
        {
            "scale": "C",
            "mode": "major"
        }
        ```
        *(Note: This endpoint can be expanded with the logic from `scales_generator.py` to return full scale and chord data.)*

# Acknowledgements
The core audio analysis capability of this project is powered by Spotify's Basic Pitch library:
* [Basic Pitch: A lightweight yet powerful audio-to-MIDI converter](https://basicpitch.spotify.com/)