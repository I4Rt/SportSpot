from __future__ import annotations
from config import *
from typing import List
from model.data.BaseData import *

import model.data as modules
from model.data.types.RoomType import *

class Room(db.Model, BaseData):
    name = db.Column(db.String(150), unique=False)
    classId = db.Column(db.Integer, unique=False)
    sportObjectId = app.config['SPORT_OBJECT_ID']
    
    def __init__(self, name:str, classId:int = 0):
        db.Model.__init__(self)
        BaseData.__init__(self, self.id)
        self.name = name
        self.classId = classId
    
    def getSectors(self) -> List[modules.Sector.Sector]:
        return modules.Sector.Sector.query.filter_by(roomId=self.id).all()
    
    
    

    def getCameras(self) -> List[modules.Camera.Camera]:
        exist = []
        result = []
        for sector in modules.Sector.Sector.query.filter_by(roomId=self.id).all():
            camera = modules.Camera.Camera.query.filter_by(id=sector.camId).first()
            if camera.id not in exist:
                exist.append(camera.id)
                result.append(camera)
        return result
    
    def getObjectClass(self):
       return modules.types.RoomType.RoomType.query.filter_by(id = self.classId)
   
    def dropSectors(self):
        db.session.query(modules.Sector.Sector).filter(
            modules.Sector.Sector.roomId == self.id
            ).update({modules.Sector.Sector.roomId:None})
        
    
        
