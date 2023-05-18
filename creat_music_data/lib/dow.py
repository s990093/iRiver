"""直接使用  不須額外"""
import os 
import logging
import concurrent.futures
import threading
from typing import List
import glob
# 自製
import lib.download.img as img
import lib.download.y2mate as y2mate
from  lib.download.audio import downloader
# import sql


#         log(music_ID= music_ID , artist=artist, success=res)

import concurrent.futures
import threading
from typing import List
import os

def download(music_ID_list: List[str], artist: str, img_url: str = None, 
             cover_img_url: str = None, artist_img_url: str = None,  
             only_dow_song: bool = False, max_thread: int = 10 , relative: str = "media") -> List[str]:
    
    class WorkerThread(threading.Thread):
        def __init__(self, music_ID, artist, only_dow_song):
            super().__init__()
            self.relative = relative
            self.music_ID = music_ID
            self.artist = artist
            self.only_dow_song = only_dow_song
            self.result = None
            self.audio = downloader(music_ID= self.music_ID , artist= self.artist)

        def run(self):
            self.result = self.audio.download_audio()
            img.download_img(url= f"https://i.ytimg.com/vi/{self.music_ID}/hqdefault.jpg?" ,
                                      file_name=f"{self.music_ID}.jpg", file_dir= os.path.join(self.relative , self.artist , "img"))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_thread) as executor:
        futures = []
        for music_ID in music_ID_list:
            t = WorkerThread(music_ID=music_ID, artist=artist, only_dow_song=only_dow_song)
            futures.append(executor.submit(t.run))
        
        # 等待所有執行緒完成並獲取結果
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())


    file_pattern = os.path.join(relative, "songs", "*.mp4")
    file_list = glob.glob(file_pattern)

    for file_path in file_list:
        os.remove(file_path)

    return True


