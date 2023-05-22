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
        this.traget = "/user/get_user_session/";
        this.push_traget = "/user/user_setting/";

        // 物件宣告
        this.fetch = new Fetch();
        this.sessionController = new SessionController();
        this.user_setting = this.sessionController.get("user_setting");
        this._register()
    }

    _register = async () => {
        const user_setting = this.sessionController.get('user_setting');
        if (user_setting !== undefined && user_setting !== null) {
            this._show();
        }

        const params = { get: "user_setting" };
        const response = await this.fetch.POST(this.traget, params);
        if (response.status === 200) {
            this.sessionController.update("user_setting", response.data.user_setting)
            this.sessionController.show();
            this._show();
        }

        this._listener();
    }

    _listener = () => {
        const self = this;
        // language
        $("#language").on("change", function () {
            self._push("LANGUAGE", $(this).val());
        });

        // color mode
        $("#color-mode input[name='flexRadioDefault']").on("change", function () {
            self._push("SHOW_MODAL", $(this).val());

        });

        // audio quality
        $("#audio-quality").on("change", function () {
            self._push("AUDIO_QUALITY", $(this).val());
        });

        // auto play
        $('#auto-play').on('change', function () {
            if ($(this).is(':checked')) {
                self._push("AUDIO_AUTO_PLAY", true);
            } else {
                self._push("AUDIO_AUTO_PLAY", false);
            }
        });
    }

    _show = () => {
        const self = this;

        // language
        const language = {
            ch: "繁體中文",
            en: "english",
            ja: "日本"
        };
        // console.log(self.user_setting.LANGUAGE);
        const selectedLanguage = language[self.user_setting.LANGUAGE];
        $('#language option:selected').text(selectedLanguage);
        $(`#language option[value="${self.user_setting.LANGUAGE}"]`).text("繁體中文");
        // change vaule
        $('#language option:selected').val(self.user_setting.LANGUAGE);
        $(`#language option[value="${self.user_setting.LANGUAGE}"]`).val("ch");


        // color mode
        $(`#color-mode option[value="${self.user_setting.SHOW_MODAL}"]`).prop('selected', true);

        // audio quality 
        const AUTO_QUALITY = self.user_setting.AUDIO_QUALITY;
        $('#audio-quality option:selected').text(AUTO_QUALITY);
        $(`#audio-quality option[value="${AUTO_QUALITY}"]`).text("320k");
        // change vaule
        $('#audio-quality option:selected').val(AUTO_QUALITY);
        $(`#audio-quality option[value="${AUTO_QUALITY}"]`).val("320k");

        // auto play
        if (self.user_setting.AUDIO_AUTO_PLAY) {
            $('#audio-quality').prop('checked', true);
        } else {
            $('#audio-quality').prop('checked', false);
        }

    }

    _push(column, new_value) {
        const params = { method: "update", kwargs: { column: column, new_value: new_value } };
        this.fetch.POST(this.push_traget, params);
    }
}



const user_setting = new User_setting();