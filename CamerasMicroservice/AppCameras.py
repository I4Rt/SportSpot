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
        #warnings.simplefilter('ignore')
        with app.app_context():
            StreamBase.init()
            app.run(host='0.0.0.0', port=5002, debug=False) # how to use model with out running app at host?
    while True:
        t1 = Thread(target=mainTask, args=())
        t1.start()
        interval = ltrh.getTimeInterval()
        while interval < 180:
            print(interval)
            sleep(20)
            interval = ltrh.getTimeInterval()
        # must rerun the flask app
        # try:
        #     with app.app_context():
        #         app.stop()
        # except Exception as e:
        #     print('error on stopping app', e)
        
        
            
        
    # cv2.CAP_PROP_OPEN_TIMEOUT_MSEC = 10000
    # cv2.LIBAVFORMAT_INTERRUPT_OPEN_TIMEOUT_MS = 10000
    
        
        