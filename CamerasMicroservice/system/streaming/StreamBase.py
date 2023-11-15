from __future__ import annotations

from time import time, sleep
import cv2
import threading
from tools.FileUtil import *

from tools.Jsonifyer import Jsonifyer
from system.streaming.StopableThread import StopableThread
import gc

class StreamBase:
    __initialized:bool = False
    __streams : list[Stream] = []
    __readyStreamsList = []
    __queue = []

    __thread = None

    
    @classmethod
    def appendToQueue(cls, route, timeLimit):
        id = f'{threading.currentThread().ident}_{time()%10000}'
        cls.__queue.append([route, timeLimit, id])
        return id
        
        
    @classmethod
    def checkCreated(cls, ident):
        return ident in cls.__readyStreamsList
    
    
    @classmethod
    def releaseQueues(cls):
        i = 0
        while i < len(cls.__streams):
            if cls.__streams[i].isFinished():
                try:
                    cls.__streams[i]._release()
                except Exception as e:
                    print('err0r', e)
                del cls.__streams[i]
            else:
                i += 1
        # if len(cls.__streams) > 0:
        #     print(cls.__streams)
        try:
            data = cls.__queue.pop(0)
            res = cls.initStream(data[0], data[1], data[2])
            if res:
                cls.__readyStreamsList.append(res)
                cls.__readyStreamsList = cls.__readyStreamsList[-400:]
        except IndexError:
            pass
        except Exception as e:
            print('releasing queue error:', e)
        finally:
            sleep(0.2)
            
        
                    
    @classmethod
    def init(cls):
        cls.__thread = StopableThread(target=cls.releaseQueues, looped=True)
        cls.__thread.start()
        cls.__initialized = True
        
    @classmethod
    def initStream(cls, route, timeLimit, initing_id=f'{time()}'):
        
        for i in range(len(cls.__streams)):
            if str(cls.__streams[i].getRoute()) == str(route):
                if not cls.__streams[i].isFinished():
                    try:
                        cls.__streams[i]._resetTime(timeLimit)
                        cls.__streams[i].setNewId(initing_id)
                        return cls.__streams[i].getId()
                    except Exception as e:
                        print('break on ', e)
                        break
    
        cls.__streams.append(Stream(route, timeLimit, initing_id))
        
        return initing_id
    
    @classmethod
    def refreshStream(cls, route, newTime):
        for i in range(len(cls.__streams)):
            if str(cls.__streams[i].getRoute()) == route:
                cls.__streams[i]._resetTime(newTime)
                return True
        return False
                   
    '''
        не безопасная ссылка на объект по индексу, длина списка может измениться
    '''
    @classmethod
    def getNext(cls, route):
        try:
            for i in range(len(cls.__streams)):
                if not cls.__streams[i].isFinished() and str(cls.__streams[i].getRoute()) == str(route):
                    return next(cls.__streams[i].getStream())
            return None
        except:
            print('can not get frame from generator exception')
            return None





    
class Stream(Jsonifyer):
    
    
    __camRoute:str|int = 0
    _streaming:cv2.VideoCapture | None = None
    __timeLimit = 120
    __deleteTime = 1
    def __init__(self, route:str, timeLimit = 120, id=f'{time()}'):
        Jsonifyer.__init__(self)
        self.__timeLimit = timeLimit
        # print('initing: adding ' + str(self.__timeLimit) + 'more seconds')
        # BAD routing
        self.__id = id
        if type(route) == str:
            if route.isdigit():
                route = int(route)
        self.__camRoute = route
        self.__generator = None
        self.__finished = False
        self.__lastAskTime = None
        self._image = None
        
        self.__deleted = False
        self.getterThread = None
        self.init()                           # TODO: check it
        
    
    def isDeleted(self):
        return self.__deleted
    
    def isFinished(self):
        return self.__finished    

    def setNewId(self, newId):
        self.__id = newId
        
    def getRoute(self):
        return self.__camRoute    
    
    def getId(self):
        return self.__id

    
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
    
    def _release(self):
        print('releasing')
        self.finished = True
        
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
        self.__deleted = True
        
    def init(self):
        try:
            self._connect()
        except:
            return False
        self.__lastAskTime = time()
        self.getterThread = StopableThread(target=self.__updateFrame, looped=True)
        self.getterThread.start()
        sleep(0.5)
        self.__generator = self.__getFrames()
        return True
        
        
    '''добавить попытку получения первых кадров'''
    def __updateFrame(self):
        # while not self._checkDelete(): #TODO: test
        
        try:
            if self._streaming:
                if not self._checkDelete():
                    result, frame = self._streaming.read()
                    if result:
                        self._image = frame
                        sleep(0.5)
                        return
            # self._release()
            sleep(0.5)
            return
        except Exception as e:
            # self._release()
            sleep(0.5)
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
            # print(f'stream {threading.currentThread().ident} of', self.__camRoute, 'reseting time')
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
                return True
            return False
        return False
    
    def __del__(self):
        try:
            self._release()
        except: 
            pass
        print("deleted stream object", self.getId())