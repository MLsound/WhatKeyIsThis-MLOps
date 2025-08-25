// This script handles the Scale page buttos for changing URL parameters (mode, is_flat)
document.addEventListener('DOMContentLoaded', function() {
    const toggleSharpFlat = document.getElementById('toggle_sharp_flat');
    const toggleMajorMinor = document.getElementById('toggle_major_minor');
    const toggleRelative = document.getElementById('toggle_relative');

    // Function to update URL parameters
    function updateUrlParameter(url, key, value) {
        const newUrl = new URL(url);
        newUrl.searchParams.set(key, value);
        return newUrl.toString();
    }

    // Event listener for the Sharp/Flat button
    if (toggleSharpFlat) {
        toggleSharpFlat.addEventListener('click', function(e) {
            e.preventDefault();
            const currentUrl = window.location.href;
            const isFlatState = toggleSharpFlat.dataset.isFlat === 'true';
            const newIsFlatState = isFlatState ? 'false' : 'true';
            window.location.href = updateUrlParameter(currentUrl, 'is_flat', newIsFlatState);
        });
    }

    // Event listener for the Major/Minor button
    if (toggleMajorMinor) {
        toggleMajorMinor.addEventListener('click', function(e) {
            e.preventDefault();
            const currentUrl = window.location.href;
            const currentMode = toggleMajorMinor.dataset.mode.toLowerCase();
            const newMode = currentMode === 'minor' ? 'major' : 'minor';
            window.location.href = updateUrlParameter(currentUrl, 'mode', newMode);
        });
    }

    // Event listener for the Relative button
    if (toggleRelative) {
        toggleRelative.addEventListener('click', function(e) {
            e.preventDefault();
            const relativeKey = toggleRelative.dataset.relative;
            const currentMode = toggleRelative.dataset.mode;
            const newMode = currentMode === 'minor' ? 'major' : 'minor';
            // The relative key is a new URL path, so we build the URL differently
            const baseUrl = window.location.origin;
            const newUrl = `${baseUrl}/scale/${relativeKey}`;
            window.location.href = updateUrlParameter(newUrl, 'mode', newMode);
        });
    }
});