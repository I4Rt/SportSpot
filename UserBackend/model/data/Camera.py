from __future__ import annotations
from config import *
from typing import List
from model.data.BaseData import *
import model.data as modules

class Camera(db.Model, BaseData):
    name = db.Column(db.String(150), unique=False)
    # TODO: make the rest of the fields
    
    def __init__(self, name:str):
        db.Model.__init__(self)
        BaseData.__init__(self, self.id)
        self.name = name
        
        
    def getSectors(self):
        return modules.Sector.Sector.query.filter_by(camId=self.id).all()
        

            