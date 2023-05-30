/**
 * @typedef {Object} TableTemplateParams
 * @property {string} song - 歌曲
 * @property {number} i - 索引
 * @property {boolean} isWeb - 是否为Web
 * @property {string} [list="org"] - 列表
 * @property {string} [method="result"] - 方法
 * @property {number} [music_list=1] - 音乐列表
 * @property {boolean} [isTest=false] - 是否为测试
 */

/**
 * 表格模板函数
 * @param {TableTemplateParams} params - 参数对象
 */
export function table_template({
  song,
  i,
  isWeb,
  list = "org",
  method = 'result',
  music_list = 1,
  isTest = false
}) {
  var icon = isWeb ? "language" : " database";
  var className = isWeb ? "web-data" : "db-data";
  var icon_class = 'far fa-heart';
  var icon_class_name = 'add';

  switch (method) {
    case 'result':
      icon_class = 'far fa-plus';
      icon_class_name = 'add';
      break;
    case 'music_list':
      icon_class = 'fa-light fa-trash';
      icon_class_name = 'delete';
      break;
    default:
      icon_class = 'far fa-plus';
      icon_class_name = 'add';
      break;
  }

  var row = `
    <tr>
      <td>
      <div>
        <a href="#" class="${className}" value="${i}" data-list="${list}">
          <div class="row">
            <div class="col-3">
              <img
                src="${song.img_url || 'https://via.placeholder.com/720x405.png?text=No+Image'}"
                alt="none"
                width="70"
                style="margin-right: 20px"
                class="img-fluid rounded"
              />
            </div>
            <div class="col-3">
              <span class="d-block">${song.title}</span>
            </div>
          </div>
        </a>
      </div>
      </td>
      <td>
        <span class="love-icon font" style="text-align: right">
          <a href="#" value=${song.music_ID}><i class="far fa-heart"></i></a>
        </span>
      </td>
      <td>
        <a href="#"
          class="${icon_class_name} font"
          vaule="${song.music_ID}" 
          data-music_list = "${music_list}">
            <i class="${icon_class}"></i>
          </a>
      </td>
      <td style="text-align: right">
        <a href="/music/music_list/?artist=${song.artist}&index=${i}" class="icon" style="margin-right: 20px">
          <span class="artist-text" style="margin-left: 20px; margin-right: 20px">${song.artist}</span>
       
        </a>
        <span class="material-symbols-outlined">${icon}</span>
      </td>
    </tr>
      `
  return row;
}