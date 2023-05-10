import { Control } from "../../../static/js/music_list/control.js";
// import { initial } from '../../../static/js/music_list/drive.js';

var isClickEventRegistered = false;
// Add click event listener to each row
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

