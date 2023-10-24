from time import time, sleep
from model.data.Camera import Camera
import cv2
import threading

import config
class Stream:
    
    __camRoute:str|int = 0
    __streaming:cv2.VideoCapture | None = None
    __timeLimit = 120
    __deleteTime = 5
    
    def __init__(self, camera:Camera, timeLimit = 120):
        self.__timeLimit = timeLimit
        # BAD routing
        self.__camRoute = camera.getRoute()
        self.__generator = None
        self.__finished = False
        self._lastAskTime = None
        self.__image = None
    
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
        try:
            if self.__streaming == None:
                self.__streaming = cv2.VideoCapture(self.__camRoute)
        except:
            self.__streaming = None
            raise Exception('Can not capture the video')
    
    def _release(self):
        if self.__streaming != None:
            self.__streaming.release()
            
    def init(self):
        self._connect()
        self.__finished = False
        self.__lastAskTime = time()
        getterThread = threading.Thread(target=self.__updateFrame, args=())
        getterThread.start()
        self.__generator = self.__getFrames()

    def __updateFrame(self):
        while not self._checkDelete(): 
            try:
                result, frame = self.__streaming.read()
                if result:
                    self.__image = frame
                    sleep(0.2)
            except:
                pass
            
            
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
                    # sleep(0.2)
                except Exception as e:
                    raise e
            
    def _resetTime(self, newTime = None):
        if newTime != None:
            self.__timeLimit = newTime
        self.__finished = False
        self.__lastAskTime = time()
        
    def _checkFinished(self):
       
        if self.__timeLimit < time() - self.__lastAskTime:
            self.__finished = True
            return True
        return False
    
    
    def _checkDelete(self):
        if self._checkFinished():
            if self.__timeLimit + self.__deleteTime < time() - self.__lastAskTime:
                self._release()
                return True
            return False
        return False
        
            
    
        
            
    