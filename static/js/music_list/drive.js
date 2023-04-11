// 選取元素
const audio = document.getElementById('myaudio');
const stopButton = document.getElementById('stopButton');
const muteButton = document.getElementById('muteButton');
const previousButton = document.getElementById('previousButton');
const nextButton = document.getElementById('nextButton');

//class
const switchPlayers = document.querySelectorAll('.switchPlayer');   //class="switchPlayer"
const playPauseButtons = document.querySelectorAll('.playPauseButton');   //class = "playPauseButton

//歌曲資訊
let songTitleElements = document.querySelectorAll("#songTitle");
let artistNameElements = document.querySelectorAll("#artistName");

// 取得大撥放介面和小撥放介面的元素
const bigPlayer = document.getElementById('big-player');
const smallPlayer = document.getElementById('small-player');

//全域變數
let musicList = [];
let currentMusicIndex = 0;
let music_length 
let data;
let is_playing = false;
let is_switch_player = false; 
// isBigPlayerDisplayed = isBigPlayerDisplayed;  


function pauseMusic(playPauseButton) {
  if (is_playing) {
    is_playing = !is_playing;
    audio.play();
    playPauseButton.innerHTML = '<i class="fa fa-pause"></i>';
  } else {
    is_playing = !is_playing;
    audio.pause();
    playPauseButton.innerHTML = '<i class="fa fa-play"></i>';
  }
}

function updateText() {
  // 操作 songTitleElements
  songTitleElements.forEach(function(element) {
    element.textContent = data.musicList[currentMusicIndex].title;
    //刷新 跑馬燈
    element.classList.remove("marquee");
    void element.offsetWidth; // 強制瀏覽器重繪
    element.classList.add("marquee");
  });
  // 操作 artistNameElements
  artistNameElements.forEach(function(element) {
    element.textContent = data.musicList[currentMusicIndex].artist;
  });
}

fetch('/get-music-list/')
  .then(response => response.json())
  .then(json => {
    console.log("data: ", json);
    data = json;
    music_length = data.musicList.length;
    if (data.musicList.length > 0) {
      audio.src = data.musicList[0].url;
      updateText();
      audio.load();
      audio.play();
     // 狀態檢查
      if (audio.paused) {
        is_playing = false;
        playPauseButtons.innerHTML = '<i class="fa fa-pause"></i>';
      } else {
        is_playing = true;  
          playPauseButtons.innerHTML = '<i class="fa fa-play"></i>';
      }
    }
  });

// 播放/暫停按鈕s
playPauseButtons.forEach(function(playPauseButton) {
  playPauseButton.addEventListener('click', function() {
    pauseMusic(playPauseButton);
  });
});

//先載入的撥放器
window.onload = function() {
  bigPlayer.style.display = isBigPlayerDisplayed ? 'none' : 'block';
  smallPlayer.style.display = isBigPlayerDisplayed ? 'block' : 'none';
  // console.log("smallPlayer.style.display" ,   smallPlayer.style.display);
  // console.log("bigPlayer.style.display",   bigPlayer.style.display)
}

// 改變播放介面
switchPlayers.forEach(function(switchPlayer) {
  switchPlayer.addEventListener('click', function() {
    isBigPlayerDisplayed = !isBigPlayerDisplayed;
    // console.log(isBigPlayerDisplayed);
    // 切換箭頭方向
    if (isBigPlayerDisplayed) {
      switchPlayer.innerHTML = '<i class="fa fa-compress"></i>';
    } else {
      switchPlayer.innerHTML = '<i class="fa fa-arrows-alt"></i>';
    }

   // 切換大小撥放介面
    bigPlayer.style.display = isBigPlayerDisplayed ? 'none' : 'block';
    smallPlayer.style.display = isBigPlayerDisplayed ? 'block' : 'none';
    updateText();
  });
});


// 自定義 tripleclick 事件  (點擊三下)
function tripleClick(element, callback) {
  let clicks = 0;
  const MIN_INTERVAL = 500; // 最小點擊間隔時間（毫秒）

  element.addEventListener('click', function(event) {
    clicks++;
    console.log(clicks);

    if (clicks === 3) {
      callback(event);
      clicks = 0;
    }

    setTimeout(() => {
      clicks = 0;
    }, MIN_INTERVAL);
  });
}

// 點擊三下改變介面
tripleClick(bigPlayer, function() {
  isBigPlayerDisplayed = !isBigPlayerDisplayed;

  // 切換大小撥放介面
  bigPlayer.style.display = isBigPlayerDisplayed ? 'none' : 'block';
  smallPlayer.style.display = isBigPlayerDisplayed ? 'block' : 'none';
});

tripleClick(smallPlayer, function() {
  isBigPlayerDisplayed = !isBigPlayerDisplayed;

  // 切換大小撥放介面
  bigPlayer.style.display = isBigPlayerDisplayed ? 'none' : 'block';
  smallPlayer.style.display = isBigPlayerDisplayed ? 'block' : 'none';
});