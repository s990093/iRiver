from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urljoin
import time
import json
import re
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import StaleElementReferenceException
from googlesearch import search
import requests
import re
from bs4 import BeautifulSoup
from .options import get_chrome_options


def search_youtube(query : str):
    service = Service('chromedriver.exe')
    options = get_chrome_options()
    driver = webdriver.Chrome(service = service, options=options) 
    start_time = time.time()
    driver.get(f"https://www.youtube.com/results?search_query={query}&sp=EgIQAQ%253D%253D&t=0s-7m")
    videos = []
    video_elements = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#contents #video-title")))
    for i, video_element in enumerate(video_elements[:10]):
        try:
            url = driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{1+i}]/div[1]/div/div[1]/div/h3/a")
            title = driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{1+i}]/div[1]/div/div[1]/div/h3/a/yt-formatted-string")                  
            artist = driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{1+i}]/div[1]/div/div[2]/ytd-channel-name/div/div/yt-formatted-string/a")     

            artist_img_url = driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[2]/a/yt-img-shadow/img")
            match  = re.search(r'(?<=v=)[^&]+',  url.get_attribute('href'))
            if match:
                ID = match.group(0)[-11:]
            else:
                ID = re.search(r"shorts\/(\w{11})", url.get_attribute('href')).group(1)
            video = {}
            video["title"] = title=title.text
            video["music_ID"] = ID
            video["url"] = url.get_attribute("href")
            video["img_url"] = f'https://i.ytimg.com/vi/{ID}/hqdefault.jpg?'
            video["artist"] = artist.text.replace('/', '').replace(' ', '')
            video["artist_url"] = artist.get_attribute("href")
            video["artist_img_url"] = artist_img_url.get_attribute("src")
            videos.append(video)
        except NoSuchElementException:
            pass
        end_time = time.time()
    print(f"程序运行时间：{end_time - start_time}秒")
    driver.close()
    return json.dumps({"videos": videos}, indent=4)

# 列出 歌手全部的歌曲
def search_musiclist(url):
    service = Service('chromedriver.exe')
    options = get_chrome_options()
    driver = webdriver.Chrome(service = service, options=options) 
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    music_video = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@id='title']")))
    music_video.click()

    # 先讓頁面滾動到最底部，直到所有的歌曲都載入
    while True:
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break

    # 獲取所有歌曲的 ID 和標題
    result = []
    for item in driver.find_elements(By.CSS_SELECTOR, 'a#video-title'):
        url = item.get_attribute('href')
        match  = re.search(r'(?<=v=)[^&]+',  url)
        if match:
            ID = match.group(0)[-11:]
        else:
            ID = re.search(r"shorts\/(\w{11})", url).group(1)
        print(ID)
        title = item.text
        if title in result:
            continue
        result.append(ID)
        result.append(title)
    driver.close()
    return result


def search_artist_summary(query :str) ->str: 
    # 设置搜索关键词
    query = f"維基百科 {query}"

    # 使用Google搜索API搜索
    search_results = list(search(query , num_results=1))
    # print(search_results)

    # 找到维基百科页面的链接
    wiki_url = None
    for result in search_results:
        if 'wikipedia.org' in result: # type: ignore
            wiki_url = result
            break

    # 如果找到了维基百科页面的链接，则请求该页面的内容
    if wiki_url:
        response = requests.get(wiki_url) # type: ignore
        soup = BeautifulSoup(response.text, 'html.parser')
        # 进一步解析页面内容，提取所需信息
        intro = soup.select_one('#mw-content-text p').text.strip()
        paras = soup.select('#mw-content-text p')
        # 取前四个非空的段落
        intro_str = ''.join([para.text.strip() for para in paras if para.text.strip()][:4])
        intro = re.sub('\[\d+\]', '', intro_str)
    return intro 

def  search_artist_img(query :str) ->str:
    # 設定搜尋關鍵字和搜尋數量
    keyword = f'{query}團照'
    # 設定 Google 圖片搜尋的 URL
    url = 'https://www.google.com/search?q={}&source=lnms&tbm=isch'.format(keyword)
    # 初始化 Chrome Driver
    options = get_chrome_options()
    driver = webdriver.Chrome( options=options)
    # 設定式等待時間
    driver.implicitly_wait(10)
    # 發送請求
    driver.get(url)
    # 取得圖片 URL
    image_urls = []
    url = driver.find_element(
                    By.XPATH, 
        f" /html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]/div[1]/img")
            

    return  url.get_attribute('src')
