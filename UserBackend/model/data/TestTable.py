from __future__ import annotations
from tools.Jsonifyer import Jsonifyer
from config import *
from typing import List
from json import *
from model.data.BaseData import BaseData
class TestTable(db.Model, BaseData):
    data = db.Column(db.Text, unique=False)
    
    def __init__(self, 
                 data:str = ''):
        db.Model.__init__(self)
        BaseData.__init__(self, self.id)
        self.data = data
        
    
    def getParamsList(self) -> str:
        try:
            return {'type': 'testData', 'id': self.id, 'data':loads(self.data).encode('utf8')}
        except Exception:
            return {'type': 'testData', 'id': self.id, 'data':self.data}
        
    
    def saveData(self, newData: object) -> None:
        self.data = dumps(newData).encode('utf8')
        
    
    
