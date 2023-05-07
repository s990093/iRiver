"""參數set"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import socket

def get_chrome_options(port=9222 , is_headLess = False):
    '''爬蟲參數'''
    options = Options()
    if is_headLess:
        options.add_argument("--headless")  # run Chrome in headless mode
        
   
    options.add_argument("--detach")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--log-level=3')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-background-timer-throttling')
    options.add_argument('--disable-background-networking')
    options.add_argument('--disable-component-extensions-with-background-pages')
    options.add_argument('--disable-ipc-flooding-protection')
    options.add_argument('--disable-renderer-backgrounding')
    options.add_argument('--enable-features=NetworkServiceInProcess')
    options.add_argument('--force-color-profile=srgb')
    options.add_argument('--hide-scrollbars')
    options.add_argument('--metrics-recording-only')
    options.add_argument('--mute-audio')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--no-first-run')
    options.add_argument('--safebrowsing-disable-auto-update')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-gpu')
    options.add_argument(f"--remote-debugging-port={port}")
    options.add_argument("--start-minimized")
    options.add_argument('--blink-settings=imagesEnabled=false')
    return options

def get_available_port():
    '''自動分配port'''
    # 使用IPv4和TCP协议创建套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定本地IP和端口0，表示使用系统分配的可用端口
    sock.bind(('0.0.0.0', 0))
    # 获取分配的端口号
    port = sock.getsockname()[1]
    # 关闭套接字
    sock.close()
    # 返回端口号
    return port