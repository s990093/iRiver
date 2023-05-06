import { WebAudio } from './web-audio.js';
import { bgAudio } from './bg-audio.js';
import { MediaPlayer } from "./emement.js";
import { EqController } from "./eq_control.js";


/**
 * @param {HTMLAudioElement} audio - the audio element
 * @param {JSON} current_info - 呼呼information about the currently selected music
 * 
 */

export class Control {
  constructor(audio, music_list, isPlaying = false, isPlayerShow = false, test = false, currentIndex = 0) {
    this.test = test;

    if (this.test) {
      console.log('control ok');
      // console.log(isPlayerShow);
    }

    this.music_list = music_list;
    this.audio = audio;

    // bool
    this.isPlaying = isPlaying;
    this.isPlayerShow = isPlayerShow;
    this.isMute = false;
    this.isLoop = false;
    this.isShuffle = false;


    this.currentIndex = currentIndex;
    this.music_length = music_list.length;

    this.$playBtn = $('.playPauseButton');
    this.$stopBtn = $('.stop-btn');
    this.$switchPlayer = $('.switchPlayer');
    this.$muteBtn = $('.muteButton');


  }

  register() {
    //宣告物件
    this.webAudio = new WebAudio(this.music_list);
    this.bgAudio = new bgAudio(this.music_list, this.currentIndex);
    this.mediaPlayer = new MediaPlayer(this.audio);
    if ('mediaSession' in navigator)
      navigator.mediaSession.metadata = null;
    this.eqController = new EqController(this.audio, this.test);
    this.mediaPlayer = new MediaPlayer(this.audio);
    this.webAudio.changePlayer(this.isPlayerShow);
    // this.insert();

    //監聽
    this._lienter();
  }



  _lienter() {
    //audio
    this.audio.addEventListener('ended', () => {
      this.next();
    });

    $('#nextButton').on('click', () => {
      this.next();
    });
    $('#previousButton').on('click', () => {
      this.previous()
    });

    let timeoutId;

    $('#progressBar').on('input', () => {

      const currentTime = this.audio.duration * $('#progressBar').val() / 100;
      this.audio.currentTime = currentTime;

    });


    this.audio.addEventListener('timeupdate', () => {
      this.mediaPlayer.updateProgressBar();
    });


    this.$muteBtn.on('click', () => {
      this.isMute = !this.isMute;
      this.webAudio.changMuteButton(this.isMute);
    });



    $('#loopButton').on('click', () => {
      this.isLoop = !this.isLoop;
      this.webAudio.changLoopButton(this.isLoop);
      this.loop(this.isLoop);
    });

    $('#shuffleButton').on('click', () => {
      this.isShuffle = !this.isShuffle;
      this.webAudio.changShuffleButton(this.isShuffle);
      if (this.isShuffle) {
        this.shuffle();
      }
    });





    // button
    this.$playBtn.on('click', () => {
      if (this.isPlaying) {
        this.play();
      } else {
        this.pause();
      }
      this.isPlaying = !this.isPlaying;

    });

    this.$stopBtn.on('click', this.stop.bind(this));

    // 撥放器
    this.$switchPlayer.on('click', () => {
      this.isPlayerShow = !this.isPlayerShow;
      this.webAudio.changePlayer(this.isPlayerShow);
    });

    // 靜音按鈕
    this.$muteBtn.on('click', () => {
      this.audio.muted = !this.audio.muted;
      this.webAudio.changMuteButton(this.audio.muted);
    });

    // 添加媒体会话 API 监听器
    navigator.mediaSession.setActionHandler('play', () => {
      if (this.isPlaying) {
        this.play();
      } else {
        this.pause();
      }
      this.isPlaying = !this.isPlaying;
    });
    navigator.mediaSession.setActionHandler('pause', () => {
      if (this.isPlaying) {
        this.play();
      } else {
        this.pause();
      }
      this.isPlaying = !this.isPlaying;
    });
    navigator.mediaSession.setActionHandler('stop', this.stop.bind(this));
    navigator.mediaSession.setActionHandler('nexttrack', () => {
      this.next();
    });
    navigator.mediaSession.setActionHandler('previoustrack', () => {
      this.previous();
    });

    // keyboard
    $(document).on('keydown', (event) => {
      if (this.test)
        // console.log(event.code);
        if (event.code === 'ArrowLeft') {
          // 慢10秒
          this.audio.currentTime -= 10;
        } else if (event.code === 'ArrowUp') {
          // 音量變大
          this.mediaPlayer.increaseVolume();
        } else if (event.code === 'ArrowRight') {
          // 快10秒
          this.audio.currentTime += 10;
        } else if (event.code === 'ArrowDown') {
          // 音量變小
          this.mediaPlayer.decreaseVolume();
        } else if (event.code === 'Space') {
          //暫停
          this.pause();
        }
    });
  }

  unregister() {

  }
  play() {
    if (this.test)
      console.log('play');
    this.audio.play();
    navigator.mediaSession.playbackState = 'playing';
  }

  pause() {
    if (this.test)
      console.log('pause');
    this.audio.pause();
    navigator.mediaSession.playbackState = 'paused';
  }

  stop() {
    if (this.test)
      console.log('stop');
    navigator.mediaSession.playbackState = 'none';
  }

  next() {
    this.currentIndex = (this.currentIndex + 1 + this.music_length) % this.music_length;
    this.update_song();


    if (this.test) {
      console.log('next');
      // console.log('currentMusicIndex', this.currentIndex);
    }
  }

  previous() {
    this.currentIndex = (this.currentIndex - 1 + this.music_length) % this.music_length;
    this.update_song();
    if (this.test)
      console.log('prev');
  }

  insert(insertIndex = this.currentIndex) {
    this.currentIndex = insertIndex - 1;
    this.next();
  }


  loop(isLoop) {
    if (isLoop)
      this.audio.loop = true;
    else
      this.audio.loop = false;
  }

  shuffle() {
    var randomIndex
    do {
      randomIndex = Math.floor(Math.random() * this.music_length);
    } while (randomIndex == this.currentIndex);
    this.currentIndex = randomIndex;
  }

  update_song() {
    this.audio.pause();
    this.audio.currentTime = 0; // 重置播放進度
    this.audio.loop = false;


    var address = '/media/' + this.music_list[this.currentIndex].artist + "/songs/" + this.music_list[this.currentIndex].music_ID + '.mp3';
    this.audio.src = address;
    this.audio.load();
    this.audio.play();

    //change information 
    this.webAudio.update_music(this.currentIndex);
    this.bgAudio.updateMediaSessionMetadata(this.currentIndex);
  }
}
