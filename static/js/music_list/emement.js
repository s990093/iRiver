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
}