//必改
let isBigPlayerDisplayed =  true


fetch('/get-music-list/')
  .then(response => response.json())
  .then(data => {;
    push_music_list(data.musicList);
  });

function push_music_list(musicList) {
  const audioElement = document.getElementById('myaudio');
  var music_list = document.getElementById("table-body");
  music_list.innerHTML = "";
  for (var i = 0; i < musicList.length; i++) {
    var row = document.createElement("tr");
    var col1 = document.createElement("td");
    var col2 = document.createElement("td");
    var col3 = document.createElement("td");
    col1.innerHTML = musicList[i].artist;
    col2.innerHTML = musicList[i].title;
    col3.innerHTML = musicList[i].duration;

    // add click event listener to each row
    row.addEventListener("click", function() {
      // get the index of the clicked row
      var clickedRowIndex = Array.from(this.parentNode.children).indexOf(this);
      
      // set the currentMusicIndex to the clickedRowIndex
      currentMusicIndex = clickedRowIndex;
      
      // update the audio element source and play the song
      var nextMusicSrc = musicList[currentMusicIndex].url;
      audioElement.src = nextMusicSrc;
      updateText();
      audioElement.load();
      audioElement.play();
    });

    row.appendChild(col1);
    row.appendChild(col2);
    row.appendChild(col3);
    music_list.appendChild(row);
  }
}
