from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

import time
import re

from lib.web_scutter.options import get_chrome_options, get_available_port
from lib.clear_str import clear_str


def get_hot_song_info():
    options = get_chrome_options(port=get_available_port(), is_headLess=True)
    options.chrome_executable_path = "C:/Users/Lenovo/Desktop/python/lib/web_scutter/chromedriver.exe"
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.youtube.com/feed/trending")
    driver.maximize_window()
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    hot = driver.find_elements(
        By.XPATH, "//*[@id=\"tabsContent\"]/tp-yt-paper-tab[2]")
    for link in hot:
        link.click()
        break  # 如果找到符合條件的元素，跳出迴圈

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    # 設定滾動的距離和暫停的時間間隔
    scroll_distance = 400  # 每次滾動的距離（像素）
    pause_time = 0.05  # 每次滾動後的暫停時間（秒）

    # 獲取頁面高度
    page_height = driver.execute_script(
        "return document.documentElement.scrollHeight")

    # 開始滾動
    current_position = 0
    while current_position < page_height:
        # 模擬滾動動作
        driver.execute_script(f"window.scrollTo(0, {current_position});")

        # 等待一段時間以模擬滑動速度
        time.sleep(pause_time)

        # 更新當前位置
        current_position += scroll_distance

        # 更新頁面高度
        page_height = driver.execute_script(
            "return document.documentElement.scrollHeight")

    # 在此處繼續處理後續操作

    hot_music = driver.find_elements(By.XPATH, "//a[@id=\"video-title\"]")
    hot_music_artist = driver.find_elements(
        By.XPATH, '//a[@class="yt-simple-endpoint style-scope yt-formatted-string"]')
    hot_music_pic = driver.find_elements(
        By.XPATH, "//a[@id=\"thumbnail\"]/yt-image/img")
    music_info = []
    for music in range(len(hot_music)):
        try:
            if hot_music[music].get_attribute('id') != "video-title":
                break
            match = re.search(
                r'(?<=v=)[^&]+', hot_music[music].get_attribute('href'))
            if match:
                ID = match.group(0)[-11:]
            else:
                ID = re.search(
                    r"shorts\/(\w{11})", hot_music[music].get_attribute('href')).group(1)
            video = {}
            video['title'] = hot_music[music].get_attribute('title')
            video['url'] = hot_music[music].get_attribute('href')
            video['img_url'] = hot_music_pic[music].get_attribute('src')
            video['artist'] = hot_music_artist[music*2].text
            video["music_ID"] = ID
            video['artist_url'] = hot_music_artist[music *
                                                   2].get_attribute('href')
            music_info.append(video)
            # for key, music_menu in video.items():
            #     print(key, music_menu)
            # print()
        except StaleElementReferenceException:
            break
    driver.close()
    return music_info
