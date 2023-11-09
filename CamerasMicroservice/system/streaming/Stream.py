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
from system.streaming.StreamBase import StreamBase
    
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
        
        self.__needStop = False
        
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
        try:
            if self._streaming == None:
                print('connecting', self.__camRoute)
                # print('ppid', os.getpid())
                try:
                    camera = cv2.VideoCapture()
                    camera.setExceptionMode(True)
                    camera.open(self.__camRoute)
                except:
                    try:
                        camera.close()
                    except Exception as e:
                        print('close in connectiong error', e)
                    raise Exception(self.__camRoute, 'connection timeout exception')
                
                self._streaming = camera
                
        except Exception as e:
            self._streaming = None
            raise Exception('Can not capture the video', type(e), e)
    
    def _release(self):
        print('releasing', self.__cameraRoute)
        self.getterThread.stop()
        sleep(0.1)
        if self._streaming != None:
            try:
                self._streaming.release()
                StreamBase._removeStream(self)         # check it
                print('releasing', self.__cameraRoute, 'done')
                self._streaming = None
            except:
                print('releasing', self.__cameraRoute, 'error')
            
            '''
            # try:
            #     self.getterThread.terminate()
            #     self.getterThread.kill()
            #     self.getterThread.close()
            # except Exception as e:
            #     print('closing thread exception', e)
            
            # self.getterThread.stop()
            '''
            
            
    
    def getId(self):
        return threading.currentThread().ident
    
    def init(self):
        self._connect()
        self.__finished = False
        self.__lastAskTime = time()
        
        self.getterThread = StopableThread(target=self.__updateFrame, args=(), looped=True)
        self.getterThread.start()

        
        for _ in range(10):
            sleep(0.4)
            if self._isRan:
                break
        self.__generator = self.__getFrames()

    def __updateFrame(self):
        # while not self._checkDelete(): #TODO: test
            try:
                if not self.__needStop and self.streaming:
                    if not self._checkDelete():
                        
                        result, frame = self._streaming.read()
                        if result:
                            self._image = frame
                            self._isRan = True
                        else:
                            self._release()
                            self.__needStop = True
                    else:
                        self._release()
                else:
                    sleep(0.2)
            except Exception as e:
                self._release()
                print('test', e)
            
            
    def getStream(self):
        return self.__generator
    
    def __getFrames(self):
        if self._streaming == None:
            raise Exception('First try to connect the camera')
        while True:                                                # check it
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
        
            
    # class ThreadConnector(threading.Thread):
        
    #     def __init__(self, route):
    #         threading.Thread.__init__(self)
    #         self.route = route
    #         self.result = None
    #         self.pid = None
        
    #     def run(self):
    #         # print(threading.currentThread().ident)
    #         self.pid = os.getpid() 
    #         try:
    #             camera = cv2.VideoCapture()
    #             camera.setExceptionMode(True)
    #             camera.open(self.route)
    #             self.result = camera
    #         except:
    #             try:
    #                 camera.close()
    #                 try:
    #                     self.result.close()
    #                 except:
    #                     pass
    #             except:
    #                 pass
                
        
    #     def stop(self):
    #         raise Exception('timeout')
            
        

        
            
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