from __future__ import annotations
from config import *
from typing import List
from model.data.BaseData import *
import  model.data as modules
from shapely.geometry import Point, Polygon
import numpy as np
import math
    

class Sector(db.Model, BaseData):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False)
    typeId = db.Column(db.Integer, unique=False, nullable=False)
    camId = db.Column(db.Integer, unique=False)
    roomId = db.Column(db.Integer, unique=False)
    __points = db.Column(db.Text, unique=False)
    
    
    def __init__(self, name:str, typeId:int, camId:int, roomId:int, points:List = []):
        db.Model.__init__(self)
        BaseData.__init__(self, self.id)
        self.name = name
        self.typeId = typeId
        self.camId = camId
        self.roomId = roomId
        self.__points = json.dumps(points)
    
    @staticmethod
    def orderPoints(points):
        listx = [p[0] for p in points]
        listy = [p[1] for p in points]
        start_point = listx[0], listy[0]
        sorted_points = []
        while len(start_point)>0:
            sorted_points.append(start_point)
            x1, y1 = start_point
            dists = {(x2, y2): np.sqrt((x1-x2)**2 + (y1-y2)**2) for x2, y2 in zip(listx, listy)}
            dists = sorted(dists.items(), key=lambda item: item[1])
            for dist in dists:
                if dist[0] not in sorted_points: 
                    start_point = dist[0]
                    break
                if dist == dists[-1]:
                    start_point = ()
                    break
        return sorted_points
    
    @staticmethod
    def checkIfInside(border, target):
        # Create Point objects
        p = Point(target[0], target[1])
        poly = Polygon(border)
        return p.within(poly)
    
    def getPointList(self):
        return json.loads(self.__points)
    
    def setPointList(self, points):
        self.__points = json.dumps(points)
        
    def getCamera(self):
        return modules.Camera.Camera.query.filter_by(id = self.camId)
        
    def orderPointsOfMe(self):
        data = __class__.orderPoints(self.__points)
        self.setPointList(data)
        return data

    def checkCointain(self, point:List[float, float]) -> bool:
        return __class__.checkIfInside(self.getPointList(), point)
    
