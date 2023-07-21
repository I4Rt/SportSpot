from __future__ import annotations
from config import *
from typing import List
from model.data.BaseData import *
import model.data as modules

class Camera(db.Model, BaseData):
    name = db.Column(db.String(150), unique=False)
    ip = db.Column(db.String(150), unique=False)
    chanel = db.Column(db.Integer, unique=False)
    codec = db.Column(db.String(150), unique=False)
    login = db.Column(db.String(150), unique=False)
    password = db.Column(db.String(150), unique=False)
    # TODO: make the rest of the fields
    
    def __init__(self, name:str, ip:str = None, chanel:int = None, codec:str = None, login:str = None, password:str = None):
        db.Model.__init__(self)
        BaseData.__init__(self, self.id)
        self.name = name
        self.ip = ip
        self.chanel = chanel
        self.codec = codec
        self.login = login
        self.password = password
        
        
    def getSectors(self):
        return modules.Sector.Sector.query.filter_by(camId=self.id).all()
    @staticmethod
    def getSectorsById(searchId):
        return modules.Sector.Sector.query.filter_by(camId=searchId).all()
        
        

            