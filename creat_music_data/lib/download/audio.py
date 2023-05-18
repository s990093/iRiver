"""main fun download song and get info in music list"""
import os
import time
import datetime
import json
from pytube import YouTube
from retrying import retry
from tqdm import tqdm
import threading
import urllib
from pydub import AudioSegment
from pytube import Playlist
from pytube.cli import on_progress
# 自製
from . import y2mate


class downloader:
    def __init__(self, music_ID :str, artist :str , relative: str = "media"):
        super().__init__()
        self.relative = relative
        self.music_ID = music_ID 
        self.artist = artist
        self.url = f"https://www.youtube.com/watch?v={self.music_ID}"
        self.path =     os.path.join(self.relative, self.artist, "songs")
        self.mp4_path = os.path.join(self.relative, self.artist, "songs", f"{self.music_ID}.mp4")
        self.mp3_path = os.path.join(self.relative, self.artist, "songs", f"{self.music_ID}.mp3")


    def download_audio(self):
        """dow method"""
        if self.check_path():
            return True
        yt = YouTube(url= self.url , on_progress_callback= on_progress)
        try:
            audio_stream = yt.streams.filter(only_audio=True).first()
            file_path = os.path.join(self.path, f"{self.music_ID}.mp4")
            audio_stream.download(filename= file_path)

            # self.convert_to_mp3()
         
            return True
        except Exception as e:
            print(f"download audio {e}")
            try:
                # change download method
                return y2mate.download_audio(music_ID= self.music_ID, artist= self.artist)
            except Exception as e:
                 print(f' y2mate {e}')
                 return False
    
    def check_path(self):
        # if os.path.isfile(os.path.join(self.path, f"{self.music_ID}.mp4")):
        #        os.remove(os.path.join(self.path,  f"{self.music_ID}.mp4"))

        if os.path.isfile(os.path.join(self.path, f"{self.music_ID}.mp3")):
            print(f"{self.music_ID}.mp3 already exists in {self.path}")
            return True
        else:
            os.makedirs(self.path, exist_ok=True)
            return False
    
    # def convert_to_mp3(self):
    #         audio = AudioSegment.from_file(self.mp4_path)
    #         audio.export(self.mp3_path, format="mp3")
    #         os.remove(self.mp4_path)


def get_play_list( artist_url):
        "get list music information"
        playlist = Playlist(artist_url)
        return playlist

# dow = downloader(music_ID="n5YS6Fo_bZ0", artist='htllo')
# print(dow.download_audio())
# # dow.download_all_song(artist_url= "https://www.youtube.com/playlist?list=PLkZYq_B674dBCKNtGC-8226T6jpBGilso")
