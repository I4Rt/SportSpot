from __future__ import annotations
from config import *
from typing import List

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False)
    classId = db.Column(db.Integer, unique=False)
    sportObjectId = app.config['SPORT_OBJECT_ID']
    
    def __init__(self, name:str, classId:int = 0):
        self.name = name
        self.classId = classId
        
