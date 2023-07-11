from __future__ import annotations
from config import *
from typing import List

class RoomType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False)
    
    def __init__(self, name:str):
        super.__init__(self)
        self.name = name