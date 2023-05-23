from pytube import Playlist
from pytube import YouTube
import concurrent.futures
import re
# 自製
from lib.web_scutter.music_list import query_music_list_urls
from lib.web_scutter.clear_str import clear_str


class PlaylistManager:
    def __init__(self, artist_url, max_thread=5):
        self.max_thread = max_thread
        self.url = artist_url
        self.music_ID_list = []
        self.playlist_urls = []

    def query(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_thread) as executor:
            futures = []
            for i in range(5):
                future = executor.submit(
                    query_music_list_urls, self.artist_url)
                futures.append(future)

            # 收集返回结果
            results = []
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                results.append(result)

            # 找到长度最长的结果并返回
            longest_result = max(results, key=lambda x: len(x))
            return longest_result

    def extract_music_ID_list(self):
        self.query()
        for item in self.playlist_urls:
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
music_ID_list = playlist_manager.extract_music_ID_list()

print(music_ID_list)
