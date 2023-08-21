from __future__ import annotations
from config import *
from typing import List
from model.data.BaseData import *
import  model.data as modules
from model.data.Result import Result


from datetime import datetime, timedelta
from sqlalchemy import or_, and_

class Task(db.Model, BaseData):
    name = db.Column(db.Text, default = "")
    targretCount = db.Column(db.Integer, default = 0)
    comment = db.Column(db.Text, default = "")
    begin = db.Column(db.DateTime(timezone=True))
    end = db.Column(db.DateTime(timezone=True))
    roomId = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    __status = db.Column(db.Integer, default=0)
    __table_args__ = (
        db.UniqueConstraint('roomId', 'begin', name='_room_unique_task'),
    )
    
    
    def __init__(self, begin, end, roomId, name = 'Не названо', targretCount = 0, comment=""):
        self.begin = begin
        self.end = end
        self.roomId = roomId
        self.name = name
        self.comment = comment
        self.targretCount = targretCount
        self.__status = 0

    def getStatus(self):
        return self.__status
        
    def setStatusInProgress(self):
        self.__status = 1
    def setStatusDone(self):
        self.__status = 2
        
    
    
    # время не должно быть меньше текущего
    # время не должно содержаться в существующем отрезке
    # начало должно быть меньше конца
    def _isValid(self):
        if self.begin < self.end:
            if self.begin > datetime.now():
                if self.id != None:
                    existCoveredTasks = Task.getCoveredTasksByRoomId(self.id, self.roomId, self.begin, self.end)
                    if len(existCoveredTasks) == 0:
                        return True
                return True
        return False
    
    def save(self):
        if not self._isValid():
            raise (Exception('The task is not valid (is covered or the beginning is in the past or greater then the end)'))
        else:
            db.session.add(self)
            if self.__getResult() == None:
                result = Result(self.id)
                db.session.add(result)
            db.session.commit()
    
    def delete(self):
        result = self.__getResult()
        db.session.delete(result)
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def getTasksByRoomId(cls, searchId) -> List[Task]:
        return cls.query.filter_by(roomId=searchId).all()
        
    @classmethod
    def getTasksAtDay(cls, date) -> List[Task]:
        
        eTime = date + timedelta(days=1)
        return db.session.query(Task).filter(
            and_(
                 date <= cls.begin, 
                 eTime > cls.end,
            ) 
        ).all()
        
    @classmethod
    def getContainedTasksByRoomId(cls, selfId, roomId, bTime, eTime) -> List[Task]:
        return db.session.query(Task).filter(
            and_(cls.roomId == roomId,
                 bTime >= cls.begin, 
                 eTime <= cls.end,
                 cls.id != selfId
            ) 
        ).all()
    
    def __getResult(self):
        return db.session.query(Result).filter(Result.taskId == self.id).first()
    def getCount(self) -> int:
        result = self.__getResult()
        return result.getPeopleCount()
    
    def setCount(self, newCount):
        result = self.__getResult()
        result.setPeopleCount(newCount)
        result.save()
    '''
    select * from tasks 
    where searchId == searchId and 
    ((begin > bTime and end < bTime) or 
    (begin > eTime and end < eTime))
    '''
    @classmethod
    def getCoveredTasksByRoomId(cls, selfId, roomID, bTime, eTime) -> List[Task]:
        return db.session.query(Task).filter(
            and_(
                cls.roomId == roomID,
                cls.id != selfId,
                or_(
                    and_(
                        bTime >= cls.begin, 
                        bTime <= cls.end
                    ),
                    and_(
                        eTime >= cls.begin, 
                        eTime <= cls.end
                    )
                )
            )
        ).all()
        
