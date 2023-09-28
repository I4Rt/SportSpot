from threading import Thread
from config import *
from model.data.Task import *
from model.data.Room import *
from system.kafka.KafkaSingleton import *

from tools.FileUtil import *

import cv2
from time import time

class TaskArchiveRunner(Thread):
    
    __closedStatus = []
    
    def __init__(self, path, interval, task) -> None:
        Thread.__init__(self)
        self.path = path
        self.cap = cv2.VideoCapture(path)
        self.interval = interval
        self.taskId = task
        
    @classmethod
    def __insertIntoQuery(cls, data):
        cls.__closedStatus = cls.__closedStatus[-99:]
        cls.__closedStatus.append(data)
    
     
    def run(self):
        initTime = time.time()
        with app.app_context():
        
            success = True
            
            frames = []
            nextTime = 0
            counter = 0
            
            while success:
                if self.cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC) > nextTime:
                    nextTime += self.interval * 1000
                    success, image = self.read()
                    output = cv2.resize(image, (600, 400))
                    #frames.append({'img': output, 'index': initTime + counter})
                    #counter += 1
                    dataToSend = {"taskID": self.task.id,
                                    "agregationMode": 2, # CHECK максимальное
                                    "data": [{
                                                "img": FileUtil.convertImageToBytes(output),
                                                "sectors": [{"points": [], 
                                                            "mode": 2}  # вся комната
                                                        ]
                                            }
                                        ]
                                }
                    sendData = sender.sendMessage(json.dumps(dataToSend))
                    
            
            