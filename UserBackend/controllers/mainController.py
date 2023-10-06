from flask import jsonify, render_template, flash, redirect, url_for, make_response, Response
from config import *
from tools.jwtHolder import *
from model.data.TestTable import *
from model.system.User import *
from flask_jwt_extended import *
import json

from model.data.Sector import Sector
from model.data.Camera import Camera 
from model.data.Room import Room
from model.data.types.RoomType import RoomType
from model.data.types.SectorType import SectorType
from model.data.Task import Task

from tools.TaskArchiveRunner import TaskArchiveRunner
import os

# from system.streaming.Stream import Stream
# from system.streaming.StreamInterface import StreamInterface

from tools.FrameGetter import *

# import time
from datetime import datetime


from system.DataHodler import *
from random import randint
# import cv2

# def authorize(foo):
#     def inner(*args,**kwargs):
#         verify_jwt_in_request()
#     identy = get_jwt_identity()
#         if identy:
#             foo(*args,**kwargs)
#         else:
#             resp = make_response({'answer': "Bad token"})
#             resp.headers['Content-Type'] = "application/json"
#             return resp
#     return inner


DataHolder.getInstance().setParam("cameraNumber", 60)
DataHolder.getInstance().setParam("roomNumber", 15)

@cross_origin
@app.route('/register', methods=['get', 'post'])
def register():
    try:
        name = request.json['name']
        surname = request.json['surname']
        login = request.json['login']
        password = request.json['password']
        
    except Exception as e:
        resp = make_response({'answer': 'Invalid json'})
        
    passwordHash = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(name, surname, login, passwordHash)
    try:
        user.save()
        resp = make_response({'register': True})
        resp.headers['Content-Type'] = "application/json"
        return resp
    except:
        resp = make_response({'answer': "Not identy login"})
        resp.headers['Content-Type'] = "application/json"
        return resp


@cross_origin
@app.route('/setUserData', methods=['get', 'post'])
def setUserData():
    try:
        id = request.json['id']
        name = request.json['name']
        surname = request.json['surname']
        password = request.json['password']
        
    except Exception as e:
        resp = make_response({'answer': 'Invalid json'})
        
    passwordHash = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User.getByID(int(id))
    try:
        user.name = name
        user.surname = surname
        user.password = passwordHash
        user.save()
        resp = make_response({'setUserData': True})
        resp.headers['Content-Type'] = "application/json"
        return resp
    except:
        resp = make_response({'answer': "Not identy login"})
        resp.headers['Content-Type'] = "application/json"
        return resp
# auth
@cross_origin()
@app.route('/authorize', methods=['get', 'post',])
def authorize():
    login = request.json['login']
    password = request.json['password']
    print(User.getByName(login))
    users = User.getByName(login)
    if len(users) > 0:
        if bcrypt.check_password_hash(users[0].password, password):
            access_token = create_access_token(identity=users[0].id, fresh=True)
            refresh_token = create_refresh_token(users[0].id)
            resp = jsonify({'login': True})
            resp.set_cookie('access_token_cookie', access_token, secure=True,  samesite='None')
            resp.set_cookie('refresh_token_cookie', refresh_token, secure=True, samesite='None')
            return resp, 200
    resp = jsonify({'login': False})
    return resp, 200

@cross_origin()
@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    if identity:
        access_token = create_access_token(identity=identity, fresh=True)
        # set_access_cookies(resp, access_token)
        resp = jsonify({'refresh': True})
        set_access_cookies(resp, access_token)
        return resp, 200
    return jsonify({'refresh': False}), 200

@cross_origin()
@app.route('/logout', methods=['GET'])
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200

@cross_origin()
@app.route('/testJWT', methods=['GET','POST'])
@jwt_required()
def testJWT():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    return jsonify({'hello': 'from {}'.format(identy)}), 200

@cross_origin()
@app.route('/getUserInfo')
@jwt_required()
def getUser():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        user = User.getByID(identy)
        return user.getParamsList(exceptions=['password', 'login']), 200
    else:
        return {'answer': 'No such user'}
    
'''
getCameras
getCameraByID
getSectorsByCameraID
getSectorByID
getSectorTypes
getRooms
getRoomByID
getCameraSectorsByRoomId
getUnusedCameraSectorsByRoomId


setSectorToRoom
removeSectorFromRoomLsit

POST
setCamera
setRoom
setSector
{camId, sectorParams}

GET
deleteCamera
deleteRoom
deleteSector
'''

