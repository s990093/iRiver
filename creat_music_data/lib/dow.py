"""直接使用  不須額外"""
import os 
import logging
import concurrent.futures
import threading
from typing import List
# 自製
import lib.download.img as img
import lib.download.y2mate as y2mate
from  lib.download.audio import downloader
# import sql


#         log(music_ID= music_ID , artist=artist, success=res)

import concurrent.futures
import threading
from typing import List

def download(music_ID_list: List[str], artist: str, img_url: str = None, 
             cover_img_url: str = None, artist_img_url: str = None,  
             only_dow_song: bool = False, max_thread: int = 10) -> List[str]:
    
    class WorkerThread(threading.Thread):
        def __init__(self, music_ID, artist, only_dow_song):
            super().__init__()
            self.music_ID = music_ID
            self.artist = artist
            self.only_dow_song = only_dow_song
            self.result = None
            self.audio = downloader(music_ID= self.music_ID , artist= self.artist)

        def run(self):
            self.result = self.audio.download_audio()
            img.download_img(url= f"https://i.ytimg.com/vi/{self.music_ID}/hqdefault.jpg?" ,
                                      file_name=f"{self.music_ID}.jpg", file_dir=f"media/{self.artist}/img/")
            # log(music_ID= self.music_ID, artist=self.artist , success= self.result)
            if not self.only_dow_song:
                if cover_img_url:
                    img.download_img_base64(url=cover_img_url, file_name='cover.jpg', file_dir=f"media/{self.artist}/img/")
                if artist_img_url:
                    img.download_img(url=artist_img_url, file_name='artist.jpg', file_dir=f"media/{self.artist}/img/")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_thread) as executor:
        futures = []
        for music_ID in music_ID_list:
            t = WorkerThread(music_ID=music_ID, artist=artist, only_dow_song=only_dow_song)
            futures.append(executor.submit(t.run))
        
        # 等待所有執行緒完成並獲取結果
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    
    return results



def log(music_ID, artist, success):
    log_dir = './log'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, 'dow_song.log')
    print(log_file_path)
    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[file_handler])

    if success:
        logging.info(f"Downloaded music '{music_ID}' by '{artist}' successfully.")
    elif success is False:  
        logging.error(f"Failed to download music '{music_ID}' by '{artist}'.")
    elif success is None:
        logging.warning(f"Already exists '{music_ID}' by '{artist}'.")
