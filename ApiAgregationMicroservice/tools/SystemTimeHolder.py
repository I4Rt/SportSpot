from datetime import datetime

class SystemTimeHolder:
    __timesToUpdateDataFrom = {}
    
    @classmethod
    def setTimeToUpdateFrom(cls, soId:int, dt:datetime):
        if soId in list(cls.__timesToUpdateDataFrom.keys()):
            if cls.__timesToUpdateDataFrom[soId]: # not None
                if dt > cls.__timesToUpdateDataFrom[soId] or dt > datetime.now(): # in future -> false
                    return False
        cls.__timesToUpdateDataFrom[soId] = dt
        return True
    
    @classmethod
    def getTimeToUpdateFrom(cls, soId:int):
        res = None
        if soId in list(cls.__timesToUpdateDataFrom.keys()):
            res = cls.__timesToUpdateDataFrom[soId]
        return res
    
    @classmethod
    def popTimeToUpdateFrom(cls, soId:int):
        res = None
        if soId in list(cls.__timesToUpdateDataFrom.keys()):
            res = cls.__timesToUpdateDataFrom[soId]
        cls.__timesToUpdateDataFrom[soId] = None
        return res
