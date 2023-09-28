from __future__ import annotations
import requests
from tools.FileUtil import FileUtil
from time import sleep

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
        # print("getting frame")
        r = requests.get(url='http://127.0.0.1:5002/getFrame', params={'route':route})
        frame = r.json()['frame']
        img = FileUtil.convertBytesToImg(frame)
        ret, jpeg = cv2.imencode('.jpg', img)
        bytesData = jpeg.tobytes()
        return bytesData
    
    @classmethod
    def getStream(cls, route, duration):
        if FrameGetter.initStream(route, duration):
            frame = FrameGetter.getFrame(route)
            # print(f'frame is {frame}')
            while frame != 'None':
                # print('here')
                yield (b'--frame\r\n'
                                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                sleep(1)
                frame = FrameGetter.getFrame(route)
        