import { Fetch } from "./fetch.js";
import { PlaylistController } from "./playlist.js";
import { SessionController } from "./session.js";

class NvabarContorller {
    constructor() {
        // 宣告物件
        this.fetch = new Fetch();
        this.sessionController = new SessionController(true);
        this.playlistController = new PlaylistController();
        this._register();
    }

    async _register() {
        const self = this;
        const user_data = this.sessionController.get("user_data");
        const isLogin = await this.fetch.GET("/user/isLogin/");
        // console.log(sessionStorage.getItem("user_playlist") != null && sessionStorage.getItem("user_playlist") != undefined)
        if (user_data != null && user_data != undefined) {
            self.show();
        } else {
            if (isLogin) {
                this.sessionController.fetch_all_session();
            }
        }
        //  check login
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
            console.log("remove session")
            sessionStorage.removeItem("user_data");
            sessionStorage.removeItem("user_playlist");
        });

        $('.navbar .navbar-playlist').on("click", async function () {
            self._get_show_data();
        });

    }

    async _get_show_data() {
        const getUserDataResponse = await this.fetch.POST("/user/get_user_show_data/");
        // console.log(getUserDataResponse);
        // this.user_data = getUserDataResponse.user_data;
        // this.user_playlists = getUserDataResponse.user_playlists;
        // console.log(this.user_playlists);

        sessionStorage.setItem("isData", true);
        sessionStorage.setItem("user_data", JSON.stringify(getUserDataResponse.user_data));
        sessionStorage.setItem("user_playlists", JSON.stringify(getUserDataResponse.user_playlists));
        // console.log(sessionStorage.getItem('user_data'));

        // show
        this.show();
        this.playlistController.push_playlist(getUserDataResponse.user_playlists);
    }



    _navbar_tmplate(playlist, title, iconClass) {
        return ` <li>
        <a
          class="dropdown-item"
          href="${playlist}"
        >
         <i class="${iconClass}"></i>
          <span class="text">${title}</span></a>
      </li>`;
    }

    show = () => {
        $('.navbar .navbar-user .dropdown-item').removeClass('disabled');
        $('.navbar .navbar-playlist .dropdown-item').removeClass('disabled');
        const self = this;

        // playlist
        const playlists = JSON.parse(sessionStorage.getItem('user_playlists'));
        // console.log(playlists);
        $('.navbar .navbar-playlist .navbar-body').html("");
        // console.log((playlists != null));
        if ((playlists != null) || (playlists != undefined)) {
            $('.navbar .navbar-playlist .navbar-body').append(playlists.map(function (playlist) {
                return self._navbar_tmplate(`/music/my_music_list?music_list=${playlist}`, playlist, "fa-solid fa-record-vinyl");
            }));
        } else {
            $('.navbar .navbar-playlist .navbar-body').append(
                self._navbar_tmplate("/music/discover/", "去聽歌!", "")
            );

        }

        // user
        const user_data = JSON.parse(sessionStorage.getItem('user_data'));
        // console.log(user_data);
        $('.navbar .navbar-user .username').html(user_data.name);
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