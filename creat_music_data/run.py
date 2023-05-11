import subprocess
import time
import keyboard

while True:
    process = subprocess.Popen(
        ['python', 'main.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
        print(
            f'main.py failed with exit code {process.returncode}, restarting in 10 seconds...')
        time.sleep(10)
