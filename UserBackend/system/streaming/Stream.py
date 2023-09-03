from time import time, sleep
from model.data.Camera import Camera
import cv2
import threading

import config
class Stream:
    
    __camRoute:str|int = 0
    __streaming:cv2.VideoCapture | None = None
    __timeLimit = 10
    __deleteTime = 5
    
    def __init__(self, camera:Camera, timeLimit = 10):
        self.__timeLimit = timeLimit
        # BAD routing
        self.__camRoute = camera.getRoute()
        self.__generator = None
        self.__finished = False
        self._lastAskTime = None
        self.__image = b''
    
    
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
        while not self._checkDelete(): # checkDelete?
            # print('getter thread')
            try:
                result, frame = self.__streaming.read()
                if result:
                    ret, jpeg = cv2.imencode('.jpg', frame)
                    self.__image = jpeg.tobytes()
                    self.__generator = self.__getFrames()
                    sleep(0.2)
            except:
                pass
            # print(self.__image)
            
            
    
    
    def getStream(self):
        return self.__generator
    
    def __getFrames(self):
        if self.__streaming == None:
            raise Exception('First try to connect the camera')
        
        while not self._checkDelete(): # or _checkDelete
            if not self.__finished:
                try:
                    if self.__image == b"":
                        yield (b'--frame\r\n'
                                b'Content-Type: image/jpeg\r\n\r\n' + config.byteWaitImage + b'\r\n')
                    else:
                        yield (b'--frame\r\n'
                                b'Content-Type: image/jpeg\r\n\r\n' + self.__image + b'\r\n')
                    # sleep(0.2)
                except Exception as e:
                    raise e
            
        return (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + self.__image + b'\r\n')
        
        
    def _resetTime(self):
        self.__finished = False
        self.__lastAskTime = time()
        
    def _checkFinished(self):
        # print(self.__finished)
        # if not self.__finished:
            if self.__timeLimit < time() - self.__lastAskTime:
                self.__finished = True
                return True
            return False
        # return True
    
    def _checkDelete(self):
        if self._checkFinished():
            if self.__timeLimit + self.__deleteTime < time() - self.__lastAskTime:
                self._release()
                self.__generator.close()
                return True
            return False
        return False
        
            
    
        
            
    