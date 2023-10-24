from model.data.Room import *
from threading import Thread
from tools.Jsonifyer import *
from tools.FrameGetter import *
from system.kafka.KafkaSingleton import *
from system.SideDataHolder import *


from time import time, sleep

class SideTaskProcessor(Thread, Jsonifyer):
    __trys = 3
    
    __duration = 2
    __interval = 5
    
    __rootTime = 1 * 60
    
    __instance = None
    
   
    
    
    def __init__(self):
        Thread.__init__(self)
        self.dataHolder = SideDataHolder.getInstance()
        
        
    

    def run(self):
        with app.app_context():
            while True:
                try:
                    self.dataHolder.updateRoomList()
                    maxedTime = 5 + 3 * self.__duration + self.__interval
                    # expectedTime = len(self.dataHolder.rooms) * maxedTime
                    
                    localTime = 0
                    beginAllCams = time()
                    for roomId in self.dataHolder.rooms:
                        begin = time()
                        room = Room.getByID(roomId)
                        sectors = room.getSectors()
                        
                        cameras = []
                        
                        for sector in sectors:
                            
                            camId = sector.camId
                            isSet = False
                            for camData in cameras:
                                if camData["camId"] == camId:
                                    camData["sectors"].append(sector)
                                    isSet = True
                                    break 
                                    
                            if not isSet:
                                try:
                                    data = {"camId": camId, 
                                            "generator": FrameGetter.getStream(sector.getCamera().getRoute(), 5 + len (cameras) * self.__duration), 
                                            "sectors": [sector], "camera": sector.getCamera()}
                                    cameras.append(data)
                                except Exception as e:
                                    print('generator create exception', e)
                        
                        dataToSend = {'taskId': f'side_{room.id}',
                                "agregationMode": room.classId, 
                                "data": []}     
                        
                        for camData in cameras:
                            
                            try:
                                
                                frame = next(camData["generator"])
                                
                                if not ( frame is None ):
                                    
                                    output = frame 
                                    
                                    localData = {
                                        "img": FileUtil.convertImageToBytes(output),
                                        "sectors": [{"points": sector.getPointList(), 
                                                    "mode": sector.typeId} 
                                                    for sector in camData["sectors"]]
                                        
                                    }
                                    
                                    dataToSend["data"].append(localData)
                            except Exception as e: 
                                print(type(e), e)
                            
                                
                        if len(dataToSend['data']) > 0:
                            try:
                                
                            
                                url = 'http://localhost:4998/appendDataToRoute'
                                myobj = {'query': f'SO{int(app.config["SPORT_OBJECT_ID"])}_side', 'data': dataToSend}
                                responcedata = requests.post(url, json = myobj, timeout=10)
                                print('inner sending result',responcedata.text)
                            
                                
                               
                            except requests.exceptions.ConnectionError:
                                print('can not send message: connection error')
                            except Exception as e:
                                print( 'inner send error ', type(e) )
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
                except Exception as e:
                    print('side task thread error in loop: ', e)
                            
                        
                            