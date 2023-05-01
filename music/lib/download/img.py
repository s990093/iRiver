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
import base64


def download_img(url, file_name, file_dir) ->bool:
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_path = os.path.join(file_dir, file_name)
    if os.path.exists(file_path):
        print(f"圖片已經存在 {file_path}")
        return False
    response = requests.get(url)
    with open(file_path, 'wb') as f:
        f.write(response.content)

    print(f"圖片已下載並儲存到 {file_path}")
    return True

def download_img_base64(url, file_name, file_dir) ->bool:
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    image_binary = base64.b64decode(url.split(",")[1])
    file_path = os.path.join(file_dir, file_name)
    if os.path.exists(file_path):
        print(f"圖片已經存在 {file_path}{file_name}")
        return False
    with open(file_path, 'wb') as f:
        f.write(image_binary)

    print(f"圖片已下載並儲存到 {file_path}")
    return True


