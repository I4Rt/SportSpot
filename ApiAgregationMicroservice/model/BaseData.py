from __future__ import annotations
from config import *
from typing import List
from tools.Jsonifyer import Jsonifyer

class BaseData(Jsonifyer):
    id = db.Column(db.Integer, primary_key=True)
    
    def __init__(self, id = None):
        Jsonifyer.__init__(self)
        if id != None:
            self.id = id
            
    def save(self):
        try:
            
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print('save error', e)
            db.session.rollback()
   
    @classmethod 
    def getAll(cls) -> List[BaseData]:
        return cls.query.all()
    
    @classmethod 
    def getByID(cls, searchId:int) -> BaseData:
        return cls.query.filter_by(id=searchId).first()
    
   
    
    def delete(self):
        # print(f'deleting {self}')
        db.session.delete(self)
        db.session.commit()
    
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.getParamsList()}>"
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.getParamsList()}"
    
    
    
        
    