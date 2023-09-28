from __future__ import annotations
from config import *
from model.BaseData import *
    

class SportObject(db.Model, BaseData):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=False)
    info = db.Column(db.Text, unique=False, nullable=True)
    outerId = db.Column(db.Text, unique=True)
    
    
    def __init__(self, name:str, outerId:str, info:str = None):
        db.Model.__init__(self)
        BaseData.__init__(self, self.id)
        self.name = name
        self.info = info
        self.outerId = outerId
        
        
        
        
        