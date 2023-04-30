from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_chrome_options():
    options = Options()
    options.add_argument("--headless")  # run Chrome in headless mode
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
    options.add_argument('--start-maximized')  # start browser maximized
    # set remote debugging port to 9222
    options.add_argument("--remote-debugging-port=9222")

    return options
