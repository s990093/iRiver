import { initial } from '../../../static/js/music_list/drive.js';
import { Control } from "../../../static/js/music_list/control.js";

let db_data
// let music_list
const isBigPlayerDisplayed = true;
var isClickEventRegistered = false;

const audio = document.getElementById('myaudio');


if (query) {
  loading(true);
  fetch(`/query_db_song?query=${query}`)
    .then(response => response.json())
    .then(music_list => {
      console.log('db_data', music_list)
      paush_db_data(music_list)
    });
  fetch(`/query_web_song?query=${query}`)
    .then(response => response.json())
    .then(music_list => {
      console.log('search data', music_list)
      paush_web_data(music_list);
    });
  query = null
}


function loading(isLoading) {
  const loading = document.getElementById("loading");
  if (isLoading) {
    loading.style.display = "block";
    table_title.style.display = "none";
  } else {
    loading.style.display = "none";
    table_title.style.display = "block";
  }
}

function table_template(song, i, isWeb) {
  var icon = "database"
  if (isWeb) icon = "language"
  var row = `
  <tr>
    <td>
      <a href="#"
        ><img
          src="${song.img_url || "https://via.placeholder.com/720x405.png?text=No+Image"}"
          alt="none"
          width="70"
          style="margin-right: 20px"
        /><span>${song.title}</span></a
      >
    </td>
    <td>
      <span class="love-icon" style="text-align: right"
        ><a href="#"><i class="far fa-heart"></i></a
      ></span>
    </td>
    <td style="text-align: right">
      <a href="/music_list/?artist=${song.artist}&index=${i}" style="margin-right: 20px"
        ><span class="artist-text" style="margin-left: 20px; margin-right: 20px"
          >${song.artist}</span
        ><img src="${song.artist_img_url || "https://via.placeholder.com/720x405.png?text=No+Image"}" alt="none" width="30" /></a
      ><span class="material-symbols-outlined">${icon}</span>
    </td>
  </tr>
    `
  return row
}
function paush_web_data(music_list) {
  loading(false)
  for (var i = 0; i < music_list.length; i++) {
    $('#table-body').append(table_template(music_list[i], i, true));
  }
  // $('#table-body').on('click', 'tr', function () {
  //   var clickedRowIndex = $(this).index();
  //   if (!isClickEventRegistered) {
  //     control.register();
  //     isClickEventRegistered = true;
  //   }
  //   control.insert(clickedRowIndex);
  // });
}
function paush_db_data(music_list) {
  const control = new Control(audio, music_list, true, false, true);
  for (var i = 0; i < music_list.length; i++) {
    music_list[i].img_url = '/media/' + music_list[i]['artist'] + '/img/' + music_list[i]['music_ID'] + '.jpg';
    music_list[i].artist_img_url = '/media/' + music_list[i]['artist'] + '/img/artist.jpg';
    $('#table-body').append(table_template(music_list[i], false));
  }
  $('#table-body').on('click', 'tr', function () {
    var clickedRowIndex = $(this).index();
    if (!isClickEventRegistered) {
      control.register();
      isClickEventRegistered = true;
    }
    control.insert(clickedRowIndex);
  });
}

const spinners = document.querySelectorAll('.spinner-grow');
spinners.forEach((spinner, index) => {
  spinner.style.setProperty('--delay', `${index * 0.1}s`);
  setTimeout(() => {
    spinner.style.display = 'block';
  }, index * 100);
});