# getters
@cross_origin
@jwt_required()
@app.route('/getCameras', methods=['get', 'post'])
def getCameras():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        data = []
        cams = Camera.getAll()
        for cam in cams:
            data.append(cam.getParamsList())
        resp = make_response(data)
        resp.headers['Content-Type'] = "application/json"
        return resp
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp
    
@cross_origin
@jwt_required()
@app.route('/getCameraByID', methods=['get', 'post'])
def getCameraByID():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        try:
            camera = Camera.getByID(request.args.get('id'))
            data = camera.getParamsList()
        except Exception:
            data = {"answer": "No such ID"}
        resp = make_response(data)
        resp.headers['Content-Type'] = "application/json"
        return resp
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp
    
@cross_origin
@jwt_required()
@app.route('/getSectorsByCameraID', methods=['get', 'post'])
def getSectorsByCameraID():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        try:
            objectiveData = Camera.getSectorsById(request.args.get('id'))
            data = []
            for obj in objectiveData:
                params = obj.getParamsList()
                params["points"] = obj.getPointList()
                data.append(params)
        except Exception: 
            data = {"answer": "No such ID"}
        resp = make_response(data)
        resp.headers['Content-Type'] = "application/json"
        return resp
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp

@cross_origin
@jwt_required()
@app.route('/getSectorByID', methods=['get', 'post'])
def getSectorByID():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        try:
            sector = Sector.getByID(request.args.get('id'))
            data = sector.getParamsList()
            data["points"] = sector.getPointList()
            data["type"] = sector.getSectorType().getParamsList()
        except Exception:
            data = {"answer": "No such ID"}
        resp = make_response(data)
        resp.headers['Content-Type'] = "application/json"
        return resp
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp

@cross_origin
@jwt_required()
@app.route('/getSectorTypes', methods=['get', 'post'])
def getSectorTypes():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        objectiveData = SectorType.getAll()
        data = []
        for obj in objectiveData:
            data.append(obj.getParamsList())
        return data
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp
    
@cross_origin
@jwt_required()
@app.route('/getRooms', methods=['get', 'post'])
def getRooms():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    print(identy)
    if identy:
        objectiveData = Room.getAll()
        data = []
        for obj in objectiveData:
            dataList = obj.getParamsList()
            dataList['roomType'] = RoomType.getByID(dataList["classId"]).getParamsList()
            data.append(dataList)
        resp = make_response(data)
        resp.headers['Content-Type'] = "application/json"
        return resp
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp


@cross_origin()
@jwt_required()
@app.route('/getTasks', methods=['get', 'post'])
def getTasks():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        try:
            date = datetime.strptime(request.json['date'], '%m/%d/%Y')
        except Exception as e:
            return make_response({'answer': str(e)})
        objectiveData = Task.getTasksAtDay(date)
        print('got Tasks len is ', len(objectiveData))
        data = []
        for obj in objectiveData:
            dataList = obj.getParamsList()
            dataList['statistics'] = obj.getCount()
            data.append(dataList)
        resp = make_response(data)
        resp.headers['Content-Type'] = "application/json"
        return resp
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp

@cross_origin
@jwt_required()
@app.route('/getRoomByID', methods=['get', 'post'])
def getRoomByID():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        try:
            room = Room.getByID(request.args.get('id'))
            data = room.getParamsList()
            data["sectors"] = []
            for sector in room.getSectors():
                sectorInfo = sector.getParamsList()
                sectorInfo["points"] = sector.getPointList()
                sectorInfo["type"] = sector.getSectorType().getParamsList()
                data["sectors"].append(sectorInfo)
        except Exception:
            data = {"answer": "No such ID"}
        resp = make_response(data)
        resp.headers['Content-Type'] = "application/json"
        return resp
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp
    
@cross_origin
@jwt_required()
@app.route('/getCameraSectorsByRoomId', methods=['get', 'post'])
def getCameraSectorsByRoomId():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        room = Room.getByID(request.args.get('roomId'))
        if room != None:
            data = room.getParamsList()
            camerasObj = room.getCameras()
            cameras = []
            for cam in camerasObj:
                curCamera = cam.getParamsList()
                curCamera["sectors"] = []
                cameras.append(curCamera)
            for sector in room.getSectors():
                sectorInfo = sector.getParamsList()
                sectorInfo["points"] = sector.getPointList()
                sectorInfo["sectorType"] = sector.getSectorType().getParamsList()["name"]
                for cam in cameras:
                    if cam["id"] == sectorInfo["camId"]:
                        cam["sectors"].append(sectorInfo)
            data["camerasList"] = cameras
        else:
            data = {"answer": "No such room"}
        resp = make_response(data)
        resp.headers['Content-Type'] = "application/json"
        return resp
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp

