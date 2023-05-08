import { Control } from "../../../static/js/music_list/control.js";
import { insert_my_music_list } from "../../../static/js/music_list/emement.js";


var isClickEventRegistered = false;
$('document').ready(function () {
    const audio = document.getElementById('myaudio');
    const control = new Control(audio, music_list_infos, false, true, false);
    $('tr .play').on('click', function (e) {
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
$('.delete').on('click', async () => {
    var music_ID = $('.delete a').attr('value');
    var music_list = $('.delete').attr('data-music_list');
    try {
        await insert_my_music_list(music_ID, music_list, false, 'delete');
        location.reload();
    } catch (error) {
        console.log('操作失敗');
    }
});
