import os
import time
import datetime
import json
from pytube import YouTube
from retrying import retry
from tqdm import tqdm
import threading


class downloader:
    def __init__(self, music_ID, artist):
        self.music_ID = music_ID
        self.artist = artist
        self.path = os.path.join("media", artist, "songs")

    def download(self):
        if self.check_path():
            return True
        yt = YouTube(f"https://www.youtube.com/watch?v={self.music_ID}")
        try:
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_stream.download(
                output_path=self.path, filename=f"{self.music_ID}.mp3")
            yt.register_on_progress_callback(
                lambda stream, chunk, bytes_remaining: None)

            print(self.path)
            return True
        except Exception as e:
            print(e)
            return False

    def check_path(self):
        if os.path.exists(os.path.join(self.path, self.music_ID)):
            print(f"{self.music_ID} already exists in {self.path}")
            return True
        else:
            return False


dow = downloader(music_ID="n5YS6Fo_bZ0", artist='12312')
dow.download()
