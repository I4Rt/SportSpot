from model.data.Room import *
from threading import Thread
from tools.Jsonifyer import *
from tools.FrameGetter import *
from system.kafka.KafkaSingleton import *
from system.SideDataHolder import *

from time import time, sleep

class AgregatedDataSender(Thread, Jsonifyer):
    __interval = 10 * 1
    
    __instance = None
    
    __lastResultativeUpdateTime = None
    
   
    
    
    def __init__(self):
        Thread.__init__(self)
        self.dataHolder = SideDataHolder.getInstance()
        self.sender = KafkaSender.getInstance()
        with open('lastResultativeTime.txt', 'w') as file:
            file.write(str(datetime.now()))
        
    

    def run(self):
        with app.app_context():
            while True:
                print('rooms data is', SideDataHolder.getInstance().rooms)
                sleep(self.__interval)