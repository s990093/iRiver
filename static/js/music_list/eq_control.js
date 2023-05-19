import { Eq } from "./eq.js";
import { Fetch } from "../fetch.js";
import { SessionController } from "../session.js";

export class EqController {
    constructor(audioElement, isTest = false) {
        this.isTest = isTest;
        this.audioElement = audioElement;

        this.dB = 5;
        this.target = "/user/get_user_eq_setting/";
        this.config = {};

        //宣告物件
        this.fetch = new Fetch();
        this.sessionController = new SessionController();
        this.eq = new Eq(this.audioElement, this.isTest);

        if (this.isTest)
            console.log('eqcontroller');


        this._register();
    }

    async _register() {
        const user_eq = this.sessionController.get('user_eq');
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

    }

    _show() {

    }

    _lienter_audio_enhancement() {
        $('#HighGain').on('change', () => {
            var highGainStatus = $('#HighGain').prop('checked');
            if (highGainStatus)
                this.eq.setHighGain(this.dB);
            else
                this.eq.setHighGain(0);

            if (this.isTest)
                console.log('高音增強：', highGainStatus);
        });

        $('#MidGain').on('change', () => {
            var midGainStatus = $('#MidGain').prop('checked');
            if (midGainStatus)
                this.eq.setMidGain(this.dB);
            else
                this.eq.setMidGain(0);

            if (this.isTest)
                console.log('中音增強：', midGainStatus);
        });

        $('#LowGain').on('change', () => {
            var lowGainStatus = $('#LowGain').prop('checked');
            if (lowGainStatus) {
                this.eq.setLowGain(this.dB);
                // this.eq.setLowStere(this.dB);
            } else {
                this.eq.setLowGain(0);
                // this.eq.setLowStereo(0);
            }


            if (this.isTest)
                console.log('低音增強：', lowGainStatus);
        });

        $('#BoostLowGain').on('change', () => {
            var boostLowGainStatus = $('#BoostLowGain').prop('checked');
            if (boostLowGainStatus)
                this.eq.setSuperBass(this.dB);
            else
                this.eq.setSuperBass(0);

            if (this.isTest)
                console.log('超低音增強：', boostLowGainStatus);
        });
    }

    _lienter_audio_style() { }

    _push(column, new_value) {
        const params = { method: "update", kwargs: { column: column, new_value: new_value } };
        this.fetch.POST(this.push_traget, params);
    }
}