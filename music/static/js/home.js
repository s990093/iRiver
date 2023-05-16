import { Control } from "../../../static/js/music_list/control.js";
import { table_template } from "../../../static/js/table.js";
import { fetch_dow_all_songs, fetch_dow_song } from "../../../static/js/fetch.js";
import { insert_my_music_list } from "../../../static/js/music_list/emement.js";
import { FaController } from "../../../static/js/music_list/add-favorite.js";
// import { fetch_dow_all_songs, fetch_dow_song, fetch_is_song_exit } from "../../../static/ts/fetch.ts";


const audio = document.getElementById('myaudio');
var isClickEventRegistered = false;
const control = new Control({
  audio: audio,
  isPlayerShow: false,
});
var length = 0;

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
        console.log('db_data', data.music_list);
        paush_db_data(data.music_list);
        length = data.music_list.length;
      }
    });
  query = null
  const fa = new FaController();
}





function paush_web_data(music_list) {
  loading(true);
  for (var i = 0; i < music_list.length; i++) {
    $('#table-body').append(table_template({
      song: music_list[i],
      i,
      isWeb: true,
      list: "web"
    }));
  }
  control.add_music_list(music_list, "web");


  $('tr td a.web-data').on('click', async function () {
    loading(true);
    var list = $(this).attr('data-list');
    var index = $(this).attr('value');
    try {
      const success = await fetch_dow_song(music_list[index]);
      loading(false);
      if (success) {
        if (!isClickEventRegistered) {
          control.register();
          isClickEventRegistered = true;
        }
        control.insert(index, list);
        fetch_dow_all_songs(music_list[index].artist_url, music_list[index].artist);
      }
    } catch (error) {
      console.error(error);
    }
  });
  loading(false)
}

function paush_db_data(music_list) {
  loading(true);
  for (var i = 0; i < music_list.length; i++) {
    music_list[i].img_url = '/media/' + music_list[i]['artist'] + '/img/' + music_list[i]['music_ID'] + '.jpg';
    music_list[i].artist_img_url = '/media/' + music_list[i]['artist'] + '/img/artist.jpg';

    $('#table-body').append(table_template({
      song: music_list[i],
      i,
      isWeb: false,
      list: "db"
    }));
    loading(false);
  }
  control.add_music_list(music_list, "db");

  $('tr td  a.db-data').on('click', async function () {
    var index = $(this).attr('value');
    var list = $(this).attr('data-list');
    // console.log('clicked on element with index:', index);
    if (!isClickEventRegistered) {
      control.register();
      isClickEventRegistered = true;
    }
    control.insert(index, list);
  });
  loading(false)
}

const spinners = document.querySelectorAll('.spinner-grow');
spinners.forEach((spinner, index) => {
  spinner.style.setProperty('--delay', `${index * 0.1}s`);
  setTimeout(() => {
    spinner.style.display = 'block';
  }, index * 100);
});


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


// $('#table-body').on('click', '.love-icon a', async function () {
//   $(this).find('i').toggleClass('far fas');
//   var music_ID = $(this).attr('value');
//   // const isSongExist = await fetch_is_songisClickEventRegistered_web _exit(music_ID);
//   // if (isSongExist)
//   await insert_my_music_list(music_ID, 1, true, 'insert');

// });

// $('#table-body').on('click', '.add', async function () {
//   $(this).find('i').toggleClass('far fas');
//   var music_ID = $(this).attr('value');
//   // const isSongExist = await fetch_is_song_exit(music_ID);
//   // if (isSongExist)
//   await insert_my_music_list(music_ID, 2, false, 'insert');
// });




