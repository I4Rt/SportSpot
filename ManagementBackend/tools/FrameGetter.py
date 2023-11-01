from __future__ import annotations
import requests
from tools.FileUtil import FileUtil
from time import sleep

from datetime import datetime
import cv2

class FrameGetter:
    @classmethod
    def initStream(cls, route, duration):
        r = requests.get(url='http://127.0.0.1:5002/initVideo', params={'route':route, 'duration': duration})
        return r.json()['init']
    
    @classmethod
    def refreshStream(cls, route, duration):
        r = requests.get(url='http://127.0.0.1:5002/refreshVideo', params={'route':route, 'duration': duration})
        data = r.json()
        print(data)
        return data['refresh']
    
    @classmethod
    def getFrame(cls, route):
        print("getting frame")
        r = requests.get(url='http://127.0.0.1:5002/getFrame', params={'route':route})
        frame = r.json()['frame']
        try:
            img = FileUtil.convertBytesToImg(frame)
            
            # with open('statistics.txt', 'a') as f:
            #     f.write(str(datetime.now()) + f' getting from {route} result: True\n' )
        except:
            # with open('statistics.txt', 'a') as f:
            #     f.write(str(datetime.now()) + f' getting from {route} result: False\n' )
            img = None
        return img
    
    @classmethod
    def getStream(cls, route, duration):
        if FrameGetter.initStream(route, duration):
            frame = FrameGetter.getFrame(route)

            while frame is not None:
                print('here')
                yield frame
                sleep(1)
                frame = FrameGetter.getFrame(route)
            return None
        return None
        