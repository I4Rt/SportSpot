from __future__ import annotations
from time import time, sleep
import cv2
import threading, multiprocessing
from tools.FileUtil import *
import config
import os
import sys
import signal
from datetime import datetime


from tools.Jsonifyer import Jsonifyer

from system.streaming.StopableThread import StopableThread


class PermanentStreamer(Jsonifyer):
    
    # route : stream
    __streams:dict[str, Stream] = {}
    __queue:list[dict] = []
    __readyStreamsList = []
    __stopped = False
    __startTime = None
    __timeLimit = None
    
    @classmethod
    def init(cls, startTime = time(), timeLimit = 4 * 60 * 60):
        cls.__startTime = startTime
        cls.__timeLimit = timeLimit
        cls.__stopped = False
        
        cls.__thread = StopableThread(target=cls.releaseQueues, looped=True)
        cls.__thread.start()
        
    
    
    @classmethod
    def appendToQueue(cls, route, timeLimit):
        id = f'{threading.currentThread().ident}_{time()%10000}'
        cls.__queue.append({id:route})
        return id
        
        
    @classmethod
    def checkCreated(cls, ident):
        for res in cls.__readyStreamsList:
            if res[0] == ident:
                return res[1]
        return None
    
    
    @classmethod
    def releaseQueues(cls):
        
        # for key in cls.__streams:
        #     if not 0 < cls.__streams[key].getTimeSinceUpdateFrom() < 10:
        #         del cls.__streams[key]
        if not cls.__stopped:
            if time() - cls.__startTime > cls.__timeLimit - 30:
                cls.__thread.stop()
                cls.__thread.join()
                cls.__stopped = True
                pass
            try:
                if len(cls.__queue):
                    print(len(cls.__queue), cls.__queue)
                id, route = list(cls.__queue.pop(0).items())[0] # [id, route]
                res = cls.initStream(route)
                cls.__readyStreamsList.append([id, res])
                cls.__readyStreamsList = cls.__readyStreamsList[-400:]
            except IndexError:
                pass
            except Exception as e:
                print('releasing queue error:', e)
            finally:
                sleep(0.2)
        else:
            sleep(0.2)
    
    # must be single executed  (from queue only)
    @classmethod
    def initStream(cls, route):
        
        if str(route) in list(cls.__streams.keys()):
            if 0 < cls.__streams[str(route)].getTimeSinceUpdateFrom() < 10:
                return True
            del cls.__streams[str(route)]

        stream = Stream(str(route))
        if stream.init():
            cls.__streams[route] = stream
            return True
        return False
        
    @classmethod
    def getNext(cls, route):
        try:
            if str(route) in list(cls.__streams.keys()):
                if 0 < cls.__streams[str(route)].getTimeSinceUpdateFrom() < 10:
                    return next(cls.__streams[str(route)].getStream())
            return None
        except:
            print('can not get frame from generator exception')
            return None
        
            
        
    @classmethod
    def refreshStream(cls, route):
        ident = cls.appendToQueue(route)
        
        for i in range(900):       # 3 min
            res = cls.checkCreated(ident)
            if type(res) == bool:
                return res
            sleep(0.2)
        return False
        
        

class Stream(Jsonifyer):
    
    __camRoute:str|int = 0
    _streaming:cv2.VideoCapture | None = None

    def __init__(self, route:str):
        Jsonifyer.__init__(self)
        # print('initing: adding ' + str(self.__timeLimit) + 'more seconds')
        # BAD routing
        if type(route) == str:
            if route.isdigit():
                route = int(route)
        self.__camRoute = route
        self.__generator = None
        self.__lastTime = None
        self._image = None
        
        self.getterThread = None
        # self.init()                           # TODO: check it
    

    def getTimeSinceUpdateFrom(self):
        if self.__lastTime:
            return (datetime.now() - self.__lastTime).total_seconds()
        return -1
    
    
        
    def init(self):
        try:
            self._connect()
        except:
            return False
        self.getterThread = StopableThread(target=self.__updateFrame, looped=True)
        self.getterThread.start()
        sleep(0.5)
        self.__generator = self.__getFrames()
        return True
    
    def _connect(self):
        try:
            if self._streaming == None:
                print('connecting', self.__camRoute)
                # print('ppid', os.getpid())
                self._streaming = cv2.VideoCapture(self.__camRoute)
        except Exception as e:
            try:
                self._release()
            except Exception as e:
                print('bad initing exception release:', e)
            raise Exception('Can not capture the video', type(e), e)
        
    '''добавить попытку получения первых кадров'''
    def __updateFrame(self):
        # while not self._checkDelete(): #TODO: test
        try:
            if self._streaming:
                
                result, frame = self._streaming.read()
                if result:
                    self.__lastTime = datetime.now()
                    self._image = frame
                    sleep(0.5)
                    return
            sleep(0.5)
            return
        except Exception as e:
            sleep(0.5)
            print('test', e)
            
            
    def __getFrames(self):
        if self._streaming == None:
            raise Exception('First try to connect the camera')
        while True:                                                # check it
            try:
                if self._image is None:
                    # print('image is none')
                    yield None
                else:
                    # print('image exist', self._image)
                    yield self._image
            except Exception as e:
                raise e    
                 
    def getStream(self):
        return self.__generator
        
    def _release(self):
        print('releasing')
        
        try:
            self.getterThread.stop()
            sleep(1)
            try:
                self.getterThread.join()
            except Exception as e:
                print('r1', e)
            sleep(0.5)
            del self.getterThread
            print('thread deleted')
        except Exception as e:
            print('release delete thread exception', e)
        try:
            del self._image
            print('image deleted')
        except Exception as e:
            print('release delete image exception', e)
        try:
            self._streaming.release()
            del self._streaming
        except Exception as e:
            print('releasing streaming exception', e)
            
    def __del__(self):
        try:
            self._release()
        except: 
            pass
        print("deleted stream object", self.getId())