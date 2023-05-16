import { Fetch } from "../../js/fetch.js";
import { insert_my_music_list } from "../../js/music_list/emement.js";
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
        this.insert_song_infos = {};
        // 宣告物件
        this.fetch = new Fetch();
        this._register();
    }

    /**
     * @method register the favortiet  mmodel 
     */
    _register() {
        this.playlist = this._get_playlist();
        // 監聽 
        this._listener();
    }

    _listener() {
        const self = this;
        // 加入個人專輯

        $(".add").on("click", function () {
            $("#favoriteModal").modal("show");

            self.insert_song_infos = {
                playlist: "我的最愛",
                music_ID: $(this).attr('vaule'),
                favorite: false,
                method: "insert"
            };

            console.log(self.insert_song_infos);
            self.showFa()
        });


        // 我的最愛
        $('.love-icon a').on('click', async function () {
            $(this).find('i').toggleClass('far fas');
            var music_ID = $(this).attr('value');
            // 送出
            insert_my_music_list({
                music_ID: music_ID,
                playlist: "我的最愛",
                favorite: true,
                method: "insert"
            });
        });
    }

    async _get_playlist() {
        const isLogin = await this.fetch.GET("/user/isLogin/");
        if (isLogin) {
            const params = { method: "get_playlists" };
            const target = "/user/get_user_music_list/";
            const response = await this.fetch.POST(target, params);
            console.log(response);
            if (response.statusCode === 200) {
                this.playlist = response.success;
            }
            console.log(this.playlist)
        } else {
            location.href = "/user/login/";
        }
    }

    playlist_template(playlist, isChecked = false) {
        const row = `
        <div class="row">
            <div class="col">
                <label class="playlist mb-3" data-playlist="${playlist}">
                    <input 
                    type="radio" 
                    name="playlist" 
                    id="${playlist}"
                    autocomplete="off" 
                    ${isChecked ? "checked" : ""}
                    >
                    ${playlist}
                </label>
            </div>
        </div>
        `;

        return row;
    }

    /**
     * show fa model
     * @method  onecycle show fa model
     */
    showFa = () => {
        const self = this;
        $(".fa-body").html("");
        $(".fa-body").append(self.playlist_template("我的最愛", true));
        $('.fa-body').append(this.playlist.map(function (playlist) {
            return self.playlist_template(playlist);
        }));


        // 添加到哪個專輯
        $("#favoriteModal").on("click", ".playlist", function () {
            self.insert_song_infos = {
                "playlist": $(this).data('playlist'),
                "music_ID": self.insert_song_infos.music_ID,
                "favorite": self.insert_song_infos.favorite,
                method: "insert"
            }
            console.log(self.insert_song_infos);
        });

        // 送出
        $("#favoriteModal").on("click", ".fa-insert", async function () {
            const success = await insert_my_music_list(self.insert_song_infos);
            console.log(success);
        });

        $(".creat-playlist").on("click", function () {
            self.createFa($('.new-playlist').val());
        });
    }

    createFa(playlist) {
        this.fetch.push_playlist(playlist);
        this.playlist.push(playlist);
        $(".fa-body").append(this.playlist_template(playlist));
    }
}
