import { Control } from "../../../static/js/music_list/control.js";
import { insert_my_music_list } from "../../../static/js/music_list/emement.js";
import { Fetch } from "../../../static/js/fetch.js";
import { SessionController } from "../../../static/js/session.js";

const sessionController = new SessionController();
const fetch = new Fetch();
var isClickEventRegistered = false;
$('document').ready(function () {
    const audio = document.getElementById('myaudio');
    const control = new Control({
        audio: audio
    });
    control.add_music_list(music_list_infos);

    $('tr .play, .play-music').on('click', function (e) {
        e.preventDefault();
        var index = $(this).attr('value');
        if (!isClickEventRegistered) {
            control.register();
            isClickEventRegistered = true;
        }
        control.insert(index);
    });

});

// delete 
$('.delete').on('click', async function () {
    try {
        await fetch.POST("/user/get_user_music_list/",
            {
                method: "delete",
                music_ID: $(this).find('a').attr('value'),
                playlist: $(this).find('a').data('music-list')
            }
        );
        if (music_list_infos.length == 1 || music_list_infos.length == 2) {
            location.href = "/music/discover/";
        }

        sessionController.refresh();

        location.reload();
    } catch (error) {
        console.log('操作失敗');
    }
});

