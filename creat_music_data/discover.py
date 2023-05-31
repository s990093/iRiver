import os
import concurrent.futures
import json
from lib.dow import download
# 自製
from lib.web_scutter.discover.hot import get_hot_song_info
import lib.download.img as img
from lib.sql.sql import SQL
import lib.sql.config as config
from lib.web_scutter.iocn import query_artist_iocn_src
from lib.web_scutter.music_ID_info import get_music_ID_info
from lib.web_scutter.summary import query_summary


def download_song(song: dict):
    path = os.path.join(
        "media", song['artist'], "songs", f"{song['music_ID']}.mp3")

    if os.path.exists(path=path):
        return True

    music_ID_list = [song['music_ID']]
    # 使用 ThreadPoolExecutor 讓下載封面圖片和維基百科摘要的工作可以同時進行
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # 下載artist 小圖``
        # executor.submit(img.download_img(url=song['artist_img_url'], file_name='artist.jpg',
        #   file_dir=f"media/{song['artist']}/img/"))

        # 下載 封面
        executor.submit(img.download_img_base64(url=executor.submit(query_artist_iocn_src, song['artist']).result(),
                                                file_name='cover.jpg', file_dir=f"media/{song['artist']}/img/"))
        # music_ID info
        music_ID_info = executor.submit(
            get_music_ID_info, song['music_ID']).result()

        # dow summary
        summary = executor.submit(
            query_summary, song['artist'])  # 取得歌手維基百科摘要

        # dow song
        success = download(music_ID_list=music_ID_list,
                           artist=song['artist'],
                           only_dow_song=True)

    params = [{
        'artist': song['artist'],
        'title': song['title'],
        'music_ID': song['music_ID'],
        'album': 'null',
        'label': 'null',
        'artist_url': song['artist_url'],
        'sources': 'web',
        'download_status': success,
        'style': 'null',
        'country': 'null',
        'language': 'null',
        'description': music_ID_info['description'],
        'keywords':  music_ID_info['keywords'],
        'ch_lyrics': music_ID_info['ch_lyrics'],
        'en_lyrics': music_ID_info['en_lyrics'],
        'rating': music_ID_info['rating'],
        'views': music_ID_info['views'],
        'release_year': '0',
        'publish_time': music_ID_info['publish_time'],
    }]

    if success is not None:
        mysql = SQL(config.DB_CONFIG)
        mysql.create_tables()  # 建立資料庫表格
        mysql.save_data(song_infos=json.dumps(params),
                        summary=summary.result())  # 儲存歌曲資訊
        mysql.close()  # 關閉資料庫連線
        return True
    else:
        return False


if __name__ == '__main__':
    res = get_hot_song_info()
    artist_channels = []
    for song in res:
        artist_channels.append(song['artist_url'])
        download_song(song=song)
