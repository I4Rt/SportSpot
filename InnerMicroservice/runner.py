import subprocess
import os
from time import time, sleep, ctime
from datetime import datetime
import shlex

from multiprocessing import Process

fileName = 'tempFile.txt'

proc = subprocess.Popen(['python', 'AppInner.py'])
# for linux
# proc = subprocess.Popen(shlex.split('python AppInner.py'))
sleep(10)
while True:

    sleep(10)
    try:
        nowTime = time()
        print(nowTime - os.path.getmtime(fileName))
        if nowTime - os.path.getmtime(fileName) > 120:
            try:
                proc.terminate()
            except Exception as e:
                print('can not terminate', e)
            print(f'{datetime.now()} rerunning\n')
            os.remove(fileName)
            # os.system('python close.py')
            log = open('log.txt', 'a')
            log.write(f'{datetime.now()} rerunning\n')
            log.close()
            proc = subprocess.Popen(['python', 'AppInner.py'], shell=True)
        sleep(10)
    except Exception as e:
        print('total exception', e)
        break