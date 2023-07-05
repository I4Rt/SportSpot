from __future__ import annotations
from tools.Jsonifyer import Jsonifyer
from config import *
from typing import List
from json import *

class TestTable(db.Model, Jsonifyer):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, unique=False)
    
    def __init__(self, 
                 data:str = ''):
        super.__init__(self)
        self.data = data
        
    
    def getJson(self) -> str:
        try:
            return {'type': 'testData', 'id': self.id, 'data':loads(self.data).encode('utf8')}
        except Exception:
            return {'type': 'testData', 'id': self.id, 'data':self.data}
        
    
    def saveData(self, newData: object) -> None:
        self.data = dumps(newData).encode('utf8')
        
    @staticmethod
    def getAll() -> List[TestTable]:
        return TestTable.query.all()
