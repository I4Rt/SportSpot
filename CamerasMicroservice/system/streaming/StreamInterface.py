from system.streaming.StreamBase import StreamBase
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
        ident = StreamBase.appendToQueue(route, timeLimit)
        if ident:
            for i in range(100):
                if StreamBase.checkCreated(ident):
                    return True
                sleep(1)
        return False
        
    
   
        
    
    @classmethod
    def getFrame(cls, route:str|int):
        # if route.isdigit():
        #     route = int(route)
        print( 'getting frame', route)
        for stream in StreamBase._getStreams():
            if str(stream.getRoute()) == str(route):
                if not stream._checkFinished():
                    print('get frame is here')
                    return next(stream.getStream())
                # else:                              # TODO: check if ness
                #     stream._release()
        
        print('not HEre')
        
        
    
    @classmethod
    def refreshStream(cls, route:str, newTime: float | int):
        return StreamBase.refreshStream(route, newTime)
    