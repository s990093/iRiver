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
            self.insert_song_infos = { "music_ID": $(this).attr('value'), "favorite": false };
            console.log(self.insert_song_infos);
            self.showFa()
        });


        // 我的最愛
        $('#table-body').on('click', '.love-icon a', async function () {
            $(this).find('i').toggleClass('far fas');
            var music_ID = $(this).attr('value');
            // 送出
            insert_my_music_list({
                music_ID: music_ID,
                music_list: "我的最愛",
                favorite: true
            });
        });
    }

    _get_playlist() {
        return this.fetch.get_playlist();
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
        $(".fa-body").html(self.playlist_template("我的最愛", true));
        $('.fa-body').html(this.playlist.map(function (playlist) {
            return self.playlist_template(playlist);
        }));


        // 添加到哪個專輯
        $(".fa-body").on("click", ".playlist", function () {
            self.insert_song_infos = {
                "playlist": $(this).data('playlist'),
                "music_ID": self.insert_song_infos.music_ID,
                "favorite": self.insert_song_infos.favorite
            }
            // console.log(self.insert_song_infos);
        });

        // 送出
        $(".fa-body").on("click", ".fa-insert", async function () {
            const success = await insert_my_music_list(self.insert_song_infos);
            console.log(success);
        });
    }

    createFa = (playlist) => {
        this.playlist = [...playlist];
        $(".fa-body").on("click", () => { this.playlist_template4(playlist); });
    }
}
