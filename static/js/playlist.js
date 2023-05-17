import { Fetch } from "./fetch.js";
import { error } from "./error.js";

export class PlaylistController {
    constructor() {
        this.fetch = new Fetch();
        this.playlists = [];
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
        $("#playlist-setting").on("click", function () {
            self._showPL();
            $("#playlistModal").modal("show");
        });

        // delete
        $("#playlistModal .modal-body .playlist").on("click", ".delete", async function () {
            var playlist = $(this).data("playlist");
            const params = { method: "delete_playlist", playlist: playlist };
            const success = await self.fetch.POST(self.target, params);
            if (success) {
                $(`#${playlist}`).removes();
            }
        });

        // edit
        $("#playlistModal .modal-body").on("click", ".edit", async function () {
            location.href = `/music/my_music_list?music_list=${$(this).data("playlist")}`;
        });

        // add
        $("#playlistModal .modal-body").on("click", ".add", async function () {
            var playlist = $(this).data("playlist");
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
        const self = this;

        $("#playlistModal .modal-body").html("");
        $("#playlistModal .modal-body").append(self.playlists.map(function (playlist) {
            return self._playlist_template(playlist);
        }));
    }

}