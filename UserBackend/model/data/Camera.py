from __future__ import annotations
from config import *
from typing import List

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False)
    # TODO: make the rest of the fields
    
    def __init__(self, name:str):
        self.name = name
        