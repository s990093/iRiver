import { Fetch } from "./fetch.js";
import { error } from "./error.js";
// import { FaController } from "./music_list/add-favorite.js";

export class PlaylistController {
    constructor() {
        this.fetch = new Fetch();
        this.playlists = [];
        this.playlist;
        this.target = "/user/get_user_music_list/";
    }

    push_playlist = (playlists) => {
        this.playlists = playlists;
        this._register();
    }
    _register = () => {
        this._listen();
    }

    _listen = () => {
        const self = this;
        $("#playlist-setting").unbind("click").on("click", function () {

            self._showPL();
        });

        // get the playlist
        $("#playlistModal .modal-body  .playlist-body .playlist").on("click", function (event) {
            self.playlist = $(this).data("playlist");
            console.log(self.playlist)
        });

        // delete
        $("#playlistModal .modal-body .playlist-body .delete").on("click", async function () {
            if (self.playlist === undefined) {
                error("錯誤", "沒有選擇專輯!");
                return;
            }

            const params = { method: "delete_playlist", playlist: self.playlist };
            const success = await self.fetch.POST(self.target, params);
            if (success) {
                $(`#${playlist}`).removes();
            }
        });

        // edit
        $("#playlistModal .modal-body").unbind("click").on("click", ".edit", async function () {
            $("#editplaylistNameModal").modal("show");
        });

        // add
        // $("#playlistModal .modal-body").unbind("click").on("click", ".add", async function () {
        //     $("#creatPlaylistModal-playlist").modal("show");
        // });

        // refresh playlist
        $("#creatPlaylistModal-playlist .creat-playlist").unbind("click").on("click", function () {
            const playlist = $('.new-playlist').val();
            $("#creatPlaylistModal-playlist").modal("hide");
            self.refresh(playlist);
        });

        //delete
        $("#playlistModal .modal-body")                                                                          
            .unbind("click")
            .on("click", ".delete", async function () {
                if (self.playlist === undefined) return;
                const params = { method: "delete", playlist: self.playlist };
                const success = await self.fetch(self.target, params);
            });
    }

    _playlist_template(playlist, isChecked = false) {
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
        `
    }

    _showPL() {
        $("#playlistModal").modal("show");


        const self = this;

        $("#playlistModal .modal-body  .playlist-body").html("");
        // console.log($("#playlistModal .modal-body .playlist-body"))
        $("#playlistModal .modal-body .playlist-body").append(self.playlists.map(function (playlist) {
            return self._playlist_template(playlist);
        }));
    }

    refresh(playlist) {
        this.playlists.push(playlist);
        console.log(this.playlists);
        this._showPL();
    }

    unregister = () => { }
}