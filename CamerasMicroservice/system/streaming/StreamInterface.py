from system.streaming.PermanentStreamer import PermanentStreamer
from time import sleep, time
class StreamInterface:
    '''
    в случае попадания в интервал финиш - удаление, 
    производится принудительное закрытие и удаление стрима,
    далее создание нового
    '''
    
    @classmethod
    def initStream(cls, route, timeLimit = 120):
        ident = PermanentStreamer.appendToQueue(route, timeLimit)
        
        for i in range(900):       # 3 min
            res = PermanentStreamer.checkCreated(ident)
            if type(res) == bool:
                return res
            sleep(0.2)
        return False
        
    
   
        
    '''route будет приведен к строке'''
    @classmethod
    def getFrame(cls, route:str|int):
        return PermanentStreamer.getNext(route)

        
        
        
        
    
    @classmethod
    def refreshStream(cls, route:str, newTime: float | int):
        return PermanentStreamer.refreshStream(route, newTime)
    