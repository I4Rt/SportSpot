from __future__ import annotations
from config import *
from typing import List
from model.data.BaseData import *
import model.data as modules


class Camera(db.Model, BaseData):
    name = db.Column(db.String(150), unique=False)
    ip = db.Column(db.String(150), unique=False)
    port = db.Column(db.Integer, unique=False)
    chanel = db.Column(db.Integer, unique=False)
    codec = db.Column(db.String(150), unique=False)
    login = db.Column(db.String(150), unique=False)
    password = db.Column(db.String(150), unique=False)
    fullRoute = db.Column(db.Text(), unique = True)
    # TODO: make the rest of the fields
    
    def __init__(self, name:str, ip:str = None, port:int = None, chanel:int = None, codec:str = None, login:str = None, password:str = None, fullRoute: str | int | None= None):
        db.Model.__init__(self)
        BaseData.__init__(self, self.id)
        self.name = name
        self.ip = ip
        self.chanel = chanel
        self.codec = codec
        self.login = login
        self.port = port
        self.password = password
        self.fullRoute = fullRoute
        
        
    def getSectors(self):
        return modules.Sector.Sector.query.filter_by(camId=self.id).all()
    @staticmethod
    def getSectorsById(searchId):
        return modules.Sector.Sector.query.filter_by(camId=searchId).all()
        
    def dropSectors(self):
        db.session.query(modules.Sector.Sector).filter(
            modules.Sector.Sector.camId == self.id
            ).delete()
         

    def getRoute(self):
        route = None
        # Bad route
        if self.fullRoute == None:
            route = 'rtsp://' + self.login + ':' + self.password + '@'+self.ip + ':' + str(self.port) +'/'
        else:
            route = self.fullRoute
            if route.isdigit():
                route = int(self.fullRoute)
        return route