export function table_template(song, i, isWeb, method = 'result', music_list = 1) {
  var icon = isWeb ? "language" : " database";
  var className = isWeb ? "web-data" : "db-data";
  var icon_class = 'far fa-heart';
  var icon_class_name = 'add';
  
  switch (method) {
    case 'result':
      icon_class = 'far fa-heart';
      icon_class_name = 'add';
      break;
    case 'music_list':
      icon_class = 'fa-light fa-trash';
      icon_class_name = 'delete';
      break;
    default:
      icon_class = 'far fa-heart';
      icon_class_name = 'add';
      break;
  }

  var row = `
    <tr>
      <td>
        <a href="#" class="${className}" value = ${i}>
          <img src="${song.img_url || "https://via.placeholder.com/720x405.png?text=No+Image"}" alt="none" width="70" style="margin-right: 20px" />
          <span>${song.title}</span>
        </a>
      </td>
      <td>
        <span class="love-icon" style="text-align: right">
          <a href="#" value=${song.music_ID}><i class="far fa-heart"></i></a>
        </span>
      </td>
      <td>
        <a href="#" class="${icon_class_name}" value=${song.music_ID} data-music_list = "${music_list}"><i class="${icon_class}"></i></a>
      </td>
      <td style="text-align: right">
        <a href="/music/music_list/?artist=${song.artist}&index=${i}" style="margin-right: 20px">
          <span class="artist-text" style="margin-left: 20px; margin-right: 20px">${song.artist}</span>
          <img src="${song.artist_img_url || "https://via.placeholder.com/720x405.png?text=No+Image"}" alt="none" width="30" />
        </a>
        <span class="material-symbols-outlined">${icon}</span>
      </td>
    </tr>
      `
  return row
}