/**
 * Logs a link click by sending a POST request to the server with the link URL.
 *
 * This function extracts the URL of the clicked link and sends it to the
 * '/log_magazine_click' endpoint on the server for logging purposes. It includes a
 * CSRF token in the request headers to protect against cross-site request forgery attacks.
 *
 * @param {Event} event - The click event triggered by the user.
 *
 * Usage:
 * <a href="https://example.com" onclick="logClick(event)">Example.com</a>
 *
 * HTML template setup:
 * <meta name="csrf-token" content="{{ csrf_token() }}">
 * <a href="https://example.com" onclick="logClick(event)">Example.com</a>
 * <a href="https://google.com" onclick="logClick(event)">Google.com</a>
 */
function log_click(event) {
    const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const link = event.target.href;
    fetch('/log_magazine_click', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token  // Include the CSRF token in the headers
        },
        body: JSON.stringify({ link: link })
    })
        .then(response => response.json())
        .catch(error => console.error('Error logging click:', error));
}