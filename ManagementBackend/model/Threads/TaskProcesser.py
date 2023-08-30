from model.data.Task import *
from model.data.Room import *
from model.data.Result import *
from threading import Thread, get_native_id
from model.QueueTaskHolder import *

from system.streaming.StreamInterface import StreamInterface

from tools.Jsonifyer import Jsonifyer
from datetime import datetime
from time import sleep
import copy
from cv2 import imshow

class TaskProcessor(Thread, Jsonifyer):
    __trys = 3
    
    def __init__(self, task:Task):
        Thread.__init__(self)
        self.task = copy.deepcopy(task)
        
    def run(self):
        
        with app.app_context():
            self.task.setStatusInProgress()
            self.task.save(False)
            tzDateStr = str(self.task.end)
            date = datetime.strptime(tzDateStr[:-6], '%Y-%m-%d %H:%M:%S')
            date += timedelta(hours=int(tzDateStr[-6:-3]) - 7) #cur tz
            duration = date - datetime.now()
            duration = int(duration.total_seconds()) - self.task.interval
            if duration <= 0:
                raise Exception(f'In thread #{get_native_id()}: time is out, duration < 0')
            
            cams = Room.getByID(self.task.roomId).getCameras() # incapsulate it
            if len(cams) != 0:
                iterators = []
                for cam in cams:
                    connectCounter = 0
                    while connectCounter < self.__trys:
                        try:
                            
                            framesIter = StreamInterface.getStream(cam, duration)
                            if framesIter is not None:
                                iterators.append(framesIter)
                            break
                        except:
                            connectCounter += 1
                if len(iterators) == 0:
                    self.task.setStatusDone()
                    self.task.save(False)
                    raise Exception(f'In thread #{get_native_id()}: during the work got three errors')
                while date > datetime.now():    
                    for iter in iterators:
                        frame = next(iter)
                        # print('frame:', frame)
                        # if frame is not None:
                        #     analize frame
                        print(f'In thread #{get_native_id()}: task id {self.task.id}, analizer sent')
                        # add wait param to kafka reciever
                        sleep(self.task.interval)
            
                print('loop finished')
                self.task.setStatusDone()
                self.task.save(False)
                print(f'In thread #{get_native_id()}: the process is finished normaly')
                return None
            else:
                self.task.setStatusDone()
                self.task.save(False)
                raise Exception(f'In thread #{get_native_id()}: no cameras')
        