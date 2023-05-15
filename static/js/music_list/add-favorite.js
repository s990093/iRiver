import { Fetch } from "../../js/fetch.js";
/**
 * FaController class for managing Fa functionality.
 * @class
 */

export class FaController {
    /**
     * Create a new instance of FaController.
     * @constructor
     * @param {HTMLElement} element - The target element.
     */
    constructor(isTest = false) {
        this.isTest = isTest;
        this.playlist = [];
        // 宣告物件
        this.fetch = new Fetch();
        this._register();
    }

    /**
     * @method register the favortiet  mmodel 
     */
    _register() {
        this._listener();
        this.playlist = this._get_playlist();
    }

    _listener() {
        var a = document.getElementById("#add");
        console.log($(".add"))
        $(".add").on("click", function () {
            $("#favoriteModal").modal("show");
        });
    }

    async _get_playlist() {
        return this.fetch.get_playlist();
    }

    playlist_template(playlist) {

    }

    /**
     * show fa model
     * @method
     */
    showFa() {
        // Code to toggle Fa functionality
    }
    /**
    * show fa model
    * @method
    */
    creatFa() {
        // Code to toggle Fa functionality
    }
    /**
     * Enable the Fa functionality.
     * @method
     */
    enableFa() {
        // Code to enable Fa functionality
    }

    /**
     * Disable the Fa functionality.
     * @method
     */
    disableFa() {
        // Code to disable Fa functionality
    }
}
