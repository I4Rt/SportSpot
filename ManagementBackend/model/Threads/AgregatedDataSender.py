from model.data.Room import *
from model.data.Task import *

from threading import Thread
from tools.Jsonifyer import *
from tools.FrameGetter import *
from system.kafka.KafkaSingleton import *
from system.SideDataHolder import *

from datetime import timedelta


from time import time, sleep, altzone, timezone, localtime

class AgregatedDataSender(Thread, Jsonifyer):
    __interval = 10 * 1
    
    __instance = None
    
    __lastResultativeUpdateTime = None
    
   
    
    
    def __init__(self):
        Thread.__init__(self)
        self.dataHolder = SideDataHolder.getInstance()
        #self.sender = KafkaSender.getInstance()
        
        
        with open('lastResultativeTime.txt', 'w') as file:
            file.write(str(datetime.now()))
        
    
    
                
    
    
    def run(self):
        with app.app_context():
            SideDataHolder.getInstance().getSavedChangedTasks()
            offset = timezone if (localtime().tm_isdst == 0) else altzone
            tz = int(offset / 60 / 60 * -1)
            print('timezone is', tz)
                            
                            
            interval = 1 # in minutes
            lastTime = datetime.now()
            lastTime-= timedelta(minutes= lastTime.minute - (lastTime.minute // interval) * interval)
            
            timeToRun = lastTime + timedelta(minutes= interval // 2)
              
            while True:
                # 2023-10-03 16:48:21.011302
                # print('rooms data is', SideDataHolder.getInstance().rooms)
                
                        
                        
                
                sleep(1 * 60)
                nt = datetime.now()
                if nt >= timeToRun:
                    
                    SideDataHolder.getInstance().updateRoomList()
                
                    print('data holder is', SideDataHolder.getInstance().rooms)
                    #select data
                    date = timeToRun
                    try:
                        with open('lastResultativeTime.txt', 'r') as file:
                            lastDateStr = file.read()
                            date = datetime.strptime(lastDateStr, '%Y-%m-%d %H:%M:%S.%f')
                    except:
                        with open('lastResultativeTime.txt', 'w') as file:
                            file.write(str(date))
                            continue
                    
                    # interval = datetime.now() - date     # to get lost time 
                    # minutes = interval.total_seconds() // 60
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
                    
                    changedData = SideDataHolder.getInstance().changedTasks.copy()
                    setData = []
                    for task in tasks:
                        for _ in changedData:
                            if _ == task.id:
                                changedData.remove(changedData)
                                setData.append(_)
                                #SideDataHolder.getInstance().removeTask(_)
                                
                    
                    
                            
                            
                    
                    # sending
                    dateToAgregate = timeToRun
                    
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
                        sendDate: {timeInterval: result},
                    }
                    print(changedData)
                    for taskId in changedData:
                        
                        task = Task.getById(taskId)
                        #SideDataHolder.getInstance().removeTask(taskId)
                        begining = task.begin
                        ending = task.end
                        
                        curDate = begining
                        
                        while curDate < ending:
                            print(curDate)
                            noTZDate = datetime.strptime(str(curDate)[:-6], '%Y-%m-%d %H:%M:%S')
                            #noTZDate -= timedelta(hours= tz)
                            print(noTZDate)
                            
                            mins = noTZDate.minute
                            if mins >= 30:
                                print('diff is ', mins - 30)
                                noTZDate -= timedelta(minutes = (mins - 30))
                            else:
                                print('diff is ', mins)
                                noTZDate -= timedelta(minutes = mins)
                            print('minute set after is ', noTZDate)
                            localDate = noTZDate.date()
                            localTime = noTZDate.time()
                            
                            print('local date is', str(localDate))
                            print('local time is', str(localTime))
                            dateStr = str(localDate)
                            timeStr = str(localTime).replace(':', '-')
                            try:
                                resultToSend[dateStr][timeStr][task.roomId] = {'real':task.getCount(), 'plan':task.targetCount}
                            except:
                                try:
                                    resultToSend[dateStr][timeStr] = {task.roomId: {'real':task.getCount(), 'plan':task.targetCount}}
                                except:
                                    resultToSend[dateStr] = {timeStr: {task.roomId: {'real':task.getCount(), 'plan':task.targetCount}}}
                            #print('after Append data is ', resultToSend)
                            curDate += timedelta(minutes=30)
                        setData.append(taskId)
                        
                    print(resultToSend)
                    try:
                        url = 'http://localhost:4999/management/appendData'
                        myobj = {'SOId': app.config['SPORT_OBJECT_ID'], 'data': resultToSend, 'rooms': [room.getParamsList() for room in rooms]}
                        data = requests.post(url, json = myobj)
                        print(data.status_code, data.json)
                        for taskId in setData:
                            SideDataHolder.getInstance().removeTask(taskId)
                            SideDataHolder.getInstance().saveChangedTasks()
                    except:
                        print ('connection error')
                    if nt.minute == 30 or nt.minute == 0:
                        SideDataHolder.resetValues()
                    timeToRun += timedelta(minutes= interval)
                        
                else:
                    print('need wait', timeToRun - nt, 'more')
                