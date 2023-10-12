from model.data.Room import *
from threading import Thread
from tools.Jsonifyer import *
from tools.FrameGetter import *
from system.kafka.KafkaSingleton import *
from system.SideDataHolder import *

from time import time, sleep

class SideTaskProcessor(Thread, Jsonifyer):
    __trys = 3
    
    __duration = 1
    __interval = 15
    
    __rootTime = 1 * 60
    
    __instance = None
    
   
    
    
    def __init__(self):
        Thread.__init__(self)
        self.dataHolder = SideDataHolder.getInstance()
        # self.sender = KafkaSender.getInstance()
        
    

    def run(self):
        with app.app_context():
            while True:
                maxedTime = 5 + 3 * self.__duration + self.__interval
                self.dataHolder.updateRoomList()
                expectedTime = len(self.dataHolder.rooms) * maxedTime
                # needSleep = expectedTime < self.__rootTime
                localTime = 0
                beginAllCams = time()
                for roomId in self.dataHolder.rooms:
                    begin = time()
                    room = Room.getByID(roomId)
                    sectors = room.getSectors()
                    # print(f"sectprs {len(sectors)}")
                    cameras = []
                    b1 = time()
                    for sector in sectors:
                        # print(sector)
                        camId = sector.camId
                        isSet = False
                        for camData in cameras:
                            if camData["camId"] == camId:
                                camData["sectors"].append(sector)
                                isSet = True
                                break # TODO: check it
                                
                        if not isSet:
                            data = {"camId": camId, 
                                    "generator": FrameGetter.getStream(sector.getCamera().getRoute(), 5 + len (cameras) * self.__duration), 
                                    "sectors": [sector], "camera": sector.getCamera()}
                            cameras.append(data)
                       
                    dataToSend = {'taskId': f'side_{room.id}',
                              "agregationMode": room.classId, # CHECK
                              "data": []}     
                    # print('here', len(cameras))
                    # print('agregation part 1 t', time() - b1, 'camLen', len(cameras))
                    b2 = time()
                    for camData in cameras:
                        # print(camData)
                        try:
                            b = time()
                            frame = next(camData["generator"])
                            # print(camData['camera'].getRoute(), 'getting t', time() - b)
                            # print(camData['camera'].getRoute(), len(str(frame)))
                            if not ( frame is None ):
                                
                                output = frame # cv2.resize(frame, (600, 400))
                                
                                localData = {
                                    "img": FileUtil.convertImageToBytes(output),
                                    "sectors": [{"points": sector.getPointList(), 
                                                "mode": sector.typeId} 
                                                for sector in camData["sectors"]]
                                    
                                }
                                # print('mode is',  sector.typeId)
                                dataToSend["data"].append(localData)
                        except Exception as e: 
                            print(type(e), e)
                        # print('agregation part 2 t', time() - b2)
                            
                    if len(dataToSend['data']) > 0:
                        try:
                            b = time()
                            # print('side data to send', dataToSend['taskId'])
                            try:
                                url = 'http://localhost:4998/appendDataToRoute'
                                myobj = {'query': f'SO{int(app.config["SPORT_OBJECT_ID"])}_local', 'data': dataToSend}
                                responcedata = requests.post(url, json = myobj, timeout=10)
                                print('inner sending result',responcedata.text)
                            except Exception as e:
                                print('tmisot')
                                continue
                            
                            #sendData = self.sender.sendMessage(json.dumps(dataToSend))
                            
                            # with open('errorSending.txt', 'w') as file:
                            #     file.write(json.dumps(dataToSend))
                            # print(camData['camera'].getRoute(), 'sending t', time() - b)
                            # print('here2 message is ', sendData)
                            # print('side analize', sendData)
                        except requests.exceptions.ConnectionError:
                            print('can not send message: connection error')
                        except Exception as e:
                            print( 'error ', type(e) )
                    end = time()
                    print('time to process', end - begin)
                    maxedTime = max(maxedTime, end - begin)
                    rest = 5 + len(cameras) * self.__duration + self.__interval - (end - begin) 
                    print('sleep before the next camera', rest)
                    sleep(rest if rest > 0 else 0)
                    localTime += maxedTime
                    
                if time() - beginAllCams < self.__rootTime :
                    print('sleep before all camera loop', self.__rootTime - (time() - beginAllCams) )
                    sleep(self.__rootTime - (time() - beginAllCams))
                        
                    
                        