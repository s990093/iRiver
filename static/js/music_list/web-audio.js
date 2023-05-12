export class WebAudio {
    constructor(music_list, test = false) {
        this.test = test = false;
        this.music_list = music_list;

        this._register();

        if (this.test) {
            console.log(music_list);
        }
    }

    _register() {
        $('#small-player').hide();
        $('#big-player').hide();
    }

    update_music(currentIndex) {
        this._changeMusic(currentIndex);
    }

    //change Button

    changButtonIcon(isplaying) {
        if (isplaying) {
            $('#.playPauseButton').html('<i class="fa fa-pause"></i>');
            $('#play .icon use').attr('href', '/static/svg/iocn.svg#icon-pause');
        }
        else {
            $('#.playPauseButton').html('<i class="fa fa-play"></i>');
            $('#play .icon use').attr('href', '/static/svg/iocn.svg#icon-play');
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
        if (isLoop)
            $('#loopButton').html('<span class="material-symbols-outlined">repeat</span>');

        else
            $('#loopButton').html('<span class="material-symbols-outlined">repeat_one</span>');
    }

    changFavoriteButton(href) {
    } s

    //  音樂資訊

    changePlayer(isPlayerShow) {
        console.log('changePlayer', isPlayerShow);
        //1 大 0小
        if (isPlayerShow) {
            $('.main-content').hide();
            $('.switchPlayer').html('<i class="fa fa-compress"></i>');
            $('#big-player').css('display', !isPlayerShow ? 'none' : 'block');
            $('#small-player').css('display', !isPlayerShow ? 'block' : 'none');

        } else {
            $('.main-content').show();
            $('.switchPlayer').html('<i class="fa fa-arrows-alt"></i>');
            $('#big-player').css('display', !isPlayerShow ? 'none' : 'block');
            $('#small-player').css('display', !isPlayerShow ? 'block' : 'none');
        }
    }

    _changeMusic(currentIndex) {
        var song_src = '/media/' + this.music_list[currentIndex].artist + '/img/' + this.music_list[currentIndex].music_ID + '.jpg';
        var artist_src = '/media/' + this.music_list[currentIndex].artist + '/img/artist.jpg';

        // 照片
        $('.albumCover').attr('src', song_src);
        $('.artist-img').attr('src', artist_src);

        //刷新  title 跑馬燈
        $('#songTitle').text(this.music_list[currentIndex].title);
        $("#artistName").text(this.music_list[currentIndex].artist)
        // $('.songTitle').removeClass("marquee");
        // $('.songTitle')[0].offsetWidth;
        // $('.songTitle').addClass("marquee");


        // artist
        var href = '/music_list/?artist=' + this.music_list[currentIndex].artist + '&index=' + currentIndex;
        // $('.artist a').attr('href', href);
        // $('.artist').find('.hover-link').text(this.music_list[currentIndex].artist)



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


        $('#myaudio').attr('data-music_ID', this.music_list[currentIndex].music_ID);
    }
}