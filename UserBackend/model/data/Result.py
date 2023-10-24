from __future__ import annotations
from config import *
from model.data.BaseData import *


class Result(db.Model, BaseData):
    __peopleCount = db.Column(db.Integer, default=0)
    taskId = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    
    
    def __init__(self, taskId):
        self.taskId = taskId
        self.__peopleCount = 0
        
    def setPeopleCount(self, newCount: int):
        self.__peopleCount = newCount
        
    def getPeopleCount(self) -> int:
        return self.__peopleCount