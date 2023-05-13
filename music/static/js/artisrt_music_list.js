import { Control } from "../../../static/js/music_list/control.js";
// import { initial } from '../../../static/js/music_list/drive.js';

var isClickEventRegistered = false;

// Add click event listener to each row
$('document').ready(function () {
    var imageUrl = `url(/media/${music_list_infos[0].artist}/img/cover.jpg`; // 设置背景图像的 URL
    $('.bg-img').css('background-image', imageUrl); // 设置背景图像
    const audio = document.getElementById('myaudio');
    const control = new Control({
        audio: audio
    });
    control.add_music_list(music_list_infos);


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


