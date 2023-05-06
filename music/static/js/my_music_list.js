import { Control } from "../../../static/js/music_list/control.js";

var isClickEventRegistered = false;
$('document').ready(function () {
    const audio = document.getElementById('myaudio');
    const control = new Control(audio, music_list_infos, false, false, false);
    $('tr .play').on('click', function (e) {
        e.preventDefault();
        var clickedRowIndex = $(this).index();
        if (!isClickEventRegistered) {
            control.register();
            isClickEventRegistered = true;
        }
        control.insert(clickedRowIndex);
    });
});