@cross_origin
@jwt_required()
@app.route('/getUnusedCameraSectorsByRoomId', methods=['get', 'post'])
def getUnusedCameraSectorsByRoomId():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        data = 'error'
        try:
            rId = request.args.get('roomId')
            unusedSectors = Sector.getUnusedSectors(rId)
            exist = []
            data = []
            print(f'i found {len(unusedSectors)} sectors')
            for sec in unusedSectors:
                # print(sec)
                #print(sec)
                camera = Camera.getByID(sec.camId)
                if camera != None:
                    # print("camera for sector is found")
                    if not (camera.id in exist):
                        # print(cam)
                        exist.append(camera.id)
                        camParams = camera.getParamsList()
                        camParams["sectors"] = []
                        data.append(camParams)
                    sectorInfo = sec.getParamsList()
                    sectorInfo["points"] = sec.getPointList()
                    sectorInfo["sectorType"] = sec.getSectorType().getParamsList()["name"]
                    #print('Info: ' + str(sectorInfo))
                    for cam in data:
                        if cam['id'] == sec.camId:
                            cam["sectors"].append(sectorInfo)
                    # print(data)
                # else:
                    # sec.remove()
                    # print(camera)
                # print(exist)
            resp = make_response({'camerasList': data})
        except Exception as e:
            resp = make_response({'answer': data})
            print(e)
        resp.headers['Content-Type'] = "application/json"
        return resp
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp

@cross_origin
@jwt_required
@app.route('/getRoomTypes', methods=['get'])
def getRoomTypes():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        return make_response({'types': [tp.getParamsList() for tp in RoomType.getAll()]})
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp

# set/remove complex data
@cross_origin
@jwt_required()
@app.route('/setSectorToRoom', methods=['get', 'post'])
def setSectorToRoom():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        code = 200
        data = {'OperationStatus': 'Done'}
        try:
            sector = Sector.getByID(request.args.get('sectorId'))
            sector.roomId = request.args.get('roomId')
            sector.save()
        except Exception:
            data = {"answer": "No such ID"}
            code = 500
        resp = make_response(data)
        resp.headers['Content-Type'] = "application/json"
        resp.status_code = code
        return resp
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp

@cross_origin
@jwt_required()
@app.route('/removeSectorFromRoomLsit', methods=['get'])
def removeSectorFromRoomLsit():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        code = 200
        data = {'OperationStatus': 'Done'}
        try:
            sector = Sector.getByID(request.args.get('sectorId'))
            sector.roomId = None
            sector.save()
        except Exception:
            data = {"answer": "No such ID"}
            code = 500
        resp = make_response(data)
        resp.headers['Content-Type'] = "application/json"
        resp.status_code = code
        return resp
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp
    
# create
@cross_origin
@jwt_required()

@app.route('/setCamera', methods=['get', 'post'])
def setCamera():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        code = 200
        data = {'OperationStatus': 'Done'}
        try:
            id = request.json['id']
            name = request.json['name']
            ip = request.json['ip']
            port = request.json['port']
            chanel = request.json['chanel']
            codec = request.json['codec']
            login = request.json['login']
            password = request.json['password']
            fullRoute = request.json['fullRoute']
        except Exception as e:
            return make_response({'answer': str(e)})
        camera = None
        if id == None:
            camera = Camera(name,ip,port,chanel,codec,login,password, fullRoute)
        else:
            camera = Camera.getByID(id)
            if camera is not None:
                camera.name = name
                camera.ip = ip
                camera.port = port
                camera.chanel = chanel
                camera.codec = codec
                camera.login = login
                camera.password = password
                camera.fullRoute = fullRoute
            else:
                return make_response({'answer': 'No such id'})
        try:
            camera.save()
        except Exception as e:
            return make_response({'answer': 'Save error, check identy if values (full route may be)'})
        data = camera.getJson()
        resp = make_response(data)
        resp.headers['Content-Type'] = "application/json"
        resp.status_code = code
        return resp
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp

