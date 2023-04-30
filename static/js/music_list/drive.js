import { Control } from "./control.js";
//全域變數
let musicList
let currentMusicIndex;
let music_length
// let index
let isBigPlayerDisplayed
var isClickEventRegistered = false;


export function initial(in_isBigPlayerDisplayed, in_data, in_currentMusicIndex, in_index) {
  console.log('initial music player', in_data, in_currentMusicIndex, 'index', in_index)
  isBigPlayerDisplayed = in_isBigPlayerDisplayed
  try {
    currentMusicIndex = in_currentMusicIndex
  } catch (error) {
    currentMusicIndex = 0
  }
  try {
    musicList = in_data.musicList
    music_length = in_data.musicList.length
  } catch (error) {
    try {
      musicList = in_data.videos
      music_length = in_data.videos.length

    } catch (error) {
      musicList = in_data
      music_length = in_data.length
    }


    $(document).ready(function () {
      const audio = document.getElementById('myaudio');
      console.log(musicList)
      const control = new Control(audio, musicList, true, false, true);
      if (!isClickEventRegistered) {
        control.register();
        isClickEventRegistered = true;
      }
      control.insert(0);
    });
  }
}

export function update_currentMusicIndex(in_currentMusicIndex) {
  currentMusicIndex = in_currentMusicIndex;
}
