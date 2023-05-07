import { Control } from "../../../static/js/music_list/control.js";
import { table_template } from "../../../static/js/table.js";
const audio = document.getElementById('myaudio');

var isClickEventRegistered_web = false
var isClickEventRegistered_db = false
var length = 0
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


function paush_web_data(music_list) {
  const control_web = new Control(audio, music_list, true, false, true);
  loading(true);
  for (var i = 0; i < music_list.length; i++) {
    $('#table-body').append(table_template(music_list[i], i, true));
  }
  $('tr td a.web-data').on('click', function () {
    loading(true);
    var index = $(this).attr('value');
    // console.log('clicked on element with index:', index);
    fetch(`/music/download?song_info=${encodeURIComponent(JSON.stringify(music_list[index]))}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          fetch_dow_all_songs(music_list[index].artist_url, music_list[index].artist);
          console.log('success get music on db');
          if (!isClickEventRegistered_web) {
            control_web.register();
            isClickEventRegistered_web = true;
          }
          control_web.insert(index)
        } else {
          alert('Error');
        }
        loading(false);
      });
  });
  loading(false);
}

function fetch_dow_all_songs(artist_url, artist) {
  fetch(`/music/download_songs?artist_url=${artist_url}&${artist}`)
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        console.log('dow all songs on db');
      }
    });
}

function paush_db_data(music_list) {
  const control_db = new Control(audio, music_list, true, false, true);
  for (var i = 0; i < music_list.length; i++) {
    music_list[i].img_url = '/media/' + music_list[i]['artist'] + '/img/' + music_list[i]['music_ID'] + '.jpg';
    music_list[i].artist_img_url = '/media/' + music_list[i]['artist'] + '/img/artist.jpg';

    $('#table-body').append(table_template(music_list[i], i, false,));
  }
  $('tr td  a.db-data').on('click', function () {
    var index = $(this).attr('value');
    // console.log('clicked on element with index:', index);
    if (!isClickEventRegistered_db) {
      control_db.register();
      isClickEventRegistered_db = true;
    }
    control_db.insert(index);
  });
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
        }).then(response => {
          if (response.ok) {
            // 保存成功
            console.log('保存成功');
          } else {
            // 保存失败
            console.log('保存失败');
          }
        });
        // .then(response => response.json())
        // .then(data => {
        //   alert(data)
        // })
        // .catch(error => console.error(error));
      } else {
        location.href = "/user/login/";
      }
    });
});

$('#table-body').on('click', '.add', function () {
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
            music_list: 2,
            method: 'insert'
          })
        }).then(response => {
          if (response.ok) {
            // 保存成功
            console.log('保存成功');
          } else {
            // 保存失败
            console.log('保存失败');
          }
        });
        // .then(response => response.json())
        // .then(data => {
        //   alert(data)
        // })
        // .catch(error => console.error(error));
      } else {
        location.href = "/user/login/";
      }
    });
});

