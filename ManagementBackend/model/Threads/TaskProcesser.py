from model.data.Task import *
from model.data.Room import *
from model.data.Result import *
from threading import Thread, get_native_id
from model.QueueTaskHolder import *

from system.kafka.KafkaSingleton import KafkaSender
from tools.FileUtil import *

from system.streaming.StreamInterface import StreamInterface

from tools.Jsonifyer import Jsonifyer
from datetime import datetime
from time import sleep
import copy
from cv2 import imshow

from tools.FrameGetter import *

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
                self.task.setStatusDone()
                self.task.save(False)
                raise Exception(f'In thread #{get_native_id()}: time is out, duration < 0')
            room = Room.getByID(self.task.roomId)
            sectors = room.getSectors()
            cameras = []
            for sector in sectors:
                camId = sector.camId
                isSet = False
                for camData in cameras:
                    if camData["camId"] == camId:
                        camData["sectors"].append(sector)
                        isSet = True
                if not isSet:
                    data = {"camId": camId, "generator": None, "sectors": [sector], "camera": sector.getCamera()}
                    cameras.append(data)
            
            for camData in cameras:
                connectCounter = 0
                while connectCounter < self.__trys:
                    print('here')
                    try:
                        framesIter = FrameGetter.getStream(camData["camera"].getRoute(), duration)
                    except Exception as e:
                        print('generator create exception', e)
                        connectCounter += 1
                        continue
                    if framesIter is not None:
                        camData["generator"]  = framesIter
                        break
                    else:
                        connectCounter += 1
                print(connectCounter)
                if connectCounter == self.__trys:
                    cameras.remove(camData)
                    
            if len(cameras) == 0:
                    self.task.setStatusDone()
                    self.task.save(False)
                    raise Exception(f'In thread #{get_native_id()}: no cameras or unable to connect to them')
            
            
            while date > datetime.now():   
                dataToSend = {"taskId": self.task.id,
                              "agregationMode": room.classId,
                              "data": []}
                for camData in cameras:
                    try: 
                        frame = next(camData["generator"])
                    except Exception as e:
                        st = f'camera  {camData["camId"]} task {self.task.id} generator error ({e})'+ f' \ntime to task finish is {self.task.end}' + f' now is{datetime.now()}\n\n'
                        with open('tasks.log', 'a') as file:
                            file.write(st)
                        print(f'camera  {camData["camId"]} task {self.task.id} generator error', e, 'time to task finish is', self.task.end, 'now is', datetime.now())
                        continue
                    if frame is not None:
                        output = frame
                        localData = {
                            "img": FileUtil.convertImageToBytes(output),
                            "sectors": [{"points": sector.getPointList(), 
                                         "mode": sector.typeId} 
                                        for sector in camData["sectors"]],
                        }
                        
                        dataToSend["data"].append(localData)
                        st = f'ok\n\n'
                        with open('tasks.log', 'a') as file:
                            file.write(st)
                    else:
                        st = f'camera  {camData["camId"]} task {self.task.id} generator NONE'+ f' \ntime to task finish is {self.task.end}' + f' now is{datetime.now()}\n\n'
                        with open('tasks.log', 'a') as file:
                            file.write(st)
                if len(dataToSend["data"]) > 0:
                    
                    with open('senderData.json', 'w') as file:
                        file.write(json.dumps(dataToSend))
                    try:
                        url = 'http://localhost:4998/appendDataToRoute'
                        myobj = {'query': f'SO{int(app.config["SPORT_OBJECT_ID"])}_data', 'data': dataToSend}
                        responcedata = requests.post(url, json = myobj, timeout=10)
                        
                    except Exception as e:
                        print('tmisot')
                        continue
                    print(f'In thread #{get_native_id()}: task id {self.task.id}, analizer sent')
                    
                sleep(self.task.interval)
            self.task.setStatusDone()
            self.task.save(False)
            print(f'In thread #{get_native_id()}: the process is finished normaly')
            return None     
        