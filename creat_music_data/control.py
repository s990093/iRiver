import json
import concurrent.futures
import threading
import time
# 自製
from lib.web_scutter.youtube import query_youtube
from lib.web_scutter.music_list import query_music_list

from lib.dow import download
import lib.sql.sql as sql
import lib.sql.config as config
from lib.web_scutter.music_list import query_music_list
from lib.web_scutter.music_ID_info import get_music_ID_info
from lib.web_scutter.iocn import query_artist_iocn_src
from lib.web_scutter.summary import query_summary
import lib.download.img as img

class Controller: 
    def __init__(self , artist_list: str, params , max_thread: int =2 , max_retries: int =2):
        """控制下在 跟上傳資料庫  回傳bool """
        super().__init__()
        self.artist_list = artist_list
        self.max_thread = max_thread
        self.max_retries = max_retries
        self.sources =  params['sources']
        self.style = params['style']
        self.country = params['country']
        self.language = params['language']

        self.mysql = sql.SQL(config= config.DB_CONFIG)
        self.mysql.create_tables()
        print("@"*30)
        print("register controller")

    def run(self):
        for query in self.artist_list:
            print(f"Downloading {query}")
            music_list_infos, artist , artist_img_url , artist_url= self.query(query= query)
            self.download_songs(music_list_infos= music_list_infos , artist= artist , 
                                artist_img_url= artist_img_url , artist_url= artist_url)
        return True
    

    def query(self , query: str):
        statistics = json.loads(query_youtube(query= query))
        artist_url = statistics["most_common_artist_url"]
        artist = statistics["most_common_artist"]
        artist_img_url = statistics["most_common_artist_img_url"]
        return query_music_list(url= artist_url, artist=  artist) , artist  , artist_img_url , artist_url
     
    def download_songs(self , music_list_infos : list , artist: str , artist_img_url: str , artist_url: str):
        # 下在cover artist
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # 下載artist 小圖
            executor.submit(img.download_img(url= artist_img_url, file_name='artist.jpg',
                                            file_dir=f"media/{artist}/img/"))

            # 下載 封面
            executor.submit(img.download_img_base64(url= executor.submit(query_artist_iocn_src, artist).result() ,
                                    file_name='cover.jpg', file_dir=f"media/{artist}/img/"))
            # summary
            self.mysql.save_summary(artist= artist,summary= executor.submit(query_summary , artist).result())
            
        download_song_infos =[]
        # 組合
        for song in music_list_infos:
            music_ID_info = get_music_ID_info(music_ID= song['music_ID'])
            download_song_infos.append({
                "artist": artist,
                'title': song['title'],
                "music_ID": song["music_ID"],
                'artist_url': artist_url,
                'description': music_ID_info['description'],
                'keywords':  music_ID_info['keywords'],  
                'ch_lyrics': music_ID_info['ch_lyrics'],
                'en_lyrics': music_ID_info['en_lyrics'],
                'views': music_ID_info['views'],
                'publish_time': music_ID_info['publish_time'],  
            })
        # 分割
        music_ID_list_chunks = [ download_song_infos[x:x+8] for x in range(0, len(download_song_infos), 10)]

        for chunk in music_ID_list_chunks:
            success = download( music_ID_list=[song['music_ID'] for song in chunk], 
                                artist=artist , 
                                only_dow_song=True, max_thread= 4
                            )
            if success:
                # print(chunk)
                self.push_data( music_list_infos = chunk)
        
        return True

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
                'sources': self.sources,
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
        def save():
            self.mysql.save_data(song_infos=json.dumps(params, indent=4))
        count = 0
        # save()

        while True:
            try:
                save()
                break
            except  Exception as e:
                if count == self.max_retries:
                    break
                time.sleep(1)
                save()
                count +=1
        self.mysql.close()

        