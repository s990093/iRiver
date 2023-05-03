$(document).ready(function () {
    // Get the user's theme preference from localStorage (default to 'auto' if not set)
    const themePreference = localStorage.getItem('theme') || 'auto';

    // Set the radio button to the user's preference
    $(`input[name=flexRadioDefault][value=${themePreference}]`).prop('checked', true);

    // Apply the user's preference to the page
    applyThemePreference(themePreference);

    // Handle changes to the radio button
    $('input[name=flexRadioDefault]').change(function () {
        const newPreference = this.value;
        applyThemePreference(newPreference);

        // Save the new preference to localStorage
        localStorage.setItem('theme', newPreference);
    });
});


function applyThemePreference(preference) {
    if (preference === 'auto') {
        const currentTime = new Date().getHours(); // Get the current hour
        if (currentTime >= 6 && currentTime < 18) {
            $('body').removeClass('dark-mode');
        } else {
            $('body').addClass('dark-mode');
        }
    } else if (preference === 'light') {
        $('body').removeClass('dark-mode');
    } else if (preference === 'dark') {
        $('body').addClass('dark-mode');
    }
}