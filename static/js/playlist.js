export class PlaylistController {
    constructor() {
        this.playlists = []
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
    }

    _playlist_template(playlist) {
        console.log(playlist);
        return `
        <div class="row">
            <div class="col-6">
            <label class="playlist mb-3" data-playlist="${playlist}">
                ${playlist}
            </label>
            </div>
            <div class="col-4 offset-2">
                <div class="d-flex justify-content-between">
                    <a href="javascript:void(0)" class="delete mr-2">
                        <i class="bi bi-trash-fill"></i>
                    </a>
                    <a href="javascript:void(0)" class="delete">
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