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
            for stream in cls.__streams:
                if stream._checkDelete():
                    print('p1 deleting', stream.getId())
                    cls.__streams.remove(stream)
            
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
                    if stream._checkDelete():
                        print('p1 deleting', stream.getId())
                        # stream._release()
                        try:
                            cls.__streams.remove(stream)
                        except:
                            pass
                        # routes = [s.getRoute() for s in cls.__streams]
                        # stilContain = stream.getRoute() in routes
                        # if stilContain:
                        #     with open('StreamQueue.txt', 'a') as f:
                        #         f.write(f'{datetime.now()}\nremoved: {stream.getRoute()}\nroute now is: {routes}\n\n')
                        print('removing thread', stream.getRoute())
                        # del stream
                        
    
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
        
    @classmethod
    def initStream(cls, route, timeLimit):
        for stream in cls.__streams:
            if stream.getRoute() == route:
                if not stream._checkFinished():
                    print('refreshing time on init')
                    stream._resetTime(timeLimit)
                    return stream
                else:
                    try:
                        stream._release()
                        cls.__streams.remove(stream)
                    except Exception as e:
                        print('deleting stream in interval failed', e)
                    break
        stream = Stream(route, timeLimit)
        stream.init()
        cls.__streams.append(stream)
        return stream
    
    @classmethod
    def refreshStream(cls, route, newTime):
        for stream in cls.__streams:
            print('compare', stream.getRoute(), type(stream.getRoute()), route, type(route))
            if not stream._checkFinished() and str(stream.getRoute()) == route:
                stream._resetTime(newTime)
                return True
        return False


