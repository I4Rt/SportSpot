from system.streaming.StreamBase import StreamBase
from system.streaming.Stream import Stream
from model.data.Camera import Camera
from time import sleep
class StreamInterface:
    
    @classmethod
    def getStream(cls, camera:Camera, timeLimit = 120):
        route = camera.getRoute()
        print(f"route is {route}")
        for stream in StreamBase._getStreams():
            print(stream._checkFinished(), route, stream.getRoute())
            if not stream._checkFinished() and stream.getRoute() == route:
                stream._resetTime(timeLimit)
                return stream.getStream()
        stream = Stream(camera, timeLimit)
        stream.init()
        # print(f'inited in time {stream.getLastAskTime()}')
        StreamBase._addStream(stream)
        return stream.getStream()
    
    @classmethod
    def refreshStream(cls, camera: Camera, newTime = None):
        route = camera.getRoute()
        for stream in StreamBase._getStreams():
            if not stream._checkFinished() and camera.getRoute() == route:
                stream._resetTime(newTime)
                return 'Done'
        return 'Stream is finished'
        
        
            
    