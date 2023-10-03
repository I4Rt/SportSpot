from model.data.Task import *
from model.data.Result import *
from threading import Thread
from model.QueueTaskHolder import *
from system.kafka.KafkaSingleton import *

from system.SideDataHolder import *
class DataReciever(Thread):
    
    def __init__(self) -> None:
        Thread.__init__(self)
        
    def run(self):
        with app.app_context():
            reciever = KafkaReciever.getInstance()
            for msg in reciever.recieve():
                print(str(msg.value))
                #save
                data = json.loads(msg.value)
                if str(data["taskID"]).isdigit():
                    task = Task.getByID(int(data["taskID"]))
                    if task is not None:
                        if int(data["counter"]) > task.getCount():
                            task.setCount(int(data["counter"]))
                            print(f'set counter {int(data["counter"])} to task {task}')
                    else:
                        print(f'recieved task does not exist')
                else:
                    print('setting side task data')
                    roomId = int( data["taskID"].split('_')[-1] )
                    print(data)
                    SideDataHolder.setResult(roomId, int(data["counter"]))