from config import *

from mainController import *
from tools.LastTimeRunnerHolder import LastTimeRunnerHolder as ltrh
from system.streaming.StreamBase import StreamBase
import warnings

from threading import Thread
from time import sleep

from multiprocessing import Process
from time import time
import os


# if __name__ == "__main__":
def mainTask():
    ltrh.setLastTime(datetime.now())
    print('App is running')
    with app.app_context():
        StreamBase.init()
        app.run(host='0.0.0.0', port=5002, debug=False) 
        
fileName = 'tempFile.txt'
if __name__ == '__main__':
    # mainTask()
    while True:
        t1 = Process(target=mainTask, args=())
        t1.start()
        sleep(10)
        nowTime = time()
        print('interval', nowTime - os.path.getmtime(fileName))
        while nowTime - os.path.getmtime(fileName) < 40:                
            sleep(10)
            nowTime = time()
        
        try:
            
            t1.terminate()
            print('terminated')
            t1.kill()
            print('killed')
            t1.join()
        except Exception as e:
            print('kill exception', e)
        try:
            t1.close()
        except Exception as e:
            print('close exception', e)

        
        