@cross_origin
@jwt_required()
@app.route('/setSector', methods=['get', 'post'])
def setSector():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        code = 200
        data = {'OperationStatus': 'Done'}
        try:
            id = request.json['id']
            name = request.json['name']
            typeId = request.json['typeId']
            camId = request.json['camId']
            roomId = request.json['roomId']
            points = request.json['points']
            if points == None:
                points = []
        except Exception as e:
            return make_response({'answer': str(e)}) 
        sector = None
        if id == None:
            sector = Sector(name,typeId,camId,roomId,points)
        else:
            sector = Sector.getByID(id)
            if sector is not None:
                sector.name = name
                sector.typeId = typeId
                sector.camId = camId
                sector.roomId = roomId
                sector.setPointList(points)
            else:
                return make_response({'answer': 'No such id'})
        sector.save()
        data = sector.getParamsList()
        data["points"] = sector.getPointList()
        resp = make_response(data)
        resp.headers['Content-Type'] = "application/json"
        resp.status_code = code
        return resp
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp
    
@cross_origin
@jwt_required()
@app.route('/setTask', methods=['get', 'post'])
def setTask():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        code = 200
        data = {'OperationStatus': 'Done'}
        try:
            id = request.json['id']
            name = request.json['name']
            comment = request.json['comment']
            begin = datetime.strptime(request.json['begin'], '%m/%d/%Y %H:%M:%S')
            end = datetime.strptime(request.json['end'], '%m/%d/%Y %H:%M:%S')
            roomId = request.json['roomId']
            targetCount = request.json['targetCount']
            interval = request.json['interval']
            color = request.json['color']
            
            task = None
            if id == None:
                task = Task(begin, end, roomId, name, targetCount, comment, interval, color)
                task.save()
            else:
                task = Task.getByID(id)
                task.name = name
                task.comment = comment
                task.roomId = roomId
                task.targetCount = targetCount
                task.color = color
                if interval != None:
                    task.interval = interval
                if task.begin != begin or task.end != end:
                    print('was', task.begin, 'now is', begin)
                    task.begin = begin
                    task.end = end
                    print('here')
                    task.save()
                else:
                    task.save(False)
            # print(str(task.begin))
            
            data = task.getParamsList()
        except Exception as e:
            return make_response({'answer': str(e)})
        resp = make_response(data)
        resp.headers['Content-Type'] = "application/json"
        resp.status_code = code
        return resp
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp

@cross_origin
@jwt_required()
@app.route('/setRoom', methods=['get', 'post'])
def setRoom():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        code = 200
        data = {'OperationStatus': 'Done'}
        try:
            id = request.json['id']
            name = request.json['name']
            classId = request.json['classId']
        except Exception as e:
            return make_response({'answer': str(e)})
        
        room = None
        if id == None:
            room = Room(name,classId)
        else:
            room = Room.getByID(id)
            if room is not None:
                room.name = name
                room.classId = classId
            else:
                return make_response({'answer': 'No such id'})
        room.save()
        data = room.getParamsList()
        resp = make_response(data)
        resp.headers['Content-Type'] = "application/json"
        resp.status_code = code
        return resp
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp
    
# delete
@cross_origin
@jwt_required()
@app.route('/removeSector', methods=['get'])
def removeSector():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        code = 200
        data = {'OperationStatus': 'Done'}
        try:
            sector = Sector.getByID(request.args.get('id'))
            sector.delete()
        except Exception as e:
            print(e.__traceback__)
            data = {"answer": 'No Such ID'}
            code = 200
        resp = make_response(data)
        resp.headers['Content-Type'] = "application/json"
        resp.status_code = code
        return resp
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp

@cross_origin
@jwt_required()
@app.route('/removeCamera', methods=['get'])
def removeCamera():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        code = 200
        data = {'OperationStatus': 'Done'}
        try:
            camera = Camera.getByID(request.args.get('id'))
            camera.dropSectors()
            camera.delete()
        except Exception:
            data = {"answer": 'No Such ID'}
            code = 500
        resp = make_response(data)
        resp.headers['Content-Type'] = "application/json"
        resp.status_code = code
        return resp
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp

@cross_origin
@jwt_required()
@app.route('/removeRoom', methods=['get'])
def removeRoom():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        code = 200
        data = {'OperationStatus': 'Done'}
        try:
            room = Room.getByID(request.args.get('id'))
            room.dropSectors()
            room.delete()
        except Exception as e:
            print(e)
            data = {"answer": 'No Such ID'}
            code = 500
        resp = make_response(data)
        resp.headers['Content-Type'] = "application/json"
        resp.status_code = code
        return resp
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp
    
@cross_origin
@jwt_required()
@app.route('/removeTask', methods=['get'])
def removeTask():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        code = 200
        data = {'OperationStatus': 'Done'}
        try:
            task = Task.getByID(request.args.get('id'))
            task.delete()
        except Exception:
            data = {"answer": 'No Such ID'}
            code = 500
        resp = make_response(data)
        resp.headers['Content-Type'] = "application/json"
        resp.status_code = code
        return resp
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp
    
# not ness
@cross_origin
@app.route('/', methods=['GET'])
def main():
    print(verify_jwt_in_request())
    print(get_jwt())
    #user = get_jwt_identity()
    #print(user)
    return "OK"

# @cross_origin()
# @app.route('/test', methods=['get', 'post'])
# def test():
#     print(request.json)
#     return {'answer': 'ok'}
      
# @cross_origin()
# @app.route('/getTestData', methods=['get', 'post',])
# def getTestData():
#     testData = Camera.getAll()
#     result = {"data": []}
#     for data in testData:
#         result["data"].append(data.getParamsList())
#     resp = make_response(result)
#     resp.headers['Content-Type'] = "application/json"
#     return resp


# @app.route('/testSave', methods=['get', 'post'])
# def testSave():
#     obj = Camera('Вторая камера')
#     obj.save()
#     return make_response("ok")
@cross_origin
@app.route('/example', methods=['get', 'post'])
def dbWorkExample():
    room = Room(f'Помещение {DataHolder.getInstance().getParam("roomNumber")}', randint(0,3))
    room.save()
    for i in range(randint(1, 3)):
        cam = Camera(f'камера {DataHolder.getInstance().getParam("cameraNumber")}', 
                     f'192.168.0.{DataHolder.getInstance().getParam("cameraNumber")}',
                     5678,
                     '.vmf8',
                     'login',
                     'password111')
        cam.save()
        for j in range(randint(1, 5)):
            sec = Sector(f'Сектор {DataHolder.getInstance().getParam("cameraNumber")}-{j}', randint(1, 2), cam.id, room.id)
            sec.save()
        DataHolder.getInstance().setParam("cameraNumber", DataHolder.getInstance().getParam("cameraNumber") + 1)  
    DataHolder.getInstance().setParam("roomNumber", DataHolder.getInstance().getParam("roomNumber") + 1)
    
    result = {'room': room.getParamsList(), 'cameras': [], }
    for camera in room.getCameras():
        result['cameras'].append({'data':camera.getParamsList(), 'sectors': []})
        for sector in camera.getSectors():
            result['cameras'][-1]['sectors'].append(sector.getParamsList())
    resp = make_response(result)
    resp.headers['Content-Type'] = "application/json"
    return resp

@cross_origin
@app.route('/getUnusedTest', methods=['get', 'post'])
def getUnusedTest():
    rId = request.args.get('roomId')
    unusedSectors = Sector.getUnusedSectors(int(rId))
    data = [sec.getParamsList() for sec in unusedSectors]
    resp = make_response(data)
    resp.headers['Content-Type'] = "application/json"
    return resp

# cam stream
# stream = None
# stream = cv2.VideoCapture(0)
# def getFrame(stream):
#     i = 0
#     while True:
#         i += 1
#         success, image = stream.read()
#         ret, jpeg = cv2.imencode('.jpg', image)
#         frame = jpeg.tobytes()
#         if i < 10:
#             yield (b'--frame\r\n'
#                     b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#         else:
#             yield (b'--frame\r\n'
#                     b'Content-Type: image/jpeg\r\n\r\n'+ b'\r\n')
#         time.sleep(0.2)

# @cross_origin
# @app.route('/videoStream')
# def video_feed():
#     global stream
#     stream = cv2.VideoCapture(0)
#     data = getFrame(stream)
#     print('i\'v been asked for photo')
#     return Response(data,
#                     mimetype='multipart/x-mixed-replace; boundary=frame')
    
# @cross_origin
# @app.route('/stopVideo')
# def stopVideo():
#     stream.release()
#     return make_response('OK')
    

 
# # cam = Camera('test', fullRoute='0')
# # stream = Stream(cam, timeLimit = 20)
    
# # @cross_origin
# # @app.route('/testVideo')
# # def testVideo():
# #     global stream
# #     stream.init()
# #     return Response(stream.getStream(),
# #                     mimetype='multipart/x-mixed-replace; boundary=frame')
    
