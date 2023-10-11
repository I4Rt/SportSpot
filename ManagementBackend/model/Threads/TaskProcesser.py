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
            # sender = KafkaSender.getInstance()
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
                    try: 
                        frame = next(camData["generator"])
                    except Exception as e:
                        st = f'camera  {camData["camId"]} task {self.task.id} generator error ({e})'+ f' \ntime to task finish is {self.task.end}' + f' now is{datetime.now()}\n\n'
                        with open('tasks.log', 'a') as file:
                            file.write(st)
                        print(f'camera  {camData["camId"]} task {self.task.id} generator error', e, 'time to task finish is', self.task.end, 'now is', datetime.now())
                    if frame is not None:
                        output = frame # cv2.resize(frame, (600, 400))
                        localData = {
                            "img": FileUtil.convertImageToBytes(output),
                            "sectors": [{"points": sector.getPointList(), 
                                         "mode": sector.typeId} 
                                        for sector in camData["sectors"]],
                            # "mode": camData['sectors'][].typeId
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
                    try:
                        url = 'http://localhost:4998/appendDataToRoute'
                        myobj = {'query': f'SO{int(app.config["SPORT_OBJECT_ID"])}_data', 'data': dataToSend}
                        responcedata = requests.post(url, json = myobj, timeout=10)
                        print('inner sending result',responcedata.text)
                    except Exception as e:
                        print('tmisot')
                        continue
                    # print('data to send is ', sendData)
                    print(f'In thread #{get_native_id()}: task id {self.task.id}, analizer sent')
                    # add wait param to kafka reciever  
                sleep(self.task.interval)
            self.task.setStatusDone()
            self.task.save(False)
            print(f'In thread #{get_native_id()}: the process is finished normaly')
            return None     
        