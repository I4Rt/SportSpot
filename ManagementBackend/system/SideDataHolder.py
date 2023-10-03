from model.data.Room import *

class SideDataHolder():
    __instance = None
    
    def __init__(self):
        self.rooms = {}
        self.updateRoomList()
        
        
    def updateRoomList(self):
            roomData = [r.id for r in Room.getAll()]
            for rId in self.rooms:
                if not (rId in roomData):
                    del self.rooms[rId]
            for rId in roomData:
                if not ( rId in self.rooms ):
                    self.rooms[rId] = 0
                    
                    
    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = SideDataHolder()
        return cls.__instance
    
    @classmethod
    def setResult(cls, key, data):
        print('set', key, data)
        cls.__instance.rooms[key] = data
        