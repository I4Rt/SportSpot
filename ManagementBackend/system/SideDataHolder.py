from model.data.Room import *

class SideDataHolder():
    __instance = None
    
    def __init__(self):
        self.rooms = {}
        self.changedTasks = []
        self.updateRoomList()
        
    def setChangedTask(self, taskId):
        if not (taskId in self.changedTasks):
            self.changedTasks.append(taskId)
        
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
               
    def removeTask(self, taskId):
         for _ in self.changedTasks:
                if _ == taskId:
                    self.changedTasks.remove(_)    
                    
    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = SideDataHolder()
        return cls.__instance
    
    def getSavedChangedTasks(self):
        try:
            with open('existToUpdateData.txt', 'r') as file:
                data_ = json.loads(file.read())
                for id_ in data_:
                    self.setChangedTask(id_)
        except:
            with open('existToUpdateData.txt', 'w') as file:
                file.write(json.dumps([]))
                
    def saveChangedTasks(self):
        with open('existToUpdateData.txt', 'w') as file:
            file.write(json.dumps(self.changedTasks))
                
    
    
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
        