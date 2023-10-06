from model.data.Room import *

class SideDataHolder():
    __instance = None
    
    def __init__(self):
        self.rooms = {}
        self.updateRoomList()
        
        
    def updateRoomList(self):
        try:
            roomData = [r.id for r in Room.getAll()]
            for rId in self.rooms:
                if not (rId in roomData):
                    del self.rooms[rId]
            for rId in roomData:
                if not ( rId in self.rooms ):
                    self.rooms[rId] = 0
        except:
            print('error in roomListUpdate')
                    
                    
    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = SideDataHolder()
        return cls.__instance
    
    @classmethod
    def setResult(cls, key, data):
        print('use to set', data, 'key type is', type(key))
        if key in cls.__instance.rooms:
            print('key found')
            if cls.__instance.rooms[key] >= data:
                print('data is greater')
                return
        
        cls.__instance.rooms[key] = data
        print('set', cls.__instance.rooms)
        
    @classmethod
    def resetValues(cls):
        print('dropping')
        cls.__instance.rooms={}
        