# # @cross_origin
# # @app.route('/testRefreshVideo')
# # def testRefreshVideo():
# #     global stream
# #     stream.resetTime()
# #     return 'ok'


# video stream branch
@cross_origin
@app.route('/getVideo')
def getVideo():
    try:
        camId = request.args.get('camId')
    except:
        return make_response({'answer': 'Add camId param correctly'})
    camera = Camera.getByID(camId)
    if camera is None:
        return make_response({'answer': 'No such id'})

    resp = Response(FrameGetter.getStream(camera.getRoute(), 30),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
    resp.headers["Pragma"] = "no-cache" # HTTP 1.0.
    resp.headers["Expires"] = "0" # 
    return resp

    
@cross_origin
@jwt_required()
@app.route('/refreshVideo')
def refreshVideo():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        try:
            camId = request.args.get('camId')
        except:
            return make_response({'answer': 'Add camId param correctly'})
        camera = Camera.getByID(camId)
        if camera is None:
            return make_response({'answer': 'No such id'})
        return make_response({'answer': FrameGetter.refreshStream(camera.getRoute(), 30)})
    else:
            resp = make_response({'answer': "Bad token"})
            resp.headers['Content-Type'] = "application/json"
            return resp
    
    
# file data selector
@cross_origin
@jwt_required()
@app.route('/getByRoutes', methods=['post'])
def getByRoutes():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        try:
            baseRoute = request.json['baseRoute']
        except Exception:
            return {"answer": 'Bad json'}, 200
        curRoute = None
        try:
            curRoute = request.json['curRoute']
        except Exception:
            pass
        fileName = None
        
        try:
            fileName = request.json['fileName']
        except Exception:
            pass
        
        print(baseRoute)
        curDir = os.path.normpath(baseRoute)
        if curRoute:
            curDir = os.path.join(curDir, curRoute)
            
        if not fileName:
            #get files:
            data = []
            for elem in os.listdir(curDir):
                tempRoute = os.path.join(curDir, elem)
                if os.path.isdir(tempRoute):
                    data.append({'name': elem, 'type':'dir'})
                else:
                    data.append({'name': elem, 'type':'file', 'createTime': datetime.fromtimestamp(os.path.getctime(tempRoute))})
            
            return {'folderData': data}, 200
        else:
            tempDir = os.path.join(curDir, fileName)
            if not os.path.isdir(tempDir):
                cap = cv2.VideoCapture(tempDir)
                ret, frame = cap.read()
                if ret:
                    bytesData = FileUtil.convertImageToBytes(frame, '.jpg')
                    return {'name': fileName, 'route': tempDir, 'type':'file', 'createTime': datetime.fromtimestamp(os.path.getctime(tempDir)), 'image':bytesData}
                return {'answer': 'can not open file'}
            return {'answer': 'not a file'}
            
    else:
        resp = make_response({'answer': "Bad token"})
        resp.headers['Content-Type'] = "application/json"
        return resp
    
@cross_origin
@jwt_required()
@app.route('/sendForAnalize', methods=['post'])
def sendForAnalize():
    verify_jwt_in_request()
    identy = get_jwt_identity()
    if identy:
        try:
            route = request.json['route']
            dir = os.path.normpath(route)

            #test access
            
            name = request.json['name']
            comment = request.json['comment']
            begin = datetime.strptime(request.json['begin'], '%m/%d/%Y %H:%M:%S')
            end = datetime.strptime(request.json['end'], '%m/%d/%Y %H:%M:%S')
            roomId = request.json['roomId']
            targetCount = request.json['targetCount']
            interval = request.json['interval']
            color = request.json['color']
        except Exception as e:
            return {'answer': 'Bad json', 'key': str(e)}, 200
        try:
            task = Task(begin, end, roomId, name, targetCount, comment, interval, color)
        
            task._setStatusDone()
            print('here before saving')
            task.save(False)
        except Exception as e:
            try:
                task.delete()
            except:
                pass
            print(e)
            return {'answer': 'Can not save data to DB'}, 200
        try:
            if not os.path.isdir(dir):
                cap = cv2.VideoCapture(dir)
                ret, frame = cap.read()
                if ret:
                    thread = TaskArchiveRunner(dir, interval, task.id)
                    thread.start()
                    return {'id': task.id, 'answer': 'recogonition beguns'}, 200
                task.delete()
                return {'answer': 'can not read from file'}, 200
        except:
            task.delete()
            return {'answer': 'can not open file with cv2'}, 200
            