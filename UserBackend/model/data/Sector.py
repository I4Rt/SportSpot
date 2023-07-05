from __future__ import annotations
from config import *
from typing import List

class Sector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False)
    typeId = db.Column(db.Integer, unique=False, nullable=False)
    camId = db.Column(db.Integer, unique=False)
    roomId = db.Column(db.Integer, unique=False)
    
    
    def __init__(self, name:str, typeId:int, camId:int, roomId:int):
        self.name = name
        self.typeId = typeId
        self.camId = camId
        self.roomId = roomId
        
