import { Fetch } from "./fetch.js";
class NvabarContorller {
    constructor() {
        // 宣告物件
        this.fetch = new Fetch();
        this._register();
    }

    async _register() {
        const self = this;
        //  check login
        const isLogin = await this.fetch.GET("/user/isLogin/");
        if (isLogin) {
            $(".navbar .navbar-user").off("click");
            this._get_show_data();
        }
        else {
            this.notLoggedIn();
        }
        // 監聽
        self._linter();
    }

    _linter() {
        const self = this;
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        // console.log(urlParams.get('query'))
        $('#query').val(urlParams.get('query'));

        $('#logout').on("click", function () {
            sessionStorage.removeItem("user_data");
            sessionStorage.removeItem("user_playlist");
            sessionStorage.setItem("isData", false);
        });
    }

    async _get_show_data() {
        const self = this;
        var isData = sessionStorage.getItem('isData');
        // isData = false
        if ((isData !== undefined) && (isData)) {
            this.show();
        } else {
            const getUserDataResponse = await self.fetch.POST("/user/get_user_show_data/");
            console.log(getUserDataResponse);
            sessionStorage.setItem("isData", true);
            sessionStorage.setItem("user_data", JSON.stringify(getUserDataResponse.user_data));
            sessionStorage.setItem("user_playlists", JSON.stringify(getUserDataResponse.user_playlists));
            // console.log(sessionStorage.getItem('user_data'));
        }
    }



    _navbar_tmplate(playlist, title, iconClass) {
        return ` <li>
        <a
          class="dropdown-item"
          href="/music/my_music_list?music_list=${playlist}"
        >
         <i class="${iconClass}"></i>
          <span class="text">${title}</span></a>
      </li>`;
    }

    show = () => {
        const self = this;

        // playlist
        const playlists = JSON.parse(sessionStorage.getItem('user_playlists'));
        $('.navbar .navbar-playlist .navbar-body').append(playlists.map(function (playlist) {
            return self._navbar_tmplate(playlist, playlist, "fa-solid fa-record-vinyl");
        }));

        // user
        const user_data = JSON.parse(sessionStorage.getItem('user_data'));
        console.log(user_data);
        $('.navbar .navbar-user .username').html(user_data.username);
        $('.navbar .navbar-user .dropdown-item').removeClass('disabled');



    }

    notLoggedIn = () => {
        $('.navbar .navbar-user .dropdown-item').addClass('disabled');
        $('.navbar .navbar-user  .navbar-body').css("display", "none");
        $(".navbar .navbar-user").on("click", () => {
            location.href = '/user/login/';
        });

        $('.navbar .navbar-playlist a').addClass('disabled');
        $('.navbar .navbar-discover a').addClass('disabled');
    }
}


$('document').ready(function () {
    const nav = new NvabarContorller();
});