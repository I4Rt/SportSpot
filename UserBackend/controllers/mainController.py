from flask import render_template, flash, redirect, url_for, make_response
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

from system.DataHodler import *
from random import randint

DataHolder.getInstance().setParam("cameraNumber", 60)
DataHolder.getInstance().setParam("roomNumber", 15)




@cross_origin()
@jwt_required
@app.route('/', methods=['GET'])
def main():
    print(verify_jwt_in_request())
    print(get_jwt())
    #user = get_jwt_identity()
    #print(user)
    return "OK"

@cross_origin()
@app.route('/test', methods=['get', 'post'])
def test():
    print(request.json)
    return {'answer': 'ok'}

@cross_origin()
@app.route('/authorize', methods=['get', 'post',])
def authorize():
    #print(request.json)
    login = request.json['login']
    password = request.json['password']
    print(User.getByName(login))
    users = User.getByName(login)
    if len(users) > 0:
        if bcrypt.check_password_hash(users[0].password, password):
            access_token = create_access_token(identity=users[0].id, fresh=True)
            refresh_token = create_refresh_token(users[0].id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
    return {'answer': 'not valid data'}


@cross_origin
@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    if identity:
        access_token = create_access_token(identity=identity)
        return {'access_token': access_token}
    return {"answer": "your token is too old or not valid"}
    
        
@cross_origin()
@app.route('/getTestData', methods=['get', 'post',])
def getTestData():
    testData = Camera.getAll()
    result = {"data": []}
    for data in testData:
        result["data"].append(data.getParamsList())
    resp = make_response(result)
    resp.headers['Content-Type'] = "application/json"
    return resp


@app.route('/testSave', methods=['get', 'post'])
def testSave():
    obj = Camera('Вторая камера')
    obj.save()
    return make_response("ok")

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
@jwt_required
@app.route('/getCameras', methods=['get', 'post'])
def getCameras():
    data = []
    cams = Camera.getAll()
    for cam in cams:
        data.append(cam.getParamsList())
    resp = make_response(data)
    resp.headers['Content-Type'] = "application/json"
    return resp


@cross_origin
@jwt_required
@app.route('/getCameraByID', methods=['get', 'post'])
def getCameraByID():
    try:
        camera = Camera.getByID(request.args.get('id'))
        data = camera.getParamsList()
    except Exception:
        data = {"answer": "No such ID"}
    resp = make_response(data)
    resp.headers['Content-Type'] = "application/json"
    return resp

@cross_origin
@jwt_required
@app.route('/getSectorsByCameraID', methods=['get', 'post'])
def getSectorsByCameraID():
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

@jwt_required
@app.route('/getSectorByID', methods=['get', 'post'])
def getSectorByID():
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

@cross_origin
@jwt_required
@app.route('/getSectorTypes', methods=['get', 'post'])
def getSectorTypes():
    objectiveData = SectorType.getAll()
    data = []
    for obj in objectiveData:
        data.append(obj.getParamsList())
    return data

@cross_origin
@jwt_required
@app.route('/getRooms', methods=['get', 'post'])
def getRooms():
    objectiveData = Room.getAll()
    data = []
    for obj in objectiveData:
        dataList = obj.getParamsList()
        dataList['roomType'] = RoomType.getByID(dataList["classId"]).getParamsList()
        data.append(dataList)
    resp = make_response(data)
    resp.headers['Content-Type'] = "application/json"
    return resp
@cross_origin
@jwt_required
@app.route('/getRoomByID', methods=['get', 'post'])
def getRoomByID():
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

@cross_origin
@app.route('/getCameraSectorsByRoomId', methods=['get', 'post'])
def getCameraSectorsByRoomId():
    
    room = Room.getByID(request.args.get('id'))
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
