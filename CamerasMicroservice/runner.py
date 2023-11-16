import subprocess
import os
from time import time, sleep, ctime

from multiprocessing import Process
from datetime import datetime
import signal

FILE_NAME = 'tempFile.txt'
TIME_LIMIT = 1 * 60

proc = subprocess.Popen(['python', 'AppCameras.py'], shell=True)
runTime = time()
sleep(10)
while True:
    sleep(10)
    
    try:
        nowTime = time()
        print('time params', nowTime - os.path.getmtime(FILE_NAME) > 120, nowTime - runTime > TIME_LIMIT, nowTime - runTime)
        if nowTime - os.path.getmtime(FILE_NAME) > 120 or nowTime - runTime > TIME_LIMIT:
            try:
                os.kill(proc.pid, signal.SIGTERM)
            except Exception as e:
                print('can not terminate', e)
            print('rerunnung')
            os.remove(FILE_NAME)
            os.system('python close.py')           #???
            log = open('log.txt', 'a')          
            log.write('rerunning '+ str(datetime.now()))
            log.close()
            
            proc = subprocess.Popen(['python', 'AppCameras.py'], shell=True)
            runTime = time()
        sleep(10)
    except Exception as e:
        print('total exception', e)
        break