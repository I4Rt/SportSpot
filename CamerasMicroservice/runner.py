import subprocess
import os
from time import time, sleep, ctime

fileName = 'tempFile.txt'

proc = subprocess.Popen(['python', 'AppCameras.py'], shell=True)
sleep(10)
while True:
    sleep(10)
    try:
        nowTime = time()
        print(nowTime - os.path.getmtime(fileName))
        if nowTime - os.path.getmtime(fileName) > 40:
            try:
                proc.terminate()
            except Exception as e:
                print('can not terminate', e)
            print('rerunnung')
            os.remove(fileName)
            proc = subprocess.Popen(['python', 'AppCameras.py'], shell=True)
        sleep(10)
    except Exception as e:
        print('total exception', e)
        break