from threading import Thread
from system.streaming.Stream import Stream
from time import sleep
class StreamBase:
    __initialized:bool = False
    __streams = []
    @classmethod
    def _getStreams(cls):
        if cls.__initialized:
            return cls.__streams
    
    @classmethod
    def _addStream(cls, stream:Stream):
        if cls.__initialized:
            cls.__streams.append(stream)
            return True
    
    
    @classmethod
    def __checkStreams(cls):
        while True:
            sleep(2)
            # print(f'inside: {cls.__streams}')
            if len(cls.__streams) > 0:
                for stream in cls.__streams:
                    #print(f'has data: {stream.getParams()}')
                    if Stream._checkDelete(stream):
                        cls.__streams.remove(stream)
                        
    
    @classmethod
    def init(cls):
        t = Thread(target=cls.__checkStreams)
        t.start()
        cls.__initialized = True
    
    # @classmethod
    # def deleteStream(cls, route):
    #     for stream in cls.__streams:
    #         if stream.checkDelete():
    #             cls.__streams.remove(stream)
    

