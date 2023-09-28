from __future__ import annotations
from config import *
from model.BaseData import *
    

class DataRow(db.Model, BaseData):
    id = db.Column(db.Integer, primary_key=True)
    sportObjectId = db.Column(db.Integer, db.ForeignKey('sport_object.id'), nullable=False)
    date = db.Column(db.DateTime(timezone=False), nullable=False)
    timeInterval = db.Column(db.Time(), nullable=False)
    plan = db.Column(db.Integer, nullable=False)
    real = db.Column(db.Integer, nullable=False)
    
    def __init__(self, sportObjectId:int, date, timeInterval, plan:int, real:int):
        db.Model.__init__(self)
        BaseData.__init__(self, self.id)
        self.sportObjectId = sportObjectId
        self.date = date
        self.timeInterval = timeInterval
        self.plan = plan
        self.real = real
        