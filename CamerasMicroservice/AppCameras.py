from config import *

from mainController import *
from tools.LastTimeRunnerHolder import LastTimeRunnerHolder as ltrh
from system.streaming.PermanentStreamer import PermanentStreamer
import warnings

from threading import Thread
from time import sleep

from multiprocessing import Process
from time import time
import os
# if __name__ == "__main__":
def mainTask(time, timeLimit):
    ltrh.setLastTime(datetime.now())
    print('App is running')
    with app.app_context():
        PermanentStreamer.init(time, timeLimit)
        app.run(host='0.0.0.0', port=5002, debug=False) 
        
FILE_NAME = 'tempFile.txt'
TIME_LIMIT = 1 * 60 # 4 hours

if __name__ == '__main__':
    # mainTask(time(), TIME_LIMIT)
    runTime = time()
    t1 = Process(target=mainTask, args=(runTime, TIME_LIMIT))
    t1.start()
    while time() - runTime < TIME_LIMIT - 10:
        sleep(5)
    t1.terminate()
    t1.join()
    print('terminated inside')
        
        
    #     while nowTime - os.path.getmtime(FILE_NAME) < 120:        
    #         print('interval', nowTime - os.path.getmtime(FILE_NAME))        
    #         sleep(10)
    #         nowTime = time()
    #         if nowTime - runTime > TIME_LIMIT: 
    #             break
        
    #     try:
    #         t1.terminate()
    #         print('terminated')
    #         t1.join(10)
    #         print('joined')
    #         t1.kill()
    #         print('killed')
            
    #     except Exception as e:
    #         print('kill exception', e)
    #     try:
    #         t1.close()
    #     except Exception as e:
    #         print('close exception', e)

        
        