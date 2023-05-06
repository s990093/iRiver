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
    options.add_argument("--disable-gpu")  # disable GPU
    options.add_argument("--no-sandbox")  # disable sandbox mode
    options.add_argument("--disable-dev-shm-usage")  # disable /dev/shm usage
    options.add_argument('--log-level=3')  # set log level to ERROR
    options.add_argument('--disable-extensions')  # disable extensions
    # disable timer throttling
    options.add_argument('--disable-background-timer-throttling')
    # disable background networking
    options.add_argument('--disable-background-networking')
    # disable certain features
    options.add_argument(
        '--disable-features=NetworkService,RendererCodeIntegrity')
    # disable site isolation trials
    options.add_argument('--disable-site-isolation-trials')
    options.add_argument('--disable-breakpad')  # disable breakpad
    # disable component extensions with background pages
    options.add_argument(
        '--disable-component-extensions-with-background-pages')
    # disable IPC flooding protection
    options.add_argument('--disable-ipc-flooding-protection')
    # disable renderer backgrounding
    options.add_argument('--disable-renderer-backgrounding')
    # enable network service in process
    options.add_argument('--enable-features=NetworkServiceInProcess')
    # set color profile to sRGB
    options.add_argument('--force-color-profile=srgb')
    options.add_argument('--hide-scrollbars')  # hide scrollbars
    options.add_argument('--metrics-recording-only')  # only record metrics
    options.add_argument('--mute-audio')  # mute audio
    # don't perform default browser check
    options.add_argument('--no-default-browser-check')
    options.add_argument('--no-first-run')  # don't perform first run setup
    # disable safe browsing auto-update
    options.add_argument('--safebrowsing-disable-auto-update')
    options.add_argument('--disable-popup-blocking') # 禁止弹出窗口的阻止
    # set remote debugging port
    options.add_argument(f"--remote-debugging-port={port}")
    options.add_argument('--disable-dev-shm-usage')
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