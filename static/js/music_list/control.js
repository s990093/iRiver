import { WebAudio } from './web-audio.js';
import { bgAudio } from './bg-audio.js';
import { MediaPlayer } from "./emement.js";
import { EqController } from "./eq_control.js";
import { FaController } from "./add-favorite.js";
import { InformationManager } from "./information.js";


/**
 * @typedef {Object} ControlParams
 * @property {Audio} audio - The audio object
 * @property {boolean} [isPlaying=false] - Indicates if the audio is currently playing
 * @property {boolean} [isPlayerShow=false] - Indicates if the audio player is visible
 * @property {number} [currentIndex=0] - The index of the current song in the list
 * @property {string} [currentList="org"] - The name of the current music list
 * @property {boolean} [test=false] - Indicates if it is a test mode
 */
export class Control {
  /**
  * Constructor for Control class
  * @param {ControlParams} params - The parameters object
  */
  constructor({
    audio,
    isPlaying = false,
    isPlayerShow = false,
    currentIndex = 0,
    currentList = "org",
    test = false,
  }) {
    this.test = test;

    this.music_list_list = {};
    // this.audio = new Audio();
    this.audio = audio;

    // bool
    this.isPlaying = isPlaying;
    this.isPlayerShow = isPlayerShow;
    this.isMute = false;
    this.isLoop = false;
    this.isShuffle = false;


    this.currentIndex = currentIndex;
    this.currentList = currentList;
    this.music_length = 0;

    this.$playBtn = $('#play');
    this.$switchPlayer = $('.switchPlayer');
    this.$muteBtn = $('.muteButton');

    //宣告物件
    this.webAudio = new WebAudio();
    this.mediaPlayer = new MediaPlayer(this.audio);
    this.faController = new FaController({ isTest: false });
  }

  register() {
    //宣告物件
    this.bgAudio = new bgAudio(this.test);
    this.mediaPlayer.register();
    this.eqController = new EqController(this.audio, this.test);
    this.webAudio.changePlayer(this.isPlayerShow);
    // if ('mediaSession' in navigator)
    //   navigator.mediaSession.metadata = null;
    // // this.insert();
    //監聽
    this._lienter();
  }



  _lienter() {
    var self = this;
    //audio
    this.audio.addEventListener('ended', () => {
      this.next();
    });

    $('#nextTrack').on('click', () => {
      this.next();
    });


    $('#prevTrack').on('click', () => {
      this.previous()
    });

    let timeoutId;

    $('#progressBar').on('change', () => {
      const currentTime = this.audio.duration * ($('#progressBar').val() / 100);
      console.log(currentTime);
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
    // play
    this.$playBtn.on('click', () => {
      if (this.isPlaying) {
        this.play();
      } else {
        this.pause();
      }
      this.webAudio.changButtonIcon(this.isPlaying);
      this.isPlaying = !this.isPlaying;
    });

    $(".playPauseButton").on('click', () => {
      if (self.isPlaying) {
        self.play();
      } else {
        self.pause();
      }
      self.webAudio.changButtonIcon(self.isPlaying);
      self.isPlaying = !self.isPlaying;
    });

    // 撥放器大小
    $(document).on('click', '.small-player, .player', (event) => {
      if ($(event.currentTarget).hasClass('small-player') || $(event.target).hasClass('player')) {
        this.isPlayerShow = !this.isPlayerShow;
        this.webAudio.changePlayer(this.isPlayerShow);
      }
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

  insert(insertIndex = this.currentIndex, list = "org") {
    console.log(this.music_list_list)
    this.currentList = list;
    this.music_length = this.music_list_list[this.currentList].length;
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
    var music_list = this.music_list_list[this.currentList][this.currentIndex];
    this.audio.pause();
    this.audio.currentTime = 0;
    this.audio.loop = false;

    var address = '/media/' + music_list.artist + "/songs/" + music_list.music_ID + '.mp3';
    this.audio.src = address;
    this.audio.load();
    this.audio.play();

    //change information 
    this.webAudio.update_music(music_list);
    this.bgAudio.updateMediaSessionMetadata(music_list);
  }

  add_music_list(music_list, list = "org") {
    const newList = { [list]: music_list };
    this.music_list_list = { ...this.music_list_list, ...newList };
  }

  update_music(music_list, list = "org") {
    this.music_list_list[list] = music_list;
  }
}
