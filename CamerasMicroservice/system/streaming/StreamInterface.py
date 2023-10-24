from system.streaming.StreamBase import StreamBase
from system.streaming.Stream import Stream
from time import sleep
class StreamInterface:
    
    @classmethod
    def initStream(cls, route, timeLimit = 120):
        if route.isdigit():
            route = int(route)
        for stream in StreamBase._getStreams():
            print(stream._checkFinished(), route, stream.getRoute())
            if not stream._checkFinished() and stream.getRoute() == route:
                stream._resetTime(timeLimit)
                return stream.getStream()
        stream = Stream(route, timeLimit)
        stream.init()
        StreamBase._addStream(stream)
        
    
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
        for stream in StreamBase._getStreams():
            print('compare', stream.getRoute(), type(stream.getRoute()), route, type(route))
            if not stream._checkFinished() and str(stream.getRoute()) == route:
                stream._resetTime(newTime)
                return True
        return False
    