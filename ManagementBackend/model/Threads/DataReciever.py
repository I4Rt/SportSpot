from model.data.Task import *
from model.data.Result import *
from threading import Thread
from model.QueueTaskHolder import *
from system.kafka.KafkaSingleton import *
from time import altzone, timezone, localtime
from system.SideDataHolder import *
class DataReciever(Thread):
    
    def __init__(self) -> None:
        Thread.__init__(self)
        
    def run(self):
        with app.app_context():
            reciever = KafkaReciever.getInstance()
            for msg in reciever.recieve():
                '''
                    if data[counter] > task.counter and task.end < datetime.now():
                        task intervals  <-  {date: {time1: data[counter], 
                                                    time1: data[counter], 
                                                    time1: data[counter], 
                                                    ...}}
                    toSendDataHolder += tasks
                    
                    ~~~ for data in toSendDataHolder if data.send(): toSendDataHolder.remove(data) ~~~
                                                      
                '''
                
                print(str(msg.value))
                #save
                data = json.loads(msg.value)
                if str(data["taskId"]).isdigit():
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