function prevMusic() {
  currentMusicIndex = (currentMusicIndex - 1 + music_length) % music_length;
  audio.src = data.musicList[currentMusicIndex].url;
  //更新
  updateText();

  audio.currentTime = 0; // 重置播放進度
  audio.loop = false;
  audio.load();
  audio.play();
}
function nextMusic() { 
  currentMusicIndex = (currentMusicIndex - 1 + music_length) % music_length;
  audio.src = data.musicList[currentMusicIndex].url;
  updateText();

  audio.currentTime = 0; // 重置播放進度
  audio.loop = false;
  audio.load();
  audio.play();
}

// 靜音按鈕
muteButton.addEventListener('click', function() {
    audio.muted = !audio.muted;
    if (audio.muted) {
    muteButton.innerHTML = '<i class="fa fa-volume-off"></i>';
    } else {
    muteButton.innerHTML = '<i class="fa fa-volume-up"></i>';
    }
});

// 上一首按鈕
previousButton.addEventListener('click', function() {
  prevMusic();
});

// 下一首按鈕
nextButton.addEventListener('click', function() {
  nextMusic();
});

const progressBar = document.getElementById('progressBar');
const progress = document.getElementById('progress');
// 設定音訊檔案路徑
const audioSource = document.getElementById('audio-source');

progressBar.addEventListener('input', function() {
  const seekPos = progressBar.value / 100;
  audio.currentTime = audio.duration * seekPos;
  progressBar.value = progress.value;
});
// 在音频的 timeupdate 事件触发时，更新进度条的进度
audio.addEventListener('timeupdate', function() {
  // 计算当前播放进度（以百分比为单位）
  const progress = (audio.currentTime / audio.duration) * 100;
  // 更新进度条的值
  progressBar.value =  progress;
});

//結束
audio.addEventListener('ended', function() {
  // console.log("結束")
   nextButton.click();
});

const volumeSlider = document.getElementById("volumeSlider");

// 音量调节事件监听
volumeSlider.addEventListener("input", function() {
    audio.volume = volumeSlider.value / 100;
});



//鍵盤
document.addEventListener('keydown', function(event) {
  console.log(event.code);
  if (event.code === 'ArrowLeft') {
    // 慢10秒
    audio.currentTime -= 10;
  } else if (event.code === 'ArrowUp') {
    // 音量變大
    volumeSlider.value +=10;
    audio.volume = volumeSlider.value / 100;
  } else if (event.code === 'ArrowRight') { 
    // 快10秒
    audio.currentTime += 10;
  } else if (event.code === 'ArrowDown') {
    // 音量變小
    volumeSlider.value -=10;
    audio.volume = volumeSlider.value / 100;
  } else if (event.code === 'Space') {
    //暫停
    const playPauseButtons = document.querySelectorAll('.playPauseButton');
    pauseAllMusic(playPauseButtons);
  }
});