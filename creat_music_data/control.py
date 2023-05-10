import json
import concurrent.futures
import threading
# 自製
from lib.web_scutter.youtube import query_youtube
from lib.web_scutter.music_list import query_music_list

from lib.dow import download
import lib.sql.sql as sql
import lib.sql.config as config
from lib.web_scutter.music_list import query_music_list
from lib.web_scutter.music_ID_info import get_music_ID_info

class Controller: 
    def __init__(self , artist_list: str, params , max_thread: int =2):
        """控制下在 跟上傳資料庫  回傳bool """
        super().__init__()
        self.artist_list = artist_list
        self.max_thread = max_thread
        self.local =  params['local']
        self.style = params['style']
        self.country = params['country']
        self.language = params['language']

        self.mysql = sql.SQL(config= config.DB_CONFIG)
        self.mysql.create_tables()

    def run(self):
        for artist in self.artist_list:
          music_list_infos, artist = query_youtube(artist= artist)
          self.download_songs(music_list_infos= music_list_infos , artist= artist)
    

    def query(artist: str):
        statistics = json.loads(query_youtube(artist= artist))
        artist_url = statistics["most_common_artist_url"]
        artist = statistics["most_common_artist"]
        return query_music_list(url= artist_url, artist=  artist) , artist 
     
    def download_songs(self , music_list_infos : list , artist: str):
        download_song_infos =[]
        # 組合
        for song in music_list_infos:
            music_ID_info = get_music_ID_info(music_ID= song['music_ID'])
            download_song_infos.append({
                "artist": artist,
                "music_ID": song["music_ID"],
                'description': music_ID_info['description'],
                'keywords':  music_ID_info['keywords'],  
                'ch_lyrics': music_ID_info['ch_lyrics'],
                'en_lyrics': music_ID_info['en_lyrics'],
                'views': music_ID_info['views'],
                'publish_time': music_ID_info['publish_time'],  
            })
        # 分割
        music_ID_list_chunks = [ download_song_infos[x:x+8] for x in range(0, len(   download_song_infos), 10)]

        for chunk in music_ID_list_chunks:
            success = download( music_ID_list=[song['music_ID'] for song in chunk], 
                                artist=artist , 
                                only_dow_song=True, max_thread= 3
                            )
            if success:
                self.push_data( music_list_infos = chunk)

    def push_data(self ,  music_list_infos : list , success: bool = True):
        params = []
        for song_info in music_list_infos:
            params.append({
                'artist': song_info['artist'],
                'title': song_info['title'],
                'music_ID': song_info['music_ID'],
                'album': 'null',
                'label': 'null',
                'artist_url': song_info['artist_url'],
                'sources': self.local,
                'download_status': success,
                'style': self.style,
                'country': self.country,
                'language': self.language,
                'description': song_info['description'],
                'keywords':  song_info['keywords'],  
                'ch_lyrics': song_info['ch_lyrics'],
                'en_lyrics': song_info['en_lyrics'],
                'views': song_info['views'],
                'release_year': '0',
                'publish_time': song_info['publish_time'],  
            })
        self.mysql.save_data(song_infos=json.dumps(params, indent=4))
        self.mysql.close()

        