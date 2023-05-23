import { Eq } from "./eq.js";
import { Fetch } from "../fetch.js";
import { SessionController } from "../session.js";

export class EqController {
    constructor(audioElement, isTest = false) {
        this.isTest = isTest;
        this.audioElement = audioElement;

        this.dB = 5;
        this.traget = "/user/get_user_session/";
        this.push_traget = "/user/user_eq/";

        //宣告物件
        this.fetch = new Fetch();
        this.sessionController = new SessionController();
        this.eq = new Eq(this.audioElement, this.isTest);

        if (this.isTest)
            console.log('eqcontroller');

        // 變數
        this.config = this.sessionController.get('user_eq');
        this._register();
    }

    async _register() {
        const user_eq = this.sessionController.get('user_eq');
        //console.log(user_eq)
        if (user_eq !== undefined && user_eq !== null) {
            this._show();
        }
        const params = { get: "user_eq" };
        const traget = "/user/get_user_session/";
        const response = await this.fetch.POST(traget, params);
        if (response.status === 200) {
            this.sessionController.update("user_eq", response.data.user_setting)
            this.sessionController.show();
            this._show();
        }

        this._listener();
    }

    _listener() {
        this._lisenter_element();
        this._lienter_audio_enhancement();
        this._lienter_audio_style();
    }

    _lisenter_element() {
        const self = this;
    }

    _show() {
        const user_EQ = this.config;

        // high
        if (user_EQ.ENGANCE_HIGH) {
            $('#HighGain').prop('checked', true);
        } else {
            $('#HighGain').prop('checked', false);
        }

        // middle
        if (user_EQ.ENGANCE_MEDDLE) {
            $('#MedGain').prop('checked', true);
        } else {
            $('#MedGain').prop('checked', false);
        }


        // low
        if (user_EQ.ENGANCE_LOW) {
            $('#LowGain').prop('checked', true);
        } else {
            $('#LowGain').prop('checked', false);
        }


        // heavy
        if (user_EQ.ENGANCE_HEAVY) {
            $('#HeavyLowGain').prop('checked', true);
        } else {
            $('#HeavyLowGain').prop('checked', false);
        }

    }

    _lienter_audio_enhancement() {
        const self = this;
        $('#HighGain').unbind("click").on('change', function (event) {
            var highGainStatus = $(event.target).prop('checked');
            if (highGainStatus) {

                self.eq.setHighGain(self.dB);
            }
            else {

                self.eq.setHighGain(0);
            }

            // push data
            self._push("ENGANCE_HIGH", highGainStatus);

            if (self.isTest)
                console.log('高音增強：', highGainStatus);
        });

        $('#MidGain').unbind("click").on('change', function (event) {
            var midGainStatus = $(event.target).prop('checked');
            if (midGainStatus)
                self.eq.setMidGain(self.dB);
            else
                self.eq.setMidGain(0);

            // push data
            self._push("ENGANCE_MIDDLE", midGainStatus);

            if (self.isTest)
                console.log('中音增強：', midGainStatus);
        });

        $('#LowGain').on('change', function (event) {
            var lowGainStatus = $(event.target).prop('checked');
            if (lowGainStatus) {
                self.eq.setLowGain(self.dB);
                // this.eq.setLowStere(this.dB);
            } else {
                self.eq.setLowGain(0);
                // this.eq.setLowStereo(0);
            }

            // push data
            self._push("ENGANCE_LOW", lowGainStatus);

            if (self.isTest)
                console.log('低音增強：', lowGainStatus);
        });

        $('#HeavyLowGain').on('change', function (event) {
            var boostLowGainStatus = $(event.target).prop('checked');
            if (boostLowGainStatus)
                self.eq.setSuperBass(self.dB);
            else
                self.eq.setSuperBass(0);

            // push data
            self._push("ENGANCE_HEAVY", boostLowGainStatus);

            if (self.isTest)
                console.log('超低音增強：', boostLowGainStatus);
        });
    }

    _lienter_audio_style() { }


    _update() {

    }

    _push(column, new_value) {
        const params = { method: "update", kwargs: { column: column, new_value: new_value } };
        this.fetch.POST(this.push_traget, params);
    }
}