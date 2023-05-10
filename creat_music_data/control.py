import json
# 自製
from lib.web_scutter.youtube import query_youtube
from lib.web_scutter.music_list import query_music_list

from lib.dow import download
import lib.sql.sql as sql
import lib.sql.config as config
from lib.web_scutter.music_list import query_music_list
from lib.web_scutter.music_ID_info import get_music_ID_info

class Controller: 
    def __init__(self , artist_list: str, params , max_threads: int =2):
        """控制下在 跟上傳資料庫  回傳bool """
        super().__init__()
        self.artist_list = artist_list
        self.max_threads = max_threads
        self.local =  params['local']
        self.style = params['style']
        self.country = params['country']
        self.language = params['language']

        self.mysql = sql.SQL(config= config.DB_CONFIG)
        self.mysql.create_tables()

    def run(self):
        for artist in self.artist_list:
          self.download(music_list_infos= query_youtube(artist= artist))
    

    def query(artist: str):
        statistics = json.loads(query_youtube(artist= artist))
        artist_url = statistics["most_common_artist_url"]
        return query_music_list(url= statistics["most_common_artist_url"], artist= statistics["most_common_artist"]) , 
    
    def download(self , music_list_infos : list):
        music_ID_list_chunks = [music_list[x:x+8] for x in range(0, len(music_list), 10)]

        for chunk in music_ID_list_chunks:
            success = download( music_ID_list=[song['music_ID'] for song in chunk], 
                                artist=artist , 
                                only_dow_song=True, max_thread= 3
                            )
            if success:
                self.push_data()

    def push_data(self , song_info : list , success: bool = True):
        params = [{
            'artist': song_info['artist'],
            'title': song_info['title'],
            'music_ID': song_info['music_ID'],
            'album': 'null',
            'label': 'null',
            'artist_url': song_info['artist_url'],
            'sources': 'pytube',
            'download_status': success,
            'style': self.style,
            'country': self.country,
            'language': self.language,
            'description': music_ID_info['description'],
            'keywords':  music_ID_info['keywords'],  
            'ch_lyrics': music_ID_info['ch_lyrics'],
            'en_lyrics': music_ID_info['en_lyrics'],
            'views': music_ID_info['views'],
            'release_year': '0',
            'publish_time': music_ID_info['publish_time'],  
        }] 
        self.mysql.save_data(song_infos=json.dumps(params, indent=4))
        self.mysql.close()

        