export class WebAudio {
    constructor(test = false) {
        this.test = test = false;


        this._register();

        if (this.test) {
            console.log(music_list_list);
        }
    }

    _register() {
        $('#small-player').hide();
        $('#big-player').hide();
    }

    update_music(currentIndex) {
        this._changeMusic(currentIndex, this.list);
    }

    //change Button

    changButtonIcon(isplaying) {
        if (isplaying) {
            $('.playPauseButton').html('<i class="fa fa-pause"></i>');
            $('#play .icon use').attr('href', '/static/svg/icon.svg#icon-pause');
        }
        else {
            $('.playPauseButton').html('<i class="fa fa-play"></i>');
            $('#play .icon use').attr('href', '/static/svg/icon.svg#icon-play');
        }
    }

    changMuteButton(isMute) {
        if (isMute)
            $('.muteButton').html('<i class="fa fa-volume-off"></i>');
        else
            $('.muteButton').html('<i class="fa fa-volume-up"></i>');
    }

    changShuffleButton(isShuffle) {
        if (isShuffle)
            $('#shuffleButton').html('<i class="fa fa-random"></i>');
        else
            $('#shuffleButton').html('<i class="fas fa-redo-alt">');
    }

    changLoopButton(isLoop) {
        var symbol = isLoop ? 'repeat' : 'repeat_one';
        $('#loopButton').html(`<span class="material-symbols-outlined">${symbol}</span>`);
    }

    changFavoriteButton(href) {
        const path = "/static/svg/icon.svg";
        const iconHeart = `${path}#icon-heart`;
        const iconHeartO = `${path}#icon-heart-o`;
        if (href == "/static/svg/icon.svg#icon-heart-o")
            $('#favorite use').attr('href', iconHeart);
        else
            $('#favorite use').attr('href', iconHeartO);
    }

    //  音樂資訊

    changePlayer(isPlayerShow) {
        // console.log('changePlayer', isPlayerShow);
        //1 大 0小
        if (isPlayerShow) {
            // $('.main-content').hide();
            $('.switchPlayer').html('<i class="fa fa-compress"></i>');
            $('#big-player').css('display', !isPlayerShow ? 'none' : 'block');
            $('#small-player').css('display', !isPlayerShow ? 'block' : 'none');

        } else {
            // $('.main-content').show();
            $('.switchPlayer').html('<i class="fa fa-arrows-alt"></i>');
            $('#big-player').css('display', !isPlayerShow ? 'none' : 'block');
            $('#small-player').css('display', !isPlayerShow ? 'block' : 'none');
        }
    }

    _changeMusic(music_list) {
        var song_src = '/media/' + music_list.artist + '/img/' + music_list.music_ID + '.jpg';
        var artist_src = '/media/' + music_list.artist + '/img/artist.jpg';

        // 照片
        $('.albumCover').attr('src', song_src);
        $('.artist-img').attr('src', artist_src);

        //刷新  title 跑馬燈
        $('.songTitle').text(music_list.title);
        $(".artistName").text(music_list.artist)
        // $('.songTitle').removeClass("marquee");
        // $('.songTitle')[0].offsetWidth;
        // $('.songTitle').addClass("marquee");


        // artist
        var href = '/music/music_list/?artist=' + music_list.artist;
        $('.artist a').attr('href', href);
        // $('.artist').find('.hover-link').text(music_list.artist)



        // 新版
        $('.player-cover__item').fadeOut(250, function () {
            $(this).css('background-image', `url(${song_src})`).fadeIn(300);
        });

        // $('.player-cover__item').fadeOut(200, function () {
        //     $(this).css('background-image', `url(${song_src})`);
        //     $(this).removeClass('scale-in-enter-active scale-in-leave-active scale-in-enter scale-in-leave-to');
        //     $(this).addClass('scale-out-enter-active scale-out-leave-active scale-out-enter scale-out-leave-to');
        //     $(this).fadeIn(200, function () {
        //         $(this).removeClass('scale-out-enter-active scale-out-leave-active scale-out-enter scale-out-leave-to');
        //         $(this).addClass('scale-in-enter-active scale-in-leave-active scale-in-enter scale-in-leave-to');
        //         $(this).css({
        //             'transform': 'scale(1)',
        //             'pointer-events': 'auto',
        //             'opacity': '1'
        //         });
        //     });
        // });


        $('#myaudio').attr('data-music_ID', music_list.music_ID);
    }
}