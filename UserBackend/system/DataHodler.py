class DataHolder:
    
    __instance = None
    __params = {}
    
    @classmethod
    def getInstance(cls):
        if cls.__instance == None:
            cls.__instance = DataHolder()
        return cls.__instance
    
    @classmethod
    def setParam(cls, paramName:str, value):
        cls.__instance.__params[paramName] = value
        
    @classmethod
    def getParam(cls, paramName:str):
        try:
            return cls.__instance.__params[paramName]
        except:
            return None
    