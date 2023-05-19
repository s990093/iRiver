import { Fetch } from "./fetch.js";
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
        // 物件宣告
        this.fetch = new Fetch();

        // Retrieve session data from sessionStorage
        let session = JSON.parse(sessionStorage.getItem("session"));

        // Initialize session if it's undefined or null
        if (session === undefined || session === null) {
            session = [];
            sessionStorage.setItem("session", JSON.stringify(session));
        }


        this._listener();
    }

    _listener() {
        const self = this;
        $('#logout').on("click", function () {
            // self.clear();
        });
    }

    /**
     * Add an item to the session.
     * @param {object} item - The item to be added to the session
     * @param {any} title - The session title
     * .
     */
    add = (title, item) => {
        let session = JSON.parse(sessionStorage.getItem("session"));

        // Add item to the session array
        session.push(title);

        // Update session data in sessionStorage
        sessionStorage.setItem("session", JSON.stringify(session));

        // Store item separately in sessionStorage using its value as the key
        sessionStorage.setItem(title, JSON.stringify(item));
    }
    /**
     * Update the value of a specific item in the session.
     * @param {any} item - The item to be updated in the session.
     */
    update = (item) => {
        let session = JSON.parse(sessionStorage.getItem("session"));

        // Iterate through each item in the session array
        session.map((it) => {
            if (it == item) {
                // Update the value of the item in sessionStorage
                sessionStorage.setItem(item, JSON.stringify(item));
            }
        });
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
            console.log(item, this.get(item));
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

    /**
     * Fetches all user sessions from the server and updates the session data.
     * @async
     */
    fetch_all_session = async () => {
        // Define the target URL for the request
        const target = "/user/get_user_session/";

        // Define the request parameters
        const params = { get: "all" };

        // Send a POST request to fetch user data
        const user_data = await this.fetch.POST(target, params);

        // Check if the request was successful
        if (user_data.success) {
            Object.entries(user_data.data).forEach(([name, value]) => {
                this.add(name, value);
            });

            // Display the updated session data
            this.show();

            //  test
            this.clear();
        }
    }

}

