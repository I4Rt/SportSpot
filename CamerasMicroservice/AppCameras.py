from config import *

from mainController import *
from tools.LastTimeRunnerHolder import LastTimeRunnerHolder as ltrh
from system.streaming.StreamBase import StreamBase
import warnings

from threading import Thread
from time import sleep

if __name__ == "__main__":
    def mainTask():
        ltrh.setLastTime(datetime.now())
        print('App is running')
        with app.app_context():
            StreamBase.init()
            app.run(host='0.0.0.0', port=5002, debug=False) 
            
            
    mainTask()
    # while True:
    #     t1 = Thread(target=mainTask, args=())
    #     t1.start()
    #     interval = ltrh.getTimeInterval()
    #     while interval < 180:
    #         print(interval)
    #         sleep(20)
    #         interval = ltrh.getTimeInterval()

        
        