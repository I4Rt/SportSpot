from threading import Thread
from config import *
from model.data.Task import *
from model.data.Room import *
from system.kafka.KafkaSingleton import *

import requests

import time


from tools.FileUtil import *

import cv2
from time import time, sleep

class TaskArchiveRunner(Thread):
    
    __closedStatus = []
    
    def __init__(self, path, interval, taskId) -> None:
        Thread.__init__(self)
        self.path = path
        self.cap = cv2.VideoCapture(path)
        self.interval = interval
        self.taskId = taskId
        
    @classmethod
    def __insertIntoQuery(cls, data):
        cls.__closedStatus = cls.__closedStatus[-99:]
        cls.__closedStatus.append(data)
    
     
    def run(self):
        
        with app.app_context():
        
            success = True
            
            frames = []
            nextTime = 0
            counter = 0
            
            while success:
                success, image = self.cap.read()
                #print('here', success)
                if success and self.cap.get(cv2.CAP_PROP_POS_MSEC) > nextTime:
                    nextTime += self.interval * 1000
                    output = image # cv2.resize(image, (600, 400))
                    #frames.append({'img': output, 'index': initTime + counter})
                    #counter += 1
                    dataToSend = {"taskID": self.taskId,
                                    "agregationMode": 2, # CHECK максимальное
                                    "data": [{
                                                "img": FileUtil.convertImageToBytes(output),
                                                "sectors": [{"points": [], 
                                                            "mode": 2}  # вся комната
                                                        ]
                                            }
                                        ]
                                }
                    print('sending')
                    url = 'http://localhost:4998/appendDataToRoute'
                    myobj = {'SOId': app.config['SPORT_OBJECT_ID'], 'data': dataToSend}
                    data = requests.post(url, json = myobj)
                    print('result',data.text)
                    sleep(5)
                    
            TaskArchiveRunner.__insertIntoQuery(self.taskId)
            