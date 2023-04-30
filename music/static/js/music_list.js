import { Control } from "../../../static/js/music_list/control.js";
// import { initial } from '../../../static/js/music_list/drive.js';


//必改
let isBigPlayerDisplayed = true
let data
let control;
var isClickEventRegistered = false;


$(document).ready(function () {
  fetch(`/music/get_music_list/?query=${artist}&index=${index}`)
    .then(response => response.json())
    .then(data => {
      const audio = document.getElementById('myaudio');
      console.log('music list', data)
      control = new Control(audio, data.musicList, true, false, true);
      push_music_list(data);
    });
});


function push_music_list(data) {
  for (var i = 0; i < data.musicList.length; i++) {
    var img_src = '/media/' + data.musicList[i].artist + '/img/' + data.musicList[i].music_ID + '.jpg';
    var row = `
    <tr>
      <td>
        <a href="#">
          <img src="${img_src}" alt="img_src" /> 
          <span>${data.musicList[i].title}</span>
        </a>
      </td>
      <td>
      <a href="#">
      <span class="material-symbols-outlined">favorite</span>
        </a>
      </td>
      <td>
      <a href="#">
      <i class="bi bi-plus-lg"></i>
      </a>
      </td>
      <td>
        <a href="#">
          <span class="material-symbols-outlined">list</span>
        </a>
      </td>
      </tr>
    `;

    $('#table-body').append(row);

  }

  // Add click event listener to each row
  $('#table-body').on('click', 'tr', function () {
    var clickedRowIndex = $(this).index();
    if (!isClickEventRegistered) {
      control.register();
      isClickEventRegistered = true;
    }
    control.insert(clickedRowIndex);
  });
}


