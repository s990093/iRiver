from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import json
import time
import re
# 自製
from .options import get_chrome_options
from .options import get_available_port
from music.lib.clear_str import clear_str

def query_music_list(url :str , artist :str) ->json:
    service = Service('chromedriver.exe')
    options = get_chrome_options(port=get_available_port() , is_headLess= True)
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
    for item in driver.find_elements(By.CSS_SELECTOR, '#video-title'):
        url = item.get_attribute('href')
        if url is None:
            continue
        match  = re.search(r'(?<=v=)[^&]+',  url)
        try:
            if match:
                ID = match.group(0)[-11:]
            else:
                ID = re.search(r"shorts\/(\w{11})", url).group(1)
        except Exception as e:
            print(e)
            continue
        title = item.get_attribute('title')
        if title in result:
            continue
        result.append({'music_ID': ID, 'title': clear_str(title= title , artist= artist)})

    driver.close()
    return result

