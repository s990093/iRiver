from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urljoin
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import time
import re
# 自製
from .options import get_chrome_options
from .options import get_available_port


def query_music_list(url :str) ->json:
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
