from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # run Chrome in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--log-level=3')  # 3 = ERROR

def search_youtube(query):
    start_time = time.time()
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.youtube.com/results?search_query={query}+song")
    videos = []
    
    video_elements = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#contents #video-title")))
    for i, video_element in enumerate(video_elements[:10]):
        url = driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{1+i}]/div[1]/div/div[1]/div/h3/a")
        
        title = driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{1+i}]/div[1]/div/div[1]/div/h3/a/yt-formatted-string")      
        
        img_url  = driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{1+i}]/div[1]/ytd-thumbnail/a/yt-image/img")    
        
        author = driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{1+i}]/div[1]/div/div[2]/ytd-channel-name/div/div/yt-formatted-string/a")
        
        author_img = driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{1+i}]/div[1]/div/div[2]/a/yt-img-shadow/img")
        
        video = {}
        video["title"] = title.text
        video["url"] = url.get_attribute("href")
        video["img"] = img_url.get_attribute("src")
        video["author"] = author.text
        video["author_img"] = author_img.get_attribute("src")
        videos.append(video)
        end_time = time.time()
    print(f"程序运行时间：{end_time - start_time}秒")
    return json.dumps({"videos": videos}, indent=4)