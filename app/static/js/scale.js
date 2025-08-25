// This script handles the Scale page buttos for changing URL parameters (mode)
document.addEventListener('DOMContentLoaded', function() {
    const toggleSharpFlat = document.getElementById('toggle_sharp_flat');
    const toggleMajorMinor = document.getElementById('toggle_major_minor');
    const toggleRelative = document.getElementById('toggle_relative');

    // Function to update URL parameters
    function updateUrlParameter(url, key, value) {
        console.log(`Updating URL: current=${url}, key=${key}, value=${value}`);
        const newUrl = new URL(url);
        newUrl.searchParams.set(key, value);
        console.log(`New URL: ${newUrl.toString()}`);
        return newUrl.toString();
    }

    // Event listener for the Sharp/Flat button
    if (toggleSharpFlat) {
        toggleSharpFlat.addEventListener('click', function(e) {
            e.preventDefault();
            const enharmonic = toggleSharpFlat.dataset.enharmonic;
            const baseUrl = window.location.origin;
            const currentUrl = new URL(window.location.href);
            const currentSearchParams = currentUrl.search;
            console.log(`Search params: ${currentSearchParams}`);
            const newUrl = `${baseUrl}/scale/${enharmonic}${currentSearchParams}`;
            console.log(`Sharp/Flat button clicked. Redirecting to: ${newUrl}`);
            window.location.href = newUrl;
        });
    }

    // Event listener for the Major/Minor button
    if (toggleMajorMinor) {
        toggleMajorMinor.addEventListener('click', function(e) {
            e.preventDefault();
            const currentUrl = window.location.href;
            const currentMode = toggleMajorMinor.dataset.mode;
            const newMode = currentMode === 'minor' ? 'major' : 'minor';
            console.log(`Major/Minor button clicked. Current mode: ${currentMode}, New mode: ${newMode}`);
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
            const baseUrl = window.location.origin;
            const newUrl = `${baseUrl}/scale/${relativeKey}`;
            console.log(`Relative button clicked. Redirecting to: ${newUrl}`);
            window.location.href = updateUrlParameter(newUrl, 'mode', newMode);
        });
    }
});
