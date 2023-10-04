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
            sender = KafkaSender.getInstance()
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
            # print(f"sectprs {len(sectors)}")
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
            
            # print(cameras)
            for camData in cameras:
                connectCounter = 0
                while connectCounter < self.__trys:
                    print('here')
                
                    framesIter = FrameGetter.getStream(camData["camera"].getRoute(), duration)
                    # print(framesIter)
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
            # print(cameras)
            
            while date > datetime.now():   
                dataToSend = {"taskId": self.task.id,
                              "agregationMode": room.classId, # CHECK
                              "data": []}
                for camData in cameras:
                    frame = next(camData["generator"])
                    if frame is not None:
                        output = frame # cv2.resize(frame, (600, 400))
                        localData = {
                            "img": FileUtil.convertImageToBytes(output),
                            "sectors": [{"points": sector.getPointList(), 
                                         "mode": sector.typeId} 
                                        for sector in camData["sectors"]],
                            "mode": camData['sectors'].typeId
                        }
                        
                        dataToSend["data"].append(localData)
                if len(dataToSend["data"]) > 0:
                    # print("sending:")
                    #
                    # for data in dataToSend["data"]:
                    #     print(f'img: {data["img"][:10]}')
                    #     for sec in data["sectors"]:
                    #         print(f'    points: {sec["points"]}')
                    #         print(f'    mode: {sec["mode"]}')
                    #         print()
                    #
                    with open('senderData.json', 'w') as file:
                        file.write(json.dumps(dataToSend))
                    sendData = sender.sendMessage(json.dumps(dataToSend))
                    print(sendData)
                    print(f'In thread #{get_native_id()}: task id {self.task.id}, analizer sent')
                    # add wait param to kafka reciever  
                sleep(self.task.interval)
            self.task.setStatusDone()
            self.task.save(False)
            print(f'In thread #{get_native_id()}: the process is finished normaly')
            return None     
        