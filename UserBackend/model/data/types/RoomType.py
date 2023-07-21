from __future__ import annotations
from config import *
from typing import List
from model.data.BaseData import *

class RoomType(db.Model, BaseData):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False)
    
    def __init__(self, name:str):
        db.Model.__init__(self)
        BaseData.__init__(self, self.id)
        self.name = name