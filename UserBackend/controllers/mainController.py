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
        cam = Camera(f'камера {DataHolder.getInstance().getParam("cameraNumber")}')
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