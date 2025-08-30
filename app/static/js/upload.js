// This script handles the file upload interactions for the Key Detector page,
// including both traditional file selection and drag-and-drop.

document.addEventListener('DOMContentLoaded', function() {
    const dropArea = document.getElementById('drop-area');
    const audioFile = document.getElementById('audioFile');
    
    dropArea.addEventListener('click', function(event) {
    // Check if the click event originated from the label or a child element
    // of the label. The `event.target` property will tell you which element
    // was clicked.
    if (event.target.tagName !== 'LABEL' && event.target.closest('label') === null) {
        audioFile.click();
    }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Get references to all necessary DOM elements.
    const dropArea = document.getElementById('drop-area');
    const audioFile = document.getElementById('audioFile');
    const uploadForm = document.getElementById('uploadForm');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const resultBox = document.getElementById('resultBox');
    const messageBox = document.getElementById('messageBox');
    const messageText = document.getElementById('messageText');
    const playerBox = document.getElementById('playerBox');
    const resetButton = document.getElementById('resetButton');
    const audioPlayerElement = document.getElementById('audioPlayer');
    const scaleLink = document.getElementById('scaleLink');
    const audioFilename = document.getElementById('audioFilename');

    // Function to show a message in the dedicated message box.
    function showMessage(message, type) {
        messageText.textContent = message;
        messageBox.classList.remove('hidden');

        // Set colors based on message type (e.g., 'error' or 'success').
        if (type === 'error') {
            messageBox.classList.remove('border-green-400', 'bg-green-50', 'text-green-800');
            messageBox.classList.add('border-red-400', 'bg-red-50', 'text-red-800');
        } else {
            messageBox.classList.remove('border-red-400', 'bg-red-50', 'text-red-800');
            messageBox.classList.add('border-green-400', 'bg-green-50', 'text-green-800');
        }
    }

    function capitalize(s) {
        if (typeof s !== 'string' || s.length === 0) {
            return '';
        }
        return s.charAt(0).toUpperCase() + s.slice(1);
    }

    // Function to handle the file upload process, which now automatically calls the API.
    async function processFile(file) {
        // Hide previous results and messages before processing.
        resultBox.classList.add('hidden');
        messageBox.classList.add('hidden');
        loadingIndicator.classList.remove('hidden');

        // Show the player and reset button immediately.
        handleFileSelected(file);

        const formData = new FormData();
        formData.append('audio', file);
        audioFilename.textContent = file.name; // Display the filename

        try {
            // Send the audio file to the Flask backend for key detection.
            const response = await fetch('/api/detect', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();

            // Check if the response was successful.
            if (response.ok) {
                // On success, check if a key was actually detected
                const detectedPitch = capitalize(result.pitch) + ' ' + capitalize(result.mode);
                document.getElementById('detectedPitch').textContent = detectedPitch;
                resultBox.classList.remove('hidden');

                // Set the button's link and show it
                const redirectUrl = `/scale/detected/${result.pitch.replace(' ', '_')}_${result.mode}`;
                scaleLink.href = redirectUrl;
                scaleLink.classList.remove('hidden');
            } else {
                // Display a detailed error message from the server.
                showMessage(result.error || "An error occurred.", 'error');
                resetApp();
                messageBox.classList.remove('hidden');
            }
        } catch (error) {
            // Handle network or other unexpected errors.
            console.error("Error:", error);
            showMessage("Failed to connect to the server. Please try again later.", 'error');
            resetApp();
            messageBox.classList.remove('hidden');
        } finally {
            // Always hide the loading indicator.
            loadingIndicator.classList.add('hidden');
        }
    }

    // Function to handle file selection and update UI, without calling the API.
    function handleFileSelected(file) {
        // Create a temporary URL for the uploaded file to be used in the audio player.
        const audioUrl = URL.createObjectURL(file);
        audioPlayerElement.src = audioUrl;

        // Hide the upload form and show the result/player box.
        uploadForm.classList.add('hidden');
        playerBox.classList.remove('hidden');
        resultBox.classList.add('hidden');
        messageBox.classList.add('hidden');
    }

    // Function to reset the application state
    function resetApp() {
        uploadForm.classList.remove('hidden');
        resultBox.classList.add('hidden');
        playerBox.classList.add('hidden');
        messageBox.classList.add('hidden');
        scaleLink.classList.add('hidden');
        audioPlayerElement.pause(); // Stop the audio playback
        audioPlayerElement.currentTime = 0; // Rewind the audio to the beginning
        audioFile.value = ''; // Clear the file input
    }

    // --- Event Listeners for Drag and Drop and File Selection ---

    // Add visual feedback when a file is dragged over the drop area.
    dropArea.addEventListener('dragover', (event) => {
        event.preventDefault();
        dropArea.classList.add('border-blue-600', 'bg-blue-50');
    });

    // Remove visual feedback when a file leaves the drop area.
    dropArea.addEventListener('dragleave', () => {
        dropArea.classList.remove('border-blue-600', 'bg-blue-50');
    });

    // Handle the file drop event.
    dropArea.addEventListener('drop', (event) => {
        event.preventDefault();
        dropArea.classList.remove('border-blue-600', 'bg-blue-50');
        const droppedFiles = event.dataTransfer.files;
        if (droppedFiles.length > 0) {
            audioFile.files = droppedFiles;
            processFile(droppedFiles[0]); // Automatically call API
        }
    });

    // Handle traditional file selection.
    audioFile.addEventListener('change', (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            processFile(selectedFile); // Automatically call API
        }
    });

    // --- Event Listener for the Reset Button ---
    resetButton.addEventListener('click', resetApp);
});