import { Fetch } from "../../../static/js/fetch.js";
import { error } from "../../../static/js/error.js";


class User_setting {
    constructor(name) {
        this.fetch = new Fetch();
        this._register()
    }

    _register = () => {
        this._listener();
    }

    _listener = () => { }
}


const user_setting = new User_setting();