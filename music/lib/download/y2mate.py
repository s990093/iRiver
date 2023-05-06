"""下載mp3 使用爬蟲"""
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from tqdm import tqdm   #進度條
import os
import logging
# 自製
import music.lib.web_scutter.options as option

def download_audio(music_ID: str , artist: str ,  num_retries: int =0 ,  max_retries: int = 3) ->bool: 
    '''
    下載指定音樂ID的音頻文件

    Parameters:
        music_ID (str): 音樂ID 

    Returns:
        bool: True
    '''
    song_url = crawl(music_ID= music_ID,  num_retries= num_retries , max_retries= max_retries)
    if song_url is not None:
        res = download(song_url , music_ID , artist= artist)
        return res
    else:
        return False

def crawl(music_ID , num_retries , max_retries):
    # 启动浏览器并打开网页
    service = Service('C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe')  
    options =  option.get_chrome_options(port=option.get_available_port() , is_headLess= False)
    driver = webdriver.Chrome(service=service, options=options)

    success = False
    while not success and num_retries < max_retries:
        try:
            driver.get(f"https://www.youtubepp.com/watch?v={music_ID}")
            # 等待页面加载完成
            wait = WebDriverWait(driver, 10)
            # 执行操作
            audio_btn = wait.until(EC.visibility_of_element_located((By.XPATH , "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[4]/div[1]/div[2]/ul/li[2]/a")))
            ActionChains(driver).move_to_element(audio_btn).click().perform()

            download_btn = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[4]/div[1]/div[2]/div/div[2]/table/tbody/tr/td[3]/button')))
            ActionChains(driver).move_to_element(download_btn).click().perform()

            # 按下確認下載按鈕
            check_download_btn = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div[2]/div/a')))
            ActionChains(driver).move_to_element(check_download_btn ).click().perform()

            # 下載url
            song_element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div[2]/div/a')))
            song_url = song_element.get_attribute('href')
            success = True
        except:
            # 发生异常，继续尝试
            driver.close()
            num_retries += 1
            print(f"Attempt {num_retries} failed, retrying...")
            time.sleep(0.5)  # 等待1秒后重试
    
    if success:
        return song_url
    else:
        return None



def download(url, music_ID , artist):
    response = requests.get(url, stream=True)
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join("media", artist, "songs")

    if not os.path.exists(path):
        os.makedirs(path)            

    file_name = os.path.join(path, f"{music_ID}.mp3")

    if os.path.exists(file_name):
        print(f"{file_name} already exists, skipping...")
        return None

    try:
         # 設定進度條總長度為下載檔案的大小
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, desc="Downloading")
        
        # 寫入檔案
        with open(file_name, 'wb') as f:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
        
        # 關閉進度條
        progress_bar.close()
        return True
    except:
        return False
