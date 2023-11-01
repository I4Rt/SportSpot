from system.streaming.StreamBase import StreamBase
from system.streaming.Stream import Stream
from time import sleep
class StreamInterface:
    '''
    в случае попадания в интервал финиш - удаление, 
    производится принудительное закрытие и удаление стрима,
    далее создание нового
    '''
    
    @classmethod
    def initStream(cls, route, timeLimit = 120):
        if route.isdigit():
            route = int(route)
        stream = StreamBase.initStream(route, timeLimit)
        
        return stream.getStream()
    
   
        
    
    @classmethod
    def getFrame(cls, route:str|int):
        if route.isdigit():
            route = int(route)
        for stream in StreamBase._getStreams():
            if not stream._checkFinished() and stream.getRoute() == route:
                print('get frame is here')
                return next(stream.getStream())
        print('not HEre')
        
        
    
    @classmethod
    def refreshStream(cls, route:str, newTime: float | int):
        return StreamBase.refreshStream(route, newTime)
    