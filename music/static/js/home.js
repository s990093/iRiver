import { initial } from '../../../static/js/music_list/drive.js';
let db_data
let music_list
const isBigPlayerDisplayed = true;

if (query) {
  loading();
  fetch(`/query_song?query=${query}`)
    .then(response => response.json())
    .then(data => {
      db_data = data
      console.log('db_data', db_data)
      paush_db_data(db_data)
      query = ''
    });
  fetch(`/crawl?query=${query}`)
    .then(response => response.json())
    .then(data => {
      console.log('search data', data)
      music_list = data
      paush_data(data);
      query = ''
    });
}


function loading() {
  const loading = document.getElementById("loading");
  loading.style.display = "block";
  table_title.style.display = "none";
}

function paush_data(data) {
  const loading = document.getElementById("loading");
  const table_title = document.getElementById("table_title");
  const tableBody = document.getElementById("table-body");

  //清空
  // tableBody.innerHTML = "";
  data.videos.forEach((video, index) => {
    const tr = document.createElement("tr");
    const td1 = document.createElement("td");
    const td2 = document.createElement("td");

    // song
    const a = document.createElement("a");
    const song_img = document.createElement("img");
    const song_span = document.createElement("span");
    song_img.src = video.img_url || "https://via.placeholder.com/720x405.png?text=No+Image";
    song_img.alt = "none";
    song_img.width = "70";
    a.href = "#";
    a.dataset.url = video.url;
    song_span.textContent = video.title;

    a.appendChild(song_img);
    song_img.style.marginRight = "20px";
    a.appendChild(song_span);
    song_span.textContent = video.title;

    a.addEventListener('click', event => {
      event.preventDefault();
      // const url = a.dataset.url;
      const loading = document.getElementById("loading");
      loading.style.display = "block";
      fetch(`/download?selection=${index + 1}`)
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            //播放歌曲
            let music_data = {
              videos: [
                {
                  artist: video.artist,
                  music_ID: video.music_ID,
                  title: video.title,
                }
              ]
            };
            initial(isBigPlayerDisplayed, music_data, 0, 0)
            table_title.style.display = "block";
            loading.style.display = "none";
            fetch(`/download_songs?artist_url=${video.artist_url}`)
              .then(response => response.json())
          } else {
            let music_data = {
              videos: [
                {
                  artist: video.artist,
                  music_ID: video.music_ID,
                  title: video.title,
                }
              ]
            };
            initial(isBigPlayerDisplayed, music_data, 0, 0)
            table_title.style.display = "block";
            loading.style.display = "none";
          }
        });
    });

    //artist
    const author = document.createElement("span");
    author.style.marginLeft = "20px";
    const authorImg = document.createElement("img");
    author.classList.add("artist-text");
    const authorLink = document.createElement("a");
    author.textContent = video.artist || "Unknown";
    authorImg.src = video.artist_img_url || "https://via.placeholder.com/50x50.png?text=No+Image";
    authorImg.alt = "none";
    authorImg.width = "30";

    authorLink.appendChild(author);
    author.style.marginRight = "20px";
    authorLink.appendChild(authorImg);
    authorLink.style.marginRight = "20px";

    // love_iocn
    const td3 = document.createElement("td");

    const a_love = document.createElement("a");
    const td_love = document.createElement("span");
    td_love.style.textAlign = "right";
    td_love.classList.add("love-icon"); // 新增 .love 類別
    const heartIcon = document.createElement("i");
    heartIcon.classList.add("far", "fa-heart");
    a_love.href = '#'
    a_love.appendChild(heartIcon);
    td_love.appendChild(a_love);


    // network_icon
    const network_icon = document.createElement("span");
    network_icon.classList.add("material-symbols-outlined");
    network_icon.textContent = "language";


    td1.appendChild(a);
    td2.appendChild(authorLink);
    td2.appendChild(network_icon);
    td2.style.textAlign = "right"; // 將 td2 的 text-align 設置為 "right"
    td3.appendChild(td_love);
    tr.appendChild(td1);
    tr.appendChild(td3);
    tr.appendChild(td2);
    tableBody.appendChild(tr);
  });
  table_title.style.display = "block";
  loading.style.display = "none";
}

function paush_db_data(data) {
  const loading = document.getElementById("loading");
  const table_title = document.getElementById("table_title");
  const tableBody = document.getElementById("table-body");

  for (let i = 0; i < data.length; i++) {
    const tr = document.createElement("tr");
    // song
    const td1 = document.createElement("td");

    const td2 = document.createElement("td");

    const song_img = document.createElement("img");
    const author = document.createElement("span");
    author.style.marginLeft = "20px";
    const authorImg = document.createElement("img");


    // song
    const a = document.createElement("a");

    a.addEventListener('click', event => {
      event.preventDefault();
      const loading = document.getElementById("loading");
      loading.style.display = "block"
      //播放歌曲
      let music_data = {
        videos: [
          {
            artist: data[i]['artist'],
            music_ID: data[i]['music_ID'],
            title: data[i]['title'],
          }
        ]
      };
      initial(isBigPlayerDisplayed, music_data, 0, 0)
      table_title.style.display = "block";
      loading.style.display = "none";
    });

    const song_span = document.createElement("span");
    var img_url = '/media/' + data[i]['artist'] + '/img/' + data[i]['music_ID'] + '.jpg';
    song_img.src = img_url || "https://via.placeholder.com/720x405.png?text=No+Image";
    song_img.alt = "none";
    song_img.width = "70";
    a.href = '#'
    a.appendChild(song_img);
    song_img.style.marginRight = "20px";
    a.appendChild(song_span);
    song_span.textContent = data[i]['title'];

    //artist
    author.classList.add("artist-text"); // 新增 .love 類別
    author.textContent = data[i]['artist'] || "Unknown";
    var artist_img_url = '/media/' + data[i]['artist'] + '/img/artist.jpg';
    authorImg.src = artist_img_url || "https://via.placeholder.com/50x50.png?text=No+Image";
    authorImg.alt = "none";
    authorImg.width = "30";

    const authorLink = document.createElement("a");
    authorLink.href = '/music_list/?artist=' + data[i]['artist'] + '&index=' + i;

    authorLink.appendChild(author);
    author.style.marginRight = "20px";
    authorLink.appendChild(authorImg);
    authorLink.style.marginRight = "20px";

    // love_iocn
    const td3 = document.createElement("td");

    const a_love = document.createElement("a");
    const td_love = document.createElement("span");
    td_love.style.textAlign = "right";
    td_love.classList.add("love-icon"); // 新增 .love 類別
    const heartIcon = document.createElement("i");
    heartIcon.classList.add("far", "fa-heart");
    a_love.href = '#'
    a_love.appendChild(heartIcon);
    td_love.appendChild(a_love);

    // database_icon
    const database = document.createElement("span");
    database.classList.add("material-symbols-outlined");
    database.textContent = "database";


    // 放到tr1
    td2.appendChild(td_love)
    td2.appendChild(authorLink);
    td2.appendChild(database);

    td3.appendChild(td_love);

    td1.appendChild(a);
    td2.style.textAlign = "right"; // 將 td2 的 text-align 設置為 "right"

    tr.appendChild(td1);
    tr.appendChild(td3);
    tr.appendChild(td2);
    tableBody.appendChild(tr);
  }
  table_title.style.display = "block";
  loading.style.display = "none";
}


const spinners = document.querySelectorAll('.spinner-grow');
spinners.forEach((spinner, index) => {
  spinner.style.setProperty('--delay', `${index * 0.1}s`);
  setTimeout(() => {
    spinner.style.display = 'block';
  }, index * 100);
});