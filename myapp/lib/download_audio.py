from pytube import YouTube
from moviepy.editor import *
import os
def action(url):
    try:
        yt = YouTube(url)
        output_path = "media/music/"
        os.makedirs(output_path, exist_ok=True)

        # 替换文件名中的特殊字符
        title = yt.title.replace("/", "-")
        filename = f"{title}.mp4"

        print("Download in progress...")
        # stream = yt.streams.filter(only_audio=True).first()
        yt.streams.filter().get_audio_only().download(output_path=output_path, filename=filename)

        # 将 MP4 文件转换为 MP3 文件
        mp4_file_path = os.path.join(output_path, filename)
        mp3_file_path = os.path.join(output_path, os.path.splitext(filename)[0] + ".mp3")
        audio_clip = AudioFileClip(mp4_file_path)
        audio_clip.write_audiofile(mp3_file_path)

        # 删除原始的 MP4 文件
        os.remove(mp4_file_path)

        # print("Download complete!")
        return "Download complete!"
    except Exception as e:
        print(e)

