export class MediaPlayer {
    constructor(audio) {
        this.audio = audio;
        this.$volumeSlider = $('#volumeSlider');

        this._register()
    }

    _register() {
        this.changeVolumeSlider();

    }

    changeVolumeSlider() {
        $('#volumeSlider').on("input", () => {
            this.audio.volume = $('#volumeSlider').val() / 100;
        });
    }

    increaseVolume() {
        const newValue = parseInt(this.$volumeSlider.val()) + 10;
        const valueToSet = newValue < 90 ? newValue : 100;
        this.$volumeSlider.val(valueToSet);
        this.audio.volume = valueToSet / 100;
    }

    decreaseVolume() {
        const newValue = parseInt(this.$volumeSlider.val()) - 10;
        const valueToSet = newValue > 10 ? newValue : 0;
        this.$volumeSlider.val(valueToSet);
        this.audio.volume = valueToSet / 100;
    }


    updateProgressBar() {
        // 计算当前播放进度（以百分比为单位）
        var currentTime = (this.audio.currentTime / this.audio.duration) * 100;
        // 更新进度条的值
        $('#progressBar').val(currentTime);
    }

    insert_my_music_list(music_ID, music_list = 1, favorite = true, method) {
        fetch(`/user/isLogin/`)
            .then(response => response.json())
            .then(data => {
                if (data.isLogin) {
                    const csrftoken = getCookie('csrftoken');
                    fetch('/user/get_user_music_list/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken
                        },

                        body: JSON.stringify({
                            music_ID: music_ID,
                            method: method,
                            music_list: music_list,
                            favorite: favorite
                        })
                    });
                } else location.href = "/user/login/";
            });
    }
}