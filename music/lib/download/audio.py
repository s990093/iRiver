import os
import time
import datetime
import json
from pytube import YouTube
from retrying import retry
from tqdm import tqdm
import threading


def download_audio(params):
    def _download_with_retry():
        retry_count = 0
        while True:
            try:
                yt = YouTube(params['url'])
                break
            except Exception as e:
                retry_count += 1
                if retry_count > params.get('max_retry', 3):
                    raise e
                print(f"Error: {e}. Retrying in 2 seconds...")
                time.sleep(2)

        mp3_filename = f"{params['ID']}.mp3"
        mp3_path = os.path.join(params['output_path'], mp3_filename)
        if os.path.exists(mp3_path):
            print(f"{mp3_filename} already exists in {params['output_path']}")
            return None

        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            print("Error: No audio stream found for the video.")
            return None

        # Download the audio stream
        audio_stream.download(
            output_path=params['output_path'], filename=mp3_filename)

        # Update the metadata
        yt.register_on_progress_callback(
            lambda stream, chunk, bytes_remaining: None)  # Disable the progress bar
        song_info = {
            "artist": params['original_artist'],
            "title": params['title'],
            "music_ID": params['ID'],
            "artist_url": params['artist_url'],
            "keywords": yt.keywords,
            "views": yt.views,
            "publish_time": yt.publish_date.isoformat(),
        }
        print(f"Download complete! MP3 file saved in {mp3_path}")
        return song_info

    try:
        song_info = _download_with_retry()
        return song_info

    except Exception as e:
        # print(f"Error downloading video {params['title']}. Skipping...")
        print(e)
        return None
