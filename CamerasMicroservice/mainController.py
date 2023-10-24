from flask import jsonify, render_template, flash, redirect, url_for, make_response, Response
from config import *

import json

import cv2

from system.streaming.Stream import Stream
from system.streaming.StreamInterface import StreamInterface

from datetime import datetime
from random import randint
from tools.FileUtil import *

from tools.LastTimeRunnerHolder import LastTimeRunnerHolder as ltrh


@cross_origin
@app.route('/getFrame')
def getFrame():
    ltrh.setLastTime(datetime.now())
    try:
        route = request.args.get('route')
    except:
        return json.dumps({"frame":None, 'answer': 'Add params correctly'})
    try:
        frame = StreamInterface.getFrame(route)
        imgBytes = FileUtil.convertImageToBytes(frame)
        return json.dumps({"route": route, "frame": imgBytes})
    except:
        return json.dumps({"route": route, "frame": None})

                    
    
@cross_origin
@app.route('/refreshVideo')
def refreshVideo():
    ltrh.setLastTime(datetime.now())
    try:
        route = request.args.get('route')
        duration = float(request.args.get('duration'))
        result = StreamInterface.refreshStream(route, duration)
        return json.dumps({'refresh': result})
    except:
        return json.dumps({'refresh': False, 'answer': 'Add params correctly'})

@cross_origin
@app.route('/initVideo')
def initVideo():
    ltrh.setLastTime(datetime.now())
    print('got fetch')
    try:
        b = time()
        route = request.args.get('route')
        duration = int(request.args.get('duration'))
        StreamInterface.initStream(route, duration)
    except Exception as e:
        print('Exception is ' + str(e))
        print('work t', time() - b)
        return json.dumps({'init': False, 'answer':'Add params correctly'})
    print('work t', time() - b)
    return json.dumps({'init': True})
    
