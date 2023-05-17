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
            const params = { method: "delete_playlist", playlist: playlist };
            const response = await self.fetch.POST(self.target, params);
        });

    }

    _playlist_template(playlist) {
        return `
        <div class="row playlist" id= "${playlist}">
            <div class="col-6">
            <label class="mb-3" data-playlist="${playlist}">
                ${playlist}
            </label>
            </div>
            <div class="col-4 offset-2">
                <div class="d-flex justify-content-between">
                    <a href="javascript:void(0)" class="delete mr-2">
                        <i class="bi bi-trash-fill"></i>
                    </a>
                    <a href="javascript:void(0)" class="edit">
                        <i class="fa-solid fa-hammer"></i>
                    </a>
                    <a href="javascript:void(0)" class="add">
                        <i class="bi bi-plus-lg"></i>
                    </a>
                </div>
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