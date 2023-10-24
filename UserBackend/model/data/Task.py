from __future__ import annotations
from config import *
from typing import List
from model.data.BaseData import *
import  model.data as modules
from model.data.Result import Result

from model.data.Camera import Camera

from datetime import datetime, timedelta
from sqlalchemy import or_, and_

class Task(db.Model, BaseData):
    name = db.Column(db.Text, default = "")
    targetCount = db.Column(db.Integer, default = 0)
    comment = db.Column(db.Text, default = "")
    begin = db.Column(db.DateTime(timezone=True))
    end = db.Column(db.DateTime(timezone=True))
    interval = db.Column(db.Integer, default = 10)
    roomId = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    color = db.Column(db.Text, default=None)
    __status = db.Column(db.Integer, default=0)
    
    __table_args__ = (
        db.UniqueConstraint('roomId', 'begin', name='_room_unique_task'),
    )
    
    
    
    def __init__(self, begin, end, roomId, name = 'Не названо', targetCount = 0, comment="", interval:int=None, color:str=None):
        self.begin = begin
        self.end = end
        self.roomId = roomId
        self.name = name
        self.comment = comment
        self.targetCount = targetCount
        if interval != None:
            self.interval = interval
        else:
            self.interval = 30
        self.__status = 0
        self.color = color
        
    def setColor(self, color):
        self.color = color
        
    def getStatus(self):
        return self.__status
        
    def setStatusInProgress(self):
        self.__status = 1
        self.save()
    def setStatusDone(self):
        self.__status = 2
        self.save()
        
    def _setStatusDone(self):
        self.__status = 2
        
    
    
    # время не должно быть меньше текущего если условие задано
    # время не должно содержаться в существующем отрезке
    # начало должно быть меньше конца
    def _isValid(self, checkFuture=True):
        if self.begin < self.end:
                
            
            cond1 = datetime.strptime(str(self.begin)[:19], '%Y-%m-%d %H:%M:%S') > datetime.now()
            if (cond1 and checkFuture) or (not cond1 and not checkFuture):
                existCoveredTasks = Task.getCoveredTasksByRoomId(self.id, self.roomId, self.begin, self.end)
                print('covered tasks', len (existCoveredTasks))
                if len(existCoveredTasks) == 0:
                    return True
                
        return False
    
    def save(self, needCheckFuture=True):
        print('presave f is', needCheckFuture)
        if not self._isValid(needCheckFuture):
            raise (Exception('The task is not valid (is covered or the beginning is in the past or greater then the end)'))
        
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
    def getTasksAtDay(cls, date, room = None) -> List[Task]:
        eTime = date + timedelta(days=1)
        if not room:
            return db.session.query(Task).filter(
                    and_(
                        cls.begin >= date, 
                        cls.end <= eTime,
                    ) 
                ).all()
        return db.session.query(Task).filter(
                and_(
                    cls.begin >= date, 
                    cls.end <= eTime,
                    cls.roomId == room
                ) 
            ).all()
            
    @classmethod
    def getTasksToRun(cls, datetime:type(datetime.now()) = datetime.now()):
        return db.session.query(Task).filter(
            and_(
                 datetime >= cls.begin, 
                 cls.__status == 0,
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
                        bTime < cls.end
                    ),
                    and_(
                        eTime > cls.begin, 
                        eTime <= cls.end
                    )
                )
            )
        ).all()
    
    
    def getCamera(self):
        return db.session.query(Camera).filter(
            Camera.id == self.camId
        ).first()
        
