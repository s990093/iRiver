from pytube import Playlist
from pytube import YouTube
import re
# 自製
from lib.web_scutter.music_list import query_music_list_urls
from lib.clear_str import clear_str


class PlaylistManager:
    def __init__(self, artist_url):
        self.url = artist_url
        self.music_ID_list = []

    def extract_music_ids(self):
        res = query_music_list_urls(artist_url=self.url)
        print(len(res))
        for item in res:
            p = Playlist(item)
            try:
                if p:
                    for url in p.video_urls:
                        music_ID = re.search(
                            r'(?<=v=)[^&]+', url).group(0)[-11:]
                        print(music_ID)
                        if music_ID not in self.music_ID_list:
                            url = f"https://www.youtube.com/watch?v={music_ID}"
                            yt = YouTube(url)

                            music_info = {
                                "music_ID": music_ID,
                                "title": yt.title
                            }
                            self.music_ID_list.append(music_info)
            except Exception as e:
                pass

        return self.music_ID_list


# 使用示例
artist_url = "https://www.youtube.com/@nbuna/featured"

playlist_manager = PlaylistManager(artist_url)
music_ID_list = playlist_manager.extract_music_ids()

print(music_ID_list)