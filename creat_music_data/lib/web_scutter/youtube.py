from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json
import re
from collections import Counter
# 自製
from options import get_chrome_options
from  options import get_available_port
from clear_str import clear_str

def query_youtube(query : str) ->json:
    service = Service('chromedriver.exe')
    options = get_chrome_options(port = get_available_port() , is_headLess= True)
    driver = webdriver.Chrome(service = service, options=options) 
    driver.get(f"https://www.youtube.com/results?search_query={query}&sp=EgIQAQ%253D%253D&t=0s-7m")
    music_list = []
    video_elements = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#contents #video-title")))
    for i, video_element in enumerate(video_elements[:10]):
        try:
            url = driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{1+i}]/div[1]/div/div[1]/div/h3/a")
            title = driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{1+i}]/div[1]/div/div[1]/div/h3/a/yt-formatted-string")                  
            artist = driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{1+i}]/div[1]/div/div[2]/ytd-channel-name/div/div/yt-formatted-string/a")     

            # artist_img_url = driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[2]/a/yt-img-shadow/img")
            artist_img_element = video_element.find_elements(By.XPATH, '//*[@id="img"]')
            if artist_img_element:
                artist_img_url = artist_img_element[i].get_attribute("src")
            else:
                artist_img_url = ''
            
            match  = re.search(r'(?<=v=)[^&]+',  url.get_attribute('href'))
            try:
                if match:
                    ID = match.group(0)[-11:]
                else:
                    ID = re.search(r"shorts\/(\w{11})", url.get_attribute('href')).group(1)
            except:
                continue
            video = {}
            video["title"] = title=title.text
            video["music_ID"] = ID
            video["url"] = url.get_attribute("href")
            video["img_url"] = f'https://i.ytimg.com/vi/{ID}/hqdefault.jpg?'
            video["artist"] = artist.text.replace('/', '').replace(' ', '')
            video["artist_url"] = artist.get_attribute("href")
            # video["artist_img_url"] = artist_img_url.get_attribute("src")
            video["artist_img_url"] =  artist_img_url
            music_list.append(video)
        except NoSuchElementException as e:
            print(e)
            pass
    # 统计所有艺术家的出现次数
    artists = [ video["artist"] for video in music_list]
    most_common_artist = Counter(artists).most_common(1)[0][0]
    most_common_artist_url = next(( video["artist_url"] for video in music_list if video["artist"] == most_common_artist and video["artist_img_url"]), "")
    most_common_artist_img_url = next(( video["artist_img_url"] for video in music_list if video["artist"] == most_common_artist and video["artist_img_url"]), "")
     
    # 改變圖片
    for video in music_list:
        if not video["artist_img_url"]:
            artist = video["artist"]
            for video_change in music_list:
                if  video_change['artist'] == artist:
                    video["artist_img_url"] = video_change['artist_img_url']
                    break
    # clear
    for video in music_list:
        video['title'] = clear_str(title=video['title'] , artist=video['artist'])
    
    statistics = {
    'most_common_artist': most_common_artist,
    'most_common_artist_url': most_common_artist_url,
    'most_common_artist_img_url': most_common_artist_img_url,
    }
    # 合併
    # result = {
    # 'music_list': music_list,
    # 'statistics': statistics,
    # }

    json_str = json.dumps(statistics, indent=4)
    return json_str

# r = json.loads(query_youtube('比悲傷更悲傷'))
# print(r)