export class MediaPlayer {
    constructor(audio) {
        this.audio = audio;
    }

    register() {
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
        var currentTime = (this.audio.currentTime / this.audio.duration) * 100;
        $('.progress-bar').css('width', currentTime + '%');
    }

    update_my_music_list(music_ID, music_list = 1, favorite = true, method) {
        insert_my_music_list({
            music_ID: music_ID,
            playlist: music_list,
            favorite: favorite,
            method: method
        });
    }
}

export function insert_my_music_list({ music_ID, playlist = "我的最愛", favorite = true, method }) {
    return new Promise((resolve, reject) => {
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
                            playlist: playlist,
                            favorite: favorite
                        })
                    }).then(response => {
                        if (response.ok) {
                            // 保存成功
                            console.log('保存成功', method);
                            resolve(true);
                        } else {
                            // 保存失败
                            console.log('保存失败', method);
                            reject(false);
                        }
                    });
                } else {
                    location.href = "/user/login/";
                    reject(false);
                }
            });
    });
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// // export function
// export { insert_my_music_list };
