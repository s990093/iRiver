import { Control } from "../../../static/js/music_list/control.js";

const audio = document.getElementById('myaudio');

var isClickEventRegistered_web = false
var isClickEventRegistered_db = false
var length
if (query) {
  loading(true);
  fetch(`/music/query_web_song?query=${query}`)
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        console.log('search data', data.music_list)
        paush_web_data(data.music_list);
      } else {
        alert('web search error', data.music_list);
      }
    });
  fetch(`/music/query_db_song?query=${query}`)
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        console.log('db_data', data.music_list)
        paush_db_data(data.music_list)
        length = data.music_list.length;
      } else {
        length = 0;
        alert("db search error", data.music_list);
      }

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
      <a href="#" class="play"
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
        ><a href="#" value=${song.music_ID}><i class="far fa-heart"></i></a
      ></span>
    </td>
    <td style="text-align: right">
      <a href="/music/music_list/?artist=${song.artist}&index=${i}" style="margin-right: 20px"
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
  const control_web = new Control(audio, music_list, true, false, true);
  for (var i = 0; i < music_list.length; i++) {
    $('#table-body').append(table_template(music_list[i], i, true));
  }
  $('#table-body').on('click', 'tr .play', function () {
    loading(true);
    var clickedRowIndex = $(this).index();
    if (clickedRowIndex >= length) {
      fetch(`/music/download?song_info=${encodeURIComponent(JSON.stringify(music_list[clickedRowIndex - length]))}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            if (!isClickEventRegistered_db) {
              control_web.register();
              isClickEventRegistered_db = true;
            }
            control_web.insert(clickedRowIndex - length)
          } else {
            alert('Error');
          }
          loading(false);
        });

    }
  });
  loading(false);
}

function paush_db_data(music_list) {
  const control_db = new Control(audio, music_list, true, false, true);
  for (var i = 0; i < music_list.length; i++) {
    music_list[i].img_url = '/media/' + music_list[i]['artist'] + '/img/' + music_list[i]['music_ID'] + '.jpg';
    music_list[i].artist_img_url = '/media/' + music_list[i]['artist'] + '/img/artist.jpg';
    $('#table-body').append(table_template(music_list[i], false));
  }
  $('#table-body').on('click', 'tr .play', function () {
    loading(true);
    var clickedRowIndex = $(this).index();
    // console.log(clickedRowIndex);
    if (clickedRowIndex <= length) {
      if (!isClickEventRegistered_db) {
        control_db.register();
        isClickEventRegistered_db = true;
      }
      control_db.insert(clickedRowIndex);
      loading(false);
    }
    loading(false);
  });
  loading(false);
}

const spinners = document.querySelectorAll('.spinner-grow');
spinners.forEach((spinner, index) => {
  spinner.style.setProperty('--delay', `${index * 0.1}s`);
  setTimeout(() => {
    spinner.style.display = 'block';
  }, index * 100);
});

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


$('#table-body').on('click', '.love-icon a', function () {
  $(this).find('i').toggleClass('far fas');
  fetch(`/user/isLogin/`)
    .then(response => response.json())
    .then(data => {
      if (data.isLogin) {
        var music_ID = $(this).attr('value');
        const csrftoken = getCookie('csrftoken'); 
        fetch('/user/get_user_music_list/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken 
          },
          body: JSON.stringify({
            music_ID: music_ID,
            method: 'insert'
          })
        })
          .then(response => response.json())
          .then(data => {
            alert(data)
          })
          .catch(error => console.error(error));
      } else {
        location.href = "/user/login/";
      }
    });
});

