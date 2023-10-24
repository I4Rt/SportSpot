from __future__ import annotations
from config import *
from model.BaseData import *
from model.SportObject import *
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
        db.UniqueConstraint('date', 'timeInterval', 'sportObjectId', 'roomId', name='_datetime_unique', deferrable=True, initially="DEFERRED"),
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
    
    
    def update(self):
        with app.app_context():
            # print('to delete is ', len(db.session.query(DataRow).filter(
            #     and_
            #     (
            #         DataRow.sportObjectId == self.sportObjectId,
            #         DataRow.roomId == self.roomId,
            #         DataRow.date == self.date,
            #         DataRow.timeInterval == self.timeInterval,
            #         DataRow.real <= self.real
            #     ),
            # ).all()))
            # try:
            result = db.session.query(DataRow).filter(
                and_
                (
                    DataRow.sportObjectId == self.sportObjectId,
                    DataRow.roomId == self.roomId,
                    DataRow.date == self.date,
                    DataRow.timeInterval == self.timeInterval,
                    DataRow.real <= self.real
                ),
            ).update({DataRow.real: self.real})
            
                    
            
            db.session.commit()
            
            return result
            
    
    @classmethod  
    def getInInterval(cls, bd, bt, ed, et, id = None) -> List[DataRow]:
        if id:
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
                    ),
                    DataRow.sportObjectId == id
                )
            ).all()
            
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
        db.session.commit()
        
    
    def getSideSOId(self) -> List[DataRow]:
        return db.session.query(SportObject).filter(
            self.sportObjectId == SportObject.id
        ).first().outerId