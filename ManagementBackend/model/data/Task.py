from __future__ import annotations
from config import *
from typing import List
from model.data.BaseData import *
import  model.data as modules
from model.data.Result import Result
from model.data.Camera import Camera

from tools.SessionFabric import *

from datetime import datetime, timedelta, timezone
from dateutil import parser
from sqlalchemy import or_, and_

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Task(db.Model, BaseData):
    name = db.Column(db.Text, default = "")
    targetCount = db.Column(db.Integer, default = 0)
    comment = db.Column(db.Text, default = "")
    begin = db.Column(db.DateTime(timezone=True))
    end = db.Column(db.DateTime(timezone=True))
    interval = db.Column(db.Integer, default = 10)
    roomId = db.Column(db.Integer, nullable=False)
    __status = db.Column(db.Integer, default=0)
    color = db.Column(db.Text)
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
                
    def setStatusDone(self):
        self.__status = 2

        
    
    
    # время не должно быть меньше текущего
    # время не должно содержаться в существующем отрезке
    # начало должно быть меньше конца
    def _isValid(self):
        if self.begin < self.end:
            if parser.parse(str(self.begin)) > datetime.now(tz=timezone(timedelta(hours=7))):
                if self.id != None:
                    existCoveredTasks = Task.getCoveredTasksByRoomId(self.id, self.roomId, self.begin, self.end)
                    if len(existCoveredTasks) == 0:
                        return True
                return True
        return False
    
    # def __save(self):
    #     engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    #     Session = sessionmaker(engine)
    #     with Session() as localSession:
    #         localSession.add(self)
    #         localSession.commit()
    #         localSession.close()
    #         localSession.remove()
        
    @sessionly
    def save(self, needValid = True):
        print('save')
        if needValid:
            if not self._isValid():
                raise (Exception('The task is not valid (is covered or the beginning is in the past or greater then the end)'))
        db.session.add(self)
        if self.__getResult() == None:
            result = Result(self.id)
            db.session.add(result)
        #print(f'saved, statis is {self.__status}')
    
    @classmethod
    def getStatused(cls):
            return db.session.query(Task).filter(
            cls.__status == 1
        ).all()
            
    @sessionly
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
    def getTasksToRun(cls, datetime:type(datetime.now())):
        res =  db.session.query(Task).filter(
            and_(
                 datetime < cls.end, 
                 datetime >= cls.begin, 
                 cls.__status == 0,
            ) 
        ).all()
        for i in res:
            print(i.begin)
        return res
        
    @classmethod
    def getContainedTasksByRoomId(cls, selfId, roomId, bTime, eTime) -> List[Task]:
        return db.session.query(Task).filter(
            and_(cls.roomId == roomId,
                 bTime >= cls.begin, 
                 eTime <= cls.end,
                 cls.id != selfId
            )
        ).all()

    @sessionly
    def __getResult(self):
        return db.session.query(Result).filter(Result.taskId == self.id).first()
    
    def getCount(self) -> int:
        result = self.__getResult()
        return result.getPeopleCount()
    
    @sessionly
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
    
    def getCamera(self):    
        return db.session.query(Camera).filter(
            Camera.id == self.roomId
        ).first()
    
    @classmethod
    @sessionly
    def getById(cls, searchId:int) -> Task:
        return db.session.query(Task).filter_by(id=searchId).first()