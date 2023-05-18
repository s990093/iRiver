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
        $("#playlistModal .modal-body  .playlist-body .playlist").unbind("click").on("click", function (event) {
            self.playlist = $(this).data("playlist");
            // console.log(self.playlist)
        });

        // edit
        $("#playlistModal .modal-body .edit").unbind("click").on("click", async function () {
            $("#editplaylistNameModal").modal("show");
        });

        // change playlist
        $("#editplaylistNameModal .change-playlist").unbind("click").on("click", async function () {
            const newPlaylist = $('.new-name').val();
            $("#editplaylistNameModal").modal("hide");
            if (self.playlist === undefined) {
                error("錯誤", "沒選擇專輯!");
                return;
            }
            const params = {
                method: "change_playlist",
                old_playlist_name: self.playlist,
                new_playlist_name: newPlaylist
            }
            const success = self.fetch.POST(self.target, params);
            if (success) {
                self.fetch.GET("/user/save_session/")
                $("#creatPlaylistModal-playlist").modal("hide");
                self.refresh(self.playlist, newPlaylist);
                self.playlist = undefined;
            }
        });

        //delete
        $("#playlistModal .modal-body")
            .unbind("click")
            .on("click", ".delete", async function () {
                if (self.playlist === undefined) {
                    error("錯誤", "沒選擇專輯!");
                    return;
                }
                const params = { method: "delete_playlist", playlist: self.playlist };
                const success = await self.fetch.POST(self.target, params);
                if (success) {
                    self.fetch.GET("/user/save_session/")
                    $("#playlistModal #" + self.playlist).remove();
                    self.playlist = undefined;
                }
            });

        // hide
        $("#playlistModal  #close")
            .unbind("click")
            .on("click", () => {
                self._closePL();
            });
    }

    _playlist_template(playlist, isChecked = false) {
        return `
        <div class="row">
            <div class="col">
                <label class="playlist mb-3" data-playlist="${playlist}" id = "${playlist}">
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

    refresh(old_playlist_name, new_playlist_name) {
        for (let i = 0; i < this.playlists.length; i++) {
            if (this.playlists[i][0] === old_playlist_name) {
                this.playlists[i][0] = new_playlist_name;
                break;
            }
        }
        this._showPL();
    }


    _closePL = () => {
        $("#playlistModal").modal("hide");
    }

    unregister = () => { }
}