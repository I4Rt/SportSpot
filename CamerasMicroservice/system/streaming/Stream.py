from time import time, sleep
import cv2
import threading, multiprocessing
from tools.FileUtil import *
import config
import os
import sys
import signal

from tools.Jsonifyer import Jsonifyer

def streamStop( eMsg):
        raise Exception(eMsg)
    
class Stream(Jsonifyer):
    
    __camRoute:str|int = 0
    __streaming:cv2.VideoCapture | None = None
    __timeLimit = 120
    __deleteTime = 5
    __isRan = False
    def __init__(self, route:str, timeLimit = 120):
        Jsonifyer.__init__(self)
        self.__timeLimit = timeLimit
        print('initing: adding ' + str(self.__timeLimit) + 'more seconds')
        # BAD routing
        if type(route) == str:
            if route.isdigit():
                route = int(route)
        self.__camRoute = route
        self.__generator = None
        self.__finished = False
        self._lastAskTime = None
        self.__image = None
        self.__isRan = False
        
    
    def getParams(self):
        return [self.__camRoute, self._lastAskTime, self.__finished, self.__streaming]
    
    def getRoute(self):
        return self.__camRoute    
    
    def isFinished(self):
        return self.__finished    
    
    def getTimeDelta(self):
        return self.__timeLimit + self.__deleteTime - ( time() - self.__lastAskTime )
    
    def getLastAskTime(self):
        return self.__lastAskTime
    
    
    
    
    
    def _connect(self):
        b = time()
        try:
            if self.__streaming == None:
                print('connecting', self.__camRoute)
                # print('ppid', os.getpid())
                connectionThread = Stream.ThreadConnector(self.__camRoute)
                connectionThread.start()
                connectionThread.join(timeout=10)
                if not connectionThread.result:
                    connectionThread.stop()
                    raise Exception(self.__camRoute, 'connection timeout exception')
                self.__streaming = connectionThread.result
                
                print('time of initing videocapture is', time() - b)
                print('getting stream resilt', self.__streaming)
                
        except Exception as e:
            self.__streaming = None
            print('time of initing videocapture is', time() - b)
            raise Exception('Can not capture the video', type(e), e)
    
    def _release(self):
        if self.__streaming != None:
            self.__streaming.release()
            
    def init(self):
        self._connect()
        self.__finished = False
        self.__lastAskTime = time()
        getterThread = threading.Thread(target=self.__updateFrame, args=())
        getterThread.start()
        
        for _ in range(10):
            sleep(0.4)
            if self.__isRan:
                break
        self.__generator = self.__getFrames()

    def __updateFrame(self):
        while not self._checkDelete():
            try:
                result, frame = self.__streaming.read()
                if result:
                    self.__image = frame
                    self.__isRan = True
            except Exception as e:
                print(e)
            
            
    def getStream(self):
        return self.__generator
    
    def __getFrames(self):
        if self.__streaming == None:
            raise Exception('First try to connect the camera')
        while not self._checkDelete():
            if not self.__finished:
                try:
                    if self.__image is None:
                        yield None
                    else:
                        yield self.__image
                except Exception as e:
                    raise e
            
    def _resetTime(self, newTime):
        if newTime + time() > self.__timeLimit + self.__lastAskTime:
            print(f'stream {threading.currentThread().ident} of', self.__camRoute, 'reseting time')
            self.__timeLimit = newTime
            self.__finished = False
            self.__lastAskTime = time()
            print('reseting: adding ' + str(newTime) + ' more seconds')
        
    def _checkFinished(self):
            # print('stream of', self.__camRoute, 'rest time is', time() - self.__lastAskTime - self.__timeLimit, self.__timeLimit < time() - self.__lastAskTime, )
            if self.__timeLimit < time() - self.__lastAskTime:
                self.__finished = True
                return True
            return False
    
    def _checkDelete(self):
        if self._checkFinished():
            
            if self.__timeLimit + self.__deleteTime < time() - self.__lastAskTime:
                print(f'stream {threading.currentThread().ident} of', self.__camRoute, 'rest time is', time() - self.__lastAskTime - self.__timeLimit - self.__deleteTime, self.__timeLimit + self.__deleteTime < time() - self.__lastAskTime )
                self._release()
                return True
            return False
        return False
        
            
    class ThreadConnector(threading.Thread):
        
        def __init__(self, route):
            threading.Thread.__init__(self)
            self.route = route
            self.result = None
            self.pid = None
        
        def run(self):
            # print(threading.currentThread().ident)
            self.pid = os.getpid() 
            try:
                camera = cv2.VideoCapture()
                camera.setExceptionMode(True)
                camera.open(self.route)
                self.result = camera
            except:
                try:
                    camera.close()
                    try:
                        self.result.close()
                    except:
                        pass
                except:
                    pass
                
        
        def stop(self):
            raise Exception('timeout')
            
        

        
            
    