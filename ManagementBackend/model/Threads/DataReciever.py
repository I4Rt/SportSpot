from model.data.Task import *
from model.data.Result import *
from threading import Thread
from model.QueueTaskHolder import *
from system.kafka.KafkaSingleton import *
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
                task = Task.getByID(int(data["taskID"]))
                if task is not None:
                    task.setCount(int(data["counter"]))
                    print(f'set counter {int(data["counter"])} to task {task}')
                else:
                    print(f'recieved task does not exist')
                    