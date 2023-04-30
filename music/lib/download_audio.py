import os
from pytube import YouTube
from moviepy.editor import AudioFileClip
import requests
import json
import threading
import time
from moviepy.editor import AudioFileClip
from urllib import request
import urllib
import ssl
from concurrent.futures import ThreadPoolExecutor
import moviepy.editor as mp
from moviepy.video.io.VideoFileClip import VideoFileClip
from selenium import webdriver
from selenium.webdriver.common.by import By
# from .options import get_chrome_options
from googlesearch import search
from selenium.webdriver.chrome.service import Service

def download_img(query :str):
    # 設定搜尋關鍵字和搜尋數量
    keyword = f'{query}團照'
    # 設定 Google 圖片搜尋的 URL
    url = 'https://www.google.com/search?q={}&source=lnms&tbm=isch'.format(keyword)
    # 初始化 Chrome Driver
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    # 設定式等待時間
    driver.implicitly_wait(10)
    # 發送請求
    driver.get(url)
    # 取得圖片 URL
    image_urls = []
    url = driver.find_element(
                    By.XPATH, 
        f" /html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]/div[1]/img")
            
    print(url.get_attribute('src'))
    url = url.get_attribute('src')
    urllib.request.urlretrieve(url, f'{query}.jpg')
    # 關閉瀏覽器
    driver.quit()


def download_img(url, file_name, file_dir):
    file_path = os.path.join(file_dir, file_name)
    if os.path.exists(file_path):
        # print(f"檔案 {file_path} 已存在，跳過下載")
        return
    response = requests.get(url)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    # print(f"圖片已下載並儲存到 {file_path}")


# 下載音樂
def download_music(output_path, url, ID , title ,artist_url ,original_artist, max_threads=4):
    try:
        try:
            yt = YouTube(url)
            print('#'*30)
            print(url)
            
            mp3_filename = f"{ID}.mp3"
            mp3_path = os.path.join(output_path, mp3_filename)
            if os.path.exists(mp3_path):
                print(f"{mp3_filename} already exists in {output_path}")
                return
            
            yt.streams.filter(only_audio=True).get_audio_only().download(
                                    output_path=output_path, 
                                    filename=mp3_filename)
        except Exception as e:
            print(e)
            yt = YouTube(f'https://www.youtube.com/watch?v={ID}')

            mp3_filename = f"{ID}.mp3"
            mp3_path = os.path.join(output_path, mp3_filename)
            if os.path.exists(mp3_path):
                print(f"{mp3_filename} already exists in {output_path}")
                return

            
            yt.streams.filter(only_audio=True).get_audio_only().download(
                                    output_path=output_path, 
                                    filename=mp3_filename)
            
        print( f"Download complete! MP3 file saved in {mp3_path}")
    
        song_info = {
            "artist": original_artist,
            "title": title,
            "music_ID": ID,
            "artist_url": artist_url,
            "keywords": yt.keywords,
            "views": yt.views,
            "publish_time": yt.publish_date.strftime('%Y'),
        }
        # print(type(song_info))
        return song_info
        # return json.dumps(song_info, indent=4)
    
    except Exception as e:
        print(f"Error downloading video {ID}. Skipping...")
        print(e)
        return None



def download( ID , url , img_url  , artist_url , artist_img_url , original_artist , title): 
    output_path = f"media/{original_artist}/music/"
    img_output_path = f"media/{original_artist}/img/"

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        os.makedirs(img_output_path )

    # check if existing
    if os.path.exists(f'{output_path}{ID}.mp3'):
        print(f"{ID}.mp3 already exists in {output_path}")
        return
    # img
    t1 = threading.Thread(target=download_img, args=(img_url , f'{ID}.jpg', img_output_path))
    t2 = threading.Thread(target=download_img, args=(artist_img_url , 'artist.jpg', img_output_path))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    # music

    r = download_music( output_path ,url ,ID ,title , artist_url ,original_artist , max_threads=4)
    return json.dumps(r , indent=4)

