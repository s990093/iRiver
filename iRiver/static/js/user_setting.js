import { Fetch } from "../../../static/js/fetch.js";
import { SessionController } from "./../../../static/js/session.js";
import { error } from "../../../static/js/error.js";

/**
 * Create a new instance of User_setting.
 * @constructor
 * @param {string} name - The name of the User_setting.
 * @param {data} user_setting  - The user setting object data 

 */

class User_setting {
    constructor() {
        // 物件宣告
        this.fetch = new Fetch();
        this.sessionController = new SessionController();

        this._register()
        this.traget = "/user/get_user_session/";
    }

    _register = () => {
        const user_setting = this.sessionController.get('user_setting');
        if (user_setting !== undefined && user_setting !== null) {
            this._show();
        }

        const params = { get: "user_setting" };
        const response = this.fetch.POST(this.traget, params);
        if (response.status === 200) {
            sessionStorage.setItem("user_setting", response.data.user_setting);
            this._show();
        }
        this._listener();
    }

    _listener = () => { }

    _show = () => {


    }
}


const user_setting = new User_setting();