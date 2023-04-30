import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import re
# 自製
from lib.web_scutter.options import get_chrome_options


def query_summary(query: str) -> str:
    keyword = f'{query}'
    # 設定 Google 圖片搜尋的 URL
    key ='- Wikipedia'
    url = 'https://www.google.com/search?q={}- 維基百科'.format(query)
    # 初始化 Chrome Driver
    service = Service('chromedriver.exe')
    options = get_chrome_options(port = 9224)
    driver = webdriver.Chrome(service=service , options=options) 
    # driver = webdriver.Chrome() 
    # 設定式等待時間
    driver.implicitly_wait(10)
    # 發送請求
    driver.get(url)
    # 取得維基百科 
    wiki_url = None
    wiki_url_elements = driver.find_elements(By.XPATH, '//div[@class="yuRUbf"]/a')[:3]
    for elem in wiki_url_elements:
        url = elem.get_attribute('href')
        if 'wikipedia.org' in url:
                wiki_url = url 
                break

    if wiki_url:
        response = requests.get(wiki_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 进一步解析页面内容，提取所需信息
        intro = soup.select_one('#mw-content-text p').text.strip()
        paras = soup.select('#mw-content-text p')
        # 取前四个非空的段落
        intro_str = ''.join([para.text.strip() for para in paras if para.text.strip()][:4])
        intro = re.sub('\[\d+\]', '', intro_str)
        return str(intro)

    # 如果没有找到維基百科 URL，则返回空字符串
    return '找不到'


# intro = query_summary('康士坦的變化球')
# print(intro)