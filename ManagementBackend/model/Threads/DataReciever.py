from model.data.Task import *
from model.data.Result import *
from threading import Thread
from model.QueueTaskHolder import *
from system.kafka.KafkaSingleton import *
from time import altzone, timezone, localtime
from system.SideDataHolder import *

from tools.LastTimeRunnerHolder import LastTimeRunnerHolder as ltrh
from datetime import datetime

from requests import get, ConnectTimeout
class DataReciever(Thread):
    
    def __init__(self) -> None:
        Thread.__init__(self)
        
    def run(self):
        with app.app_context():
            # reciever = KafkaReciever.getInstance()
            while True:
                '''
                    if data[counter] > task.counter and task.end < datetime.now():
                        task intervals  <-  {date: {time1: data[counter], 
                                                    time1: data[counter], 
                                                    time1: data[counter], 
                                                    ...}}
                    toSendDataHolder += tasks
                    
                    ~~~ for data in toSendDataHolder if data.send(): toSendDataHolder.remove(data) ~~~
                                                      
                '''
                try:
                    print('getting data from topic ', f'SO{int(app.config["SPORT_OBJECT_ID"])}_receive')
                    ltrh.setLastTime(datetime.now())
                    url = 'http://localhost:4998/readData'
                    
                    fetchData = get(url,params={'topic': f'SO{int(app.config["SPORT_OBJECT_ID"])}_receive'}, timeout=200)
                    fetchData = json.loads(fetchData.text)
                    print(fetchData)
                    if fetchData['readData']:
                        data = fetchData['data']['message']
                    else:
                        print('getting data from inner error', fetchData)
                        continue
                except Exception as e:
                    print('tmisot', e)
                    continue
                #save
                
                if str(data["taskId"]).isdigit():  
                    if data["taskId"] == 0:
                        print('handling zero taks')
                    task = Task.getByID(int(data["taskId"]))
                    
                    if task is not None:
                        if int(data["counter"]) > task.getCount():
                            task.setCount(int(data["counter"]))
                            print('get me here ', task.end)
                            offset = timezone if (localtime().tm_isdst == 0) else altzone
                            tz = int(offset / 60 / 60 * -1)
                            endTime = datetime.strptime(str(task.end)[:-6], '%Y-%m-%d %H:%M:%S') + timedelta(hours=tz)
                            
                            if endTime < datetime.now():
                                SideDataHolder.getInstance().setChangedTask(task.id)
                                SideDataHolder.getInstance().saveChangedTasks()
                                print('getOldTask", set data to changedTasksList')
                            print(f'set counter {int(data["counter"])} to task {task}')
                    else:
                        print(f'recieved task does not exist', int(data["taskId"]))
                else:
                    print('setting side task data', list(data.keys()))
                    try:
                        roomId = int( data["taskId"].split('_')[-1] )
                        print('good set is', data)
                        SideDataHolder.setResult(roomId, int(data["counter"]))
                        SideDataHolder.getInstance().updateRoomList()
                        
                    except:
                        pass