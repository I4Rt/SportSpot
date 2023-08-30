from __future__ import annotations
from tools.Jsonifyer import Jsonifyer
class QueueTaskHolder(Jsonifyer):
    
    __instance = None
    
    def __init__(self) -> None:
        Jsonifyer.__init__(self)
        self.__queue = []
        self.__tasksToSave == []
    @classmethod
    def getInstance(cls):
        if cls.__instance == None:
            cls.__instance = QueueTaskHolder()
        return cls.__instance
    
    def getQueue(self):
        return self.__queue
    
    def addToQueue(self, id:str, taksId:int):
        #check the o
        self.__queue.append({'identifyer': id, 'taksId': id})
        
    def addTaskToSave(self, task):
        self.__tasksToSave.append(task)
    def checkSaved(self, task):
        if self.__tasksToSave.index(task):
            return False
        return True
            
        
    def removeFromQueue(self, id:str):
        for record in self.__queue:
            if record['identifyer'] == id:
                self.__queue.remove(record)
                
        