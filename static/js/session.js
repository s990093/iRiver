/**
 * SessionController class for managing session data using sessionStorage.
 */
export class SessionController {
    /**
     * Create a new instance of SessionController.
     * @constructor
     * @param {Object} options - Optional configuration options.
     */
    constructor(options = null) {
        // Retrieve session data from sessionStorage
        let session = JSON.parse(sessionStorage.getItem("session"));

        // Initialize session if it's undefined or null
        if (session === undefined || session === null) {
            session = [];
            sessionStorage.setItem("session", JSON.stringify(session));
        }
    }

    /**
     * Add an item to the session.
     * @param {any} item - The item to be added to the session.
     */
    add = (item) => {
        let session = JSON.parse(sessionStorage.getItem("session"));

        // Add item to the session array
        session.push(item);

        // Update session data in sessionStorage
        sessionStorage.setItem("session", JSON.stringify(session));

        // Store item separately in sessionStorage using its value as the key
        sessionStorage.setItem(item, JSON.stringify(item));
    }

    /**
     * Get the value of a specific item in the session.
     * @param {string} item - The key of the item to retrieve.
     * @returns {any} The value of the requested item.
     */
    get = (item) => {
        // Retrieve and parse the item from sessionStorage
        return JSON.parse(sessionStorage.getItem(item));
    }

    /**
     * Show all items in the session.
     */
    show = () => {
        let session = JSON.parse(sessionStorage.getItem("session"));

        // Display each item in the session array
        session.map((item) => {
            console.log(item);
        });
    }

    /**
     * Clear the session by removing all items.
     */
    clear = () => {
        let session = JSON.parse(sessionStorage.getItem("session"));

        // Remove each item from sessionStorage
        session.forEach((item) => {
            sessionStorage.removeItem(item);
        });

        // Clear the session array from sessionStorage
        sessionStorage.removeItem("session");
    }
}
