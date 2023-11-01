from time import time, sleep
import cv2
import threading, multiprocessing
from tools.FileUtil import *
import config
import os
import sys
import signal

from tools.Jsonifyer import Jsonifyer

from system.streaming.StopableThread import StopableThread

    
class Stream(Jsonifyer):
    
    __camRoute:str|int = 0
    _streaming:cv2.VideoCapture | None = None
    __timeLimit = 120
    __deleteTime = 5
    _isRan = False
    def __init__(self, route:str, timeLimit = 120):
        Jsonifyer.__init__(self)
        self.__timeLimit = timeLimit
        # print('initing: adding ' + str(self.__timeLimit) + 'more seconds')
        # BAD routing
        if type(route) == str:
            if route.isdigit():
                route = int(route)
        self.__camRoute = route
        self.__generator = None
        self.__finished = False
        self._lastAskTime = None
        self._image = None
        self._isRan = False
        
        self.__deleted = False
        
    
    def isDeleted(self):
        return self.__deleted
    
    def getParams(self):
        return [self.__camRoute, self._lastAskTime, self.__finished, self._streaming]
    
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
            if self._streaming == None:
                print('connecting', self.__camRoute)
                # print('ppid', os.getpid())
                connectionThread = Stream.ThreadConnector(self.__camRoute)
                connectionThread.start()
                connectionThread.join(timeout=10)
                if not connectionThread.result:
                    connectionThread.stop()
                    raise Exception(self.__camRoute, 'connection timeout exception')
                self._streaming = connectionThread.result
                
                # print('time of initing videocapture is', time() - b)
                # print('getting stream resilt', self._streaming)
                
        except Exception as e:
            self._streaming = None
            # print('time of initing videocapture is', time() - b)
            raise Exception('Can not capture the video', type(e), e)
    
    def _release(self):
        print('releasing', threading.currentThread().ident)
        self.getterThread.stop()
        sleep(0.1)
        if self._streaming != None:
            try:
                self._streaming.release()
            except:
                print('not released')
            
            
            # try:
            #     self.getterThread.terminate()
            #     self.getterThread.kill()
            #     self.getterThread.close()
            # except Exception as e:
            #     print('closing thread exception', e)
            
            # self.getterThread.stop()
            
    
    def getId(self):
        return threading.currentThread().ident
    
    def init(self):
        self._connect()
        self.__finished = False
        self.__lastAskTime = time()
        
        self.getterThread = StopableThread(target=self.__updateFrame, args=(), looped=True)
        self.getterThread.start()
        print('initing', threading.currentThread().ident)
        
        # self.getterThread = multiprocessing.Process(target=self.__updateFrame)
        # self.getterThread.start()
        
        # self.getterThread = self.ThreadReader(target=self)
        # self.getterThread.start()
        
        for _ in range(10):
            sleep(0.4)
            if self._isRan:
                break
        self.__generator = self.__getFrames()

    def __updateFrame(self):
        # while not self._checkDelete(): #TODO: test
            try:
                if not self._checkDelete():
                        
                    result, frame = self._streaming.read()
                    if result:
                        self._image = frame
                        self._isRan = True
                    else:
                        self._release()
                else:
                    sleep(1)
            except Exception as e:
                print('test', e)
            
            
    def getStream(self):
        return self.__generator
    
    def __getFrames(self):
        if self._streaming == None:
            raise Exception('First try to connect the camera')
        while not self._checkDelete():
            if not self.__finished:
                try:
                    if self._image is None:
                        yield None
                    else:
                        yield self._image
                except Exception as e:
                    raise e

    
    #TODO: bug
    def _resetTime(self, newTime):
        if newTime + time() > self.__timeLimit + self.__lastAskTime:
            print(f'stream {threading.currentThread().ident} of', self.__camRoute, 'reseting time')
            self.__timeLimit = newTime
            self.__finished = False
            self.__lastAskTime = time()
            
            print('reseting: adding ' + str(newTime) + ' more seconds')
        
    def _checkFinished(self):
            if self.__timeLimit < time() - self.__lastAskTime:
                self.__finished = True
                return True
            return False
    
    def _checkDelete(self):
        if self._checkFinished():
            if self.__timeLimit + self.__deleteTime < time() - self.__lastAskTime:
                print(f'stream {threading.currentThread().ident} of', self.__camRoute, 'rest time is', time() - self.__lastAskTime - self.__timeLimit - self.__deleteTime, self.__timeLimit + self.__deleteTime < time() - self.__lastAskTime )
                self._release()
                self.__deleted = True
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
            
        

        
            
    # class ThreadReader(threading.Thread):
        
    #     def __init__(self, target):
    #         threading.Thread.__init__(self)
    #         self.event = threading.Event()
    #         self.target = target
            
        
    #     def run(self):
    #         # print(threading.currentThread().ident)
    #         self.pid = os.getpid() 
    #         try:
    #             try:
    #                 while self.target._checkDelete():
    #                     if self.event.is_set():
    #                         print('stoped')
    #                         return
    #                     result, frame = self.target._streaming.read()
    #                     if result:
    #                         self.target._image = frame
    #                         self.target._isRan = True
    #             except Exception as e:
    #                 print(e)
    #         except:
    #             return
                
        
    #     def stop(self):
    #         self.event.set()