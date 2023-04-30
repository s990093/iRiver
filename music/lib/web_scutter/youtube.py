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
from lib.web_scutter.options import get_chrome_options

def query_youtube(query : str) ->json:
    service = Service('chromedriver.exe')
    options = get_chrome_options(port = 9222)
    # driver = webdriver.Chrome(service = service, options=options) 
    driver = webdriver.Chrome(service = service, options=options) 
    # driver = webdriver.Chrome() 
    start_time = time.time()
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
            if match:
                ID = match.group(0)[-11:]
            else:
                ID = re.search(r"shorts\/(\w{11})", url.get_attribute('href')).group(1)
            music_list = {}
            music_list["title"] = title=title.text
            music_list["music_ID"] = ID
            music_list["url"] = url.get_attribute("href")
            music_list["img_url"] = f'https://i.ytimg.com/vi/{ID}/hqdefault.jpg?'
            music_list["artist"] = artist.text.replace('/', '').replace(' ', '')
            music_list["artist_url"] = artist.get_attribute("href")
            # video["artist_img_url"] = artist_img_url.get_attribute("src")
            music_list["artist_img_url"] =  artist_img_url
            music_list.append(music_list)
        except NoSuchElementException as e:
            print(e)
            pass

    # 统计所有艺术家的出现次数
    artists = [music_list["artist"] for video in music_list]
    most_common_artist = Counter(artists).most_common(1)[0][0]
    most_common_artist_url = next((music_list["artist_url"] for video in music_list if video["artist"] == most_common_artist and video["artist_img_url"]), "")
    most_common_artist_img_url = next((music_list["artist_img_url"] for video in music_list if video["artist"] == most_common_artist and video["artist_img_url"]), "")

    statistics = {
    'most_common_artist': most_common_artist,
    'most_common_artist_url': most_common_artist_url,
    'most_common_artist_img_url': most_common_artist_img_url,
    }
    # 合併
    result = {
    'music_list': music_list,
    'statistics': statistics,
    }

    end_time = time.time()
    print(f"程序运行时间：{end_time - start_time}秒")
    # driver.close()

    json_str = json.dumps(result, indent=4)
    return json_str

# r = query_youtube('比悲傷更悲傷')
# print(r)