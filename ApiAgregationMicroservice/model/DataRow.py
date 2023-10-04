from __future__ import annotations
from config import *
from model.BaseData import *

from sqlalchemy import UniqueConstraint
from sqlalchemy import and_, or_

class DataRow(db.Model, BaseData):
    id = db.Column(db.Integer, primary_key=True)
    sportObjectId = db.Column(db.Integer, db.ForeignKey('sport_object.id'), nullable=False)
    roomId = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(timezone=False), nullable=False)
    timeInterval = db.Column(db.Time(), nullable=False)
    plan = db.Column(db.Integer, nullable=False)
    real = db.Column(db.Integer, nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('date', 'timeInterval', 'roomId', name='_datetime_unique', deferrable=True, initially="DEFERRED"),
    )
    
    
    def __init__(self, sportObjectId:int,roomId:int, date, timeInterval, plan:int, real:int):
        db.Model.__init__(self)
        BaseData.__init__(self, self.id)
        self.sportObjectId = sportObjectId
        self.roomId = roomId
        self.date = date
        self.timeInterval = timeInterval
        self.plan = plan
        self.real = real
    
    # too bad: do not update - replaced by 2 operations
    def update(self):
        
        db.session.query(DataRow).filter(
            and_(
                DataRow.roomId == self.roomId,
                DataRow.date == self.date,
                DataRow.timeInterval == self.timeInterval
            ),
        ).delete()
        # print('delete is set')
        db.session.commit()
        # print('delete is done')
        self.save()
    
    @classmethod  
    def getInInterval(cls, bd, bt, ed, et) -> List[DataRow]:
        return db.session.query(DataRow).filter(
            and_(
                or_(DataRow.date >= bd + timedelta(days=1),
                    and_(DataRow.date == bd,
                         DataRow.timeInterval >= bt
                    )
                ),
                or_(DataRow.date <= ed - timedelta(days=1),
                    and_(DataRow.date == ed,
                         DataRow.timeInterval + timedelta(minutes=30) <= et
                    )
                )
            )
        ).all()