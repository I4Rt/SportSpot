from threading import Thread
from system.streaming.Stream import Stream
from time import sleep
from datetime import datetime
class StreamBase:
    __initialized:bool = False
    __streams = []
    __needContinue = True
    __thread = None
    @classmethod
    def _getStreams(cls):
        if cls.__initialized:
            return cls.__streams
    
    @classmethod
    def _addStream(cls, stream:Stream):
        if cls.__initialized:
            cls.__streams.append(stream)
            print('inited')
            return True
    
    
    @classmethod
    def __checkStreams(cls):
        while cls.__needContinue:
            sleep(2)
            if len(cls.__streams) > 0:
                print('threads lenght is', len(cls.__streams), [s.getRoute() for s in cls.__streams])
                for stream in cls.__streams:
                    if Stream._checkDelete(stream):
                        cls.__streams.remove(stream)
                        routes = [s.getRoute() for s in cls.__streams]
                        stilContain = stream.getRoute() in routes
                        if stilContain:
                            with open('StreamQueue.txt', 'a') as f:
                                f.write(f'{datetime.now()}\nremoved: {stream.getRoute()}\nroute now is: {routes}\n\n')
                        print('removing thread', stream.getRoute(), stilContain)
                        
    
    @classmethod
    def init(cls):
        if cls.__thread:
            try:
                cls.__initialized = False
                cls.__needContinue = False
                cls.__thread.join()
            except:
                pass
        cls.__needContinue = True
        cls.__thread = Thread(target=cls.__checkStreams)
        cls.__thread.start()
        cls.__initialized = True
    


