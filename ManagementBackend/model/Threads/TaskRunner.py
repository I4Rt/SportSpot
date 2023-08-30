from model.data.Task import *
from model.data.Result import *
from model.Threads.TaskProcesser import *
from threading import Thread
from model.QueueTaskHolder import *

from tools.Jsonifyer import Jsonifyer

from datetime import datetime
from time import sleep

class TaskRunner(Thread, Jsonifyer):
    
    __instance = None
    __stop = False
    
    def __init__(self) -> None:
        Thread.__init__(self)
        Jsonifyer.__init__(self)
    
    @classmethod
    def getInstance(cls):
        if cls.__instance == None:
            cls.__instance = TaskRunner()
        return cls.__instance
    
    @classmethod
    def stop(cls):
        cls.__stop = True
    
    @classmethod
    def __getStopMark(cls):
        return cls.__stop
    
    def run(self):
        with app.app_context():
            print('runner')
            while not TaskRunner.__getStopMark():
                sleep(5)
                
                # print(f'status in progress is {Task.getStatused()}')
                tasks = Task.getTasksToRun(datetime.now())
                # print(f'now tasks are: {tasks}')
                if tasks != None:
                    for task in tasks:
                        task.setStatusInProgress()
                        task.save(False)
                        # print(f'now status is {task.getStatus()}')
                        TaskProcessor(task).start()
                
            
            