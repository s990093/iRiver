import subprocess
import keyboard
import time
import os

max_size = 100 * 1024 * 1024 * 1024  # 100 GB

while True:
    process = subprocess.Popen(
        ['python', 'main.py'], stdout=None, stderr=subprocess.PIPE)

    while process.poll() is None:
        if keyboard.is_pressed('ctrl+c'):
            process.terminate()
            print('Process terminated by user')
            exit()
        time.sleep(0.1)

    if process.returncode == 0:
        print('main.py completed successfully')
        break
    else:
        print(f'main.py failed with exit code {process.returncode}')

        # Check downloaded file size
        downloaded_size = os.path.getsize('C:\Users\s9900\OneDrive\桌面\django\myproject\media')

        if downloaded_size >= max_size:
            print('Download size limit exceeded. Stopping download.')
            break

        print('Restarting in 10 seconds...')
        time.sleep(10)
