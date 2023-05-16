import { Fetch } from "./fetch.js";
class NvabarContorller {
    constructor() {
        // 宣告物件
        this.fetch = new Fetch();
        this.user_data = [];

        this._register();
    }

    _register() {
        const self = this;
        $('document').ready(function () {
            // 監聽
            self._linter();
        });
    }

    _linter() {
        const self = this;
        $('.login').on('click', async function () {
            $.ajax({
                url: '/user/isLogin/',
                method: 'GET',
                success: async function (response) {
                    if (response.isLogin) {
                        const response = await self.fetch.POST("/user/get_user_show_data/");
                        console.log(response);
                    } else {
                        location.href = '/user/login/';
                    }
                }
            });
        });


        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        // console.log(urlParams.get('query'))
        $('#query').val(urlParams.get('query'));

    }
}


const nav = new NvabarContorller();