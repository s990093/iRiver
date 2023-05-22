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
        console.log(user_eq)
        if (user_eq !== undefined && user_eq !== null) {
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

        // high
        $("#HighGain").on("click", function () { self._push("ENGANCE_HIGH", $(this).val()); });

        // high
        $("#MidGain").on("click", function () { self._push("ENGANCE_MEDDLE", $(this).val()); });

        // high
        $("#LowGain").on("click", function () { self._push("ENGANCE_LOW", $(this).val()); });

        // high
        $("#HeavyLowGain").on("click", function () { self._push("ENGANCE_HEAVY", $(this).val()); });
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
        $('#HighGain').on('change', function (event) {
            var highGainStatus = $(event.target).prop('checked');
            console.log(highGainStatus);
            if (highGainStatus) {

                self.eq.setHighGain(self.dB);
            }
            else {

                self.eq.setHighGain(0);
            }

            // push data
            self._push(self.target, "ENGANCE_HIGH", highGainStatus);

            if (self.isTest)
                console.log('高音增強：', highGainStatus);
        });

        $('#MidGain').on('change', function (event) {
            var midGainStatus = $(event.target).prop('checked');
            if (midGainStatus)
                self.eq.setMidGain(self.dB);
            else
                self.eq.setMidGain(0);

            // push data
            self._push(self.target, "ENGANCE_MEDDIE", midGainStatus);

            if (self.isTest)
                console.log('中音增強：', midGainStatus);
        });

        $('#LowGain').on('change', function (event) {
            var lowGainStatus = $(event.traget).prop('checked');
            if (lowGainStatus) {
                self.eq.setLowGain(self.dB);
                // this.eq.setLowStere(this.dB);
            } else {
                self.eq.setLowGain(0);
                // this.eq.setLowStereo(0);
            }

            // push data
            self._push(self.target, "ENGANCE_LOW", lowGainStatus);

            if (this.isTest)
                console.log('低音增強：', lowGainStatus);
        });

        $('#HeavyLowGain').on('change', function (event) {
            var boostLowGainStatus = $(event.traget).prop('checked');
            if (boostLowGainStatus)
                this.eq.setSuperBass(this.dB);
            else
                this.eq.setSuperBass(0);

            // push data
            self._push(self.target, "ENGANCE_HEAVY", boostLowGainStatus);

            if (this.isTest)
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