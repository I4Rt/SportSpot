from __future__ import annotations

from time import time, sleep
import cv2
import threading
from tools.FileUtil import *

from tools.Jsonifyer import Jsonifyer
from system.streaming.StopableThread import StopableThread

class StreamBase:
    __initialized:bool = False
    __streams = []
    __readyStreamsList = []
    __queue = []
    __needContinue = True
    __thread = None
    __index = 0
    
    @classmethod
    def appendToQueue(cls, route, timeLimit):
        try:
            
            id = f'{threading.currentThread().ident}_{time()%10000}'
            
            data = {'route':route, 'timeLimit': int(timeLimit), 'id': id} #  may be float
            cls.__queue.append(data)
            print('got to queue', id)
            return id
        except:
            return None
        
    @classmethod
    def checkCreated(cls, ident):
        if ident in cls.__readyStreamsList:
            return True
        return False
    
    
    @classmethod
    def releaseQueue(cls):
        try:
            needPrint = len(cls.__queue) > 0
            if needPrint:
                print('queue before:', cls.__queue)
            
            data = cls.__queue.pop(0)
            cls.initStream(data['route'], data['timeLimit'])
            cls.__readyStreamsList.append(data['id'])
            cls.__readyStreamsList = cls.__readyStreamsList[-400:]
            if needPrint:
                print('queue after:', cls.__queue)
            
        except IndexError:
            pass
        except Exception as e:
            print('queue exception is', e)
    
    @classmethod
    def init(cls):
        cls.__thread = StopableThread(target=cls.releaseQueue, looped=True)
        cls.__thread.start()
        cls.__initialized = True
            
        
    @classmethod
    def _getStreams(cls):
        for stream in cls.__streams:
            if stream._checkDelete():
                print('p1 deleting', stream.getId())
                cls.__streams.remove(stream)
        
        return cls.__streams
    
    @classmethod
    def _addStream(cls, stream:Stream):
        # if cls.__initialized:
        cls.__streams.append(stream)
        # print('inited')
        return True
        
        
    @classmethod
    def _removeStream(cls, stream:Stream):
        try:
            cls.__streams.remove(stream)
        except Exception as e: 
            print('can not remove by streamBase._removeStream', e)
    
    

        
    @classmethod
    def initStream(cls, route, timeLimit):
        # found = False
        for stream in cls.__streams:                   # exist
            if stream.getRoute() == route:             # found
                # found = True
                if not stream._checkFinished():        # not finished
                    print('refreshing time on init')
                    stream._resetTime(timeLimit)       # refresh    
                    return stream
                else:                                  # exist but finished
                    try:
                        stream._release()              # stopping old one
                        # cls.__streams.remove(stream)   # remove from queue
                    except Exception as e:
                        print('deleting stream in interval failed', e)
                    break
        # if not found:
        sleep(0.5)                                 # wait to make shure it has been stopped
            
        stream = Stream(route, timeLimit)              # new stream
        stream.init()                                  # init new stream
        
        cls._addStream(stream)                 # add stream to queue
        print('after init array is', cls.__streams)
        return stream                                  # return the link to stream
        
    
    @classmethod
    def refreshStream(cls, route, newTime):
        for stream in cls.__streams:
            if not stream._checkFinished() and str(stream.getRoute()) == str(route):
                print('refreshing time on refresh') 
                stream._resetTime(newTime)
                return True
        return False

    # @classmethod
    # def __checkStreams(cls):
    #     while cls.__needContinue:
    #         sleep(2)
    #         if len(cls.__streams) > 0:
    #             print('threads lenght is', len(cls.__streams), [s.getRoute() for s in cls.__streams])
    #             for stream in cls.__streams:
    #                 if stream._checkDelete():
    #                     print('p1 deleting', stream.getId())
    #                     # stream._release()                                   # TODO: check if ness
    #                     try:
    #                         cls.__streams.remove(stream)
    #                     except:
    #                         pass
    #                     # routes = [s.getRoute() for s in cls.__streams]
    #                     # stilContain = stream.getRoute() in routes
    #                     # if stilContain:
    #                     #     with open('StreamQueue.txt', 'a') as f:
    #                     #         f.write(f'{datetime.now()}\nremoved: {stream.getRoute()}\nroute now is: {routes}\n\n')
    #                     print('removing thread', stream.getRoute())
    #                     # del stream
                        
    
    # @classmethod
    # def init(cls):
    #     if cls.__thread:
    #         # try:
    #         #     cls.__initialized = False
    #         #     cls.__needContinue = False
    #         #     cls.__thread.join()
    #         # except:
    #         #     pass
    #     cls.__needContinue = True
    #     # cls.__thread = Thread(target=cls.__checkStreams)
    #     # cls.__thread.start()
    #     cls.__initialized = True




    
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
                        camera.release()
                        
                    except Exception as e:
                        print('close in connectiong error', e)
                    raise Exception(self.__camRoute, 'connection timeout exception')
                
                self._streaming = camera
                
        except Exception as e:
            self._streaming = None
            raise Exception('Can not capture the video', type(e), e)
    
    def _release(self):
        print('releasing', self.__camRoute)
        self.getterThread.stop()
        sleep(0.1)
        if self._streaming:
            try:
                self._streaming.release()
                StreamBase._removeStream(self)         # check it
                print('releasing', self.__camRoute, 'done')
                self._streaming = None
            except Exception as e:
                print('releasing', self.__camRoute, 'error', e)
            
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
                if not self.__needStop and self._streaming:
                    if not self._streaming.isOpened():
                        self.__needStop = True
                        return
                    if not self._checkDelete():
                        
                        result, frame = self._streaming.read()
                        if result:
                            self._image = frame
                            self._isRan = True
                        else:
                            self._release()
                            self.__needStop = True
                    else:
                        print('releasing p1')
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