from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from typing import List
# 自製
from .options import get_chrome_options
from .options import get_available_port

def query_artist_iocn_src(query: str) -> str:
    # 設定搜尋關鍵字和搜尋數量
    keyword = f'{query}照片'
    # 設定 Google 圖片搜尋的 URL
    url = 'https://www.google.com/search?q={}&source=lnms&tbm=isch'.format(keyword)
    # 初始化 Chrome Driver
    service = Service('chromedriver.exe')
    options = get_chrome_options(port= get_available_port() , is_headLess= True)
    driver = webdriver.Chrome(service= service , options=options)
    # 設定式等待時間
    driver.implicitly_wait(10)
    # 發送請求
    driver.get(url)
    # 取得圖片 URL
    image_urls = []
    img_tags = driver.find_elements(By.XPATH, '//img[@class="rg_i Q4LuWd"]')
    for img_tag in img_tags:
        image_urls.append(img_tag.get_attribute('src'))

    return image_urls[0] 
