import { Fetch } from "../../js/fetch.js";
import { error } from "../error.js";
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
        this.target = "/user/get_user_music_list/";
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
            self.pushFa();
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
            if (response.data != null) {
                this.playlist = [];
                for (var i = 0; i < response.data.length; i++) {
                    this.playlist.push(response.data[i])
                }
            } else {
                this.playlist = [];
            }
            // console.log(this.playlist)
        } else {
            location.href = "/user/login/";
        }
    }

    playlist_template(playlist, isChecked = false) {
        return `
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
    }

    /**
     * show fa model
     * @method  onecycle show fa model
     */
    showFa = () => {
        const self = this;
        $(".fa-body").html("");
        $(".fa-body").append(self.playlist_template("我的最愛", true));

        if (self.playlist != undefined)
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
            // console.log(self.insert_song_infos);
        });

        // 送出
        $("#favoriteModal").on("click", "#fa-insert", async function () {
            self.pushFa();
        });

        $("#creatPlaylistModal").on("click", ".creat-playlist", function () {
            self.createFa($('.new-playlist').val());
        });
    }

    createFa(playlist) {
        // console.log(this.playlist)
        const isDuplicate = this.playlist.some((existingPlaylist) => existingPlaylist === playlist);
        if (isDuplicate) {
            error("錯誤", "該專輯已經存在!")
            return;
        }

        // 将播放列表添加到 this.playlist

        this.playlist.push(playlist);
        console.log($(".fa-body").append(this.playlist_template(playlist)));

    }

    async pushFa() {
        console.log(this.insert_song_infos);
        const success = await this.fetch.POST(this.target, this.insert_song_infos);
        if (success) this.fetch.GET("/user/save_session/")
    }
}

