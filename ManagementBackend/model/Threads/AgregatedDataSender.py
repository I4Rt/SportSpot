from model.data.Room import *
from model.data.Task import *

from threading import Thread
from tools.Jsonifyer import *
from tools.FrameGetter import *
from system.kafka.KafkaSingleton import *
from system.SideDataHolder import *

from datetime import timedelta


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
                # 2023-10-03 16:48:21.011302
                # print('rooms data is', SideDataHolder.getInstance().rooms)
                sleep(self.__interval)
                
                #select data
                date = datetime.now()
                try:
                    with open('lastResultativeTime.txt', 'r') as file:
                        lastDateStr = file.read()
                        date = datetime.strptime(lastDateStr, '%Y-%m-%d %H:%M:%S.%f')
                except:
                    with open('lastResultativeTime.txt', 'w') as file:
                        file.write(str(date))
                        continue
                
                interval = datetime.now() - date
                minutes = interval.total_seconds() // 60
                tasks = Task.getLastInInterval(30) #Task.getLastInInterval(minutes)
                rooms = Room.getAll()
                unmathcedRooms = [room.id for room in rooms]
                
                result = {}
                for task in tasks:
                    unmathcedRooms.remove(task.roomId)
                    result[str(task.roomId)] = {'real':task.getCount(), 'plan':task.targetCount}
                    
                for roomId in unmathcedRooms:
                    try:
                        result[str(roomId)] = {'real':SideDataHolder.getInstance().rooms[roomId], 'plan': 0}
                    except:
                        pass
                
                
                # sending
                dateToAgregate = datetime.now()
                
                hour = dateToAgregate.hour
                minutes = dateToAgregate.minute
                if minutes < 30: 
                    minutes = '00'
                else:
                    minutes = '30'
                    
                sendDate = str(dateToAgregate.date())
                hour = "0" + str(hour - 1) if hour < 10 else str(hour)
                
                timeInterval = f'{hour}-{minutes}-00'
                
                resultToSend= {
                    sendDate: {timeInterval: result}
                }

                print(resultToSend)
                try:
                    url = 'http://localhost:4999/management/appendData'
                    myobj = {'SOId': app.config['SPORT_OBJECT_ID'], 'data': resultToSend}
                    data = requests.post(url, json = myobj)
                    # print(data)
                except:
                    print ('connection error')
                