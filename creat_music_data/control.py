import json
# 自製
from lib.web_scutter.youtube import query_youtube
from lib.web_scutter.music_list import query_music_list

from lib.dow as dow

class Controller:
    def __init__(self , artist_list: str , max_threads: int =2):
        """控制下在 跟上傳資料庫  回傳bool """
        super().__init__()
        self.artist_list = artist_list
        self.max_threads = max_threads

    def run(self):
        """跑"""
        for artist in self.artist_list:
            statistics = json.loads(query_youtube(artist= artist))
            music_ID_list = query_music_list(url= statistics["most_common_artist_ur"],
                                             artist= statistics["most_common_artist"])
            

    def query(artist: str):
        return query_youtube(artist= artist)
    
    def download(music_ID):
        d