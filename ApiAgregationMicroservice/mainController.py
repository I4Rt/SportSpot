from config import *
from model.SportObject import *
from model.DataRow import *
from model.OutUser import *
from werkzeug.exceptions import *
from flask import request
from sqlalchemy.exc import DatabaseError
import sys
from time import time, sleep
from datetime import datetime



actualRoomsInfo = None


@auth.verify_password
def verify_password(username, password):
    user = OutUser.getUserByLogin(username)
    if user:
        if user.checkUser(password):
            return username




try:
    with open('roomsData.txt', 'r') as file:
        actualRoomsInfo = json.loads(file.read())
except Exception as e:
    print(e)
    actualRoomsInfo = {}
    with open('roomsData.txt', 'w') as file:
        file.write(json.dumps(actualRoomsInfo))
        

index = 0
def exceptionProcessing(foo):
    global index
    def inner(*args, **kwargs):
        try:
            return foo(*args, **kwargs)
        except HTTPException as httpe:
            return {request.path.split('/')[-1]: False, 'data': {'description': 'HTTP error'}}, httpe.code
        except DatabaseError as de:
            return {request.path.split('/')[-1]: False, 'data': {'description': 'Identy error, such outerId already exist'}}, 200
        except KeyError as jsone:
            return {request.path.split('/')[-1]: False, 'data': {'description': f'Json error, lost {str(jsone.args[0]).upper()} param', 'param': jsone.args[0]}}, 200
        except Exception as e:
            print(e)
            return {request.path.split('/')[-1]: False, 'data': {'description': 'Unmatched error', "error": type(e).__name__}}, 200
    inner.__name__ = "inner" + str(index)
    index += 1
    return inner


@app.route('/management/getTest', methods=['get'])
@auth.login_required
@cross_origin()
def getTest():
    try:
        info = request.args.get('data')
        return {'getTest': True, 'data':{'info': info}}, 200
    except:
        return {'getTest': False}, 200
    
@app.route('/management/SORegister', methods=['post'])
@auth.login_required
@cross_origin()
@exceptionProcessing
def soRegister():
    
    name = request.json['name']
    info = request.json['info']
    t = int(time() * 10000)
    ht = "{0:x}".format(t)
    outerId = '0' * (12 - len(ht)) + ht
    so = SportObject(name, outerId, info)
    so.save()
    return {'SORegister': True, 'data':{'SOId': so.id, 'outerId': outerId}}, 200
    

#{day:{time: [roomId:{plan:, real:},],},}
@app.route('/management/appendData', methods=['post'])
@exceptionProcessing
@cross_origin()
def appendData():
    global actualRoomsInfo
    data = request.json['data']
    soId = request.json['SOId']
    print(request.json['rooms'])
    actualRoomsInfo[str(SportObject.getByID(int(soId)).outerId)] = request.json['rooms']
    
    with open('roomsData.txt', 'w') as file:
        file.write(json.dumps(actualRoomsInfo))

    print(list(data.keys()))
    
    counter = 0
    
    for dayStamp in data:
        for timeStamp in data[dayStamp]:
            try:
                print("day", dayStamp)
                date = datetime.strptime(dayStamp, '%Y-%m-%d').date()
                timeInterval = datetime.strptime(timeStamp, '%H-%M-%S').time()
                print('rooms len is', len(data[dayStamp][timeStamp]))
                for roomId in data[dayStamp][timeStamp]:
                    try:
                        elemData = data[dayStamp][timeStamp][roomId]
                        element = DataRow(soId, int(roomId), date, timeInterval, elemData['plan'], elemData['real'])
                        res = element.update()
                        if res < 1:
                            element.save()
                        print(element)
                        counter += 1
                        if date < datetime.now().date():
                            print('saved old data')
                    except Exception as e:
                        print('can not update data', e)
                    
            except Exception as e:
                print('can not getDate', e)
    return {'appendData': True, 'data':{'updated': counter}}, 200

@app.route('/api/getStatisticsData', methods=['get', 'post'])
@auth.login_required
@cross_origin()
@exceptionProcessing
def getData():
        
        sideId = request.args.get("SOId")
        id = None
        if sideId:
            so = SportObject.getBySideId(str(sideId))
            if not so:
                return {'getStatisticsData': False, 'data':{'description': 'No such side id'}}, 200
            id = so.id
        
        begin = datetime.strptime(request.json['begin'], '%d-%m-%Y %H:%M:%S')
        end = datetime.strptime(request.json['end'], '%d-%m-%Y %H:%M:%S')
        
        beginDate = begin.date()
        beginTime = begin.time()
        
        endDate = end.date()
        endTime = end.time()
        
        data = DataRow.getInInterval(beginDate, beginTime, endDate, endTime, id)
        print(len(data))
        
        resultData = {}
        for elem in data:
            sideObjId = elem.getSideSOId()
            if not (sideObjId in resultData):
                resultData[sideObjId] = {}
            
            
            if str(elem.date.date()) in resultData[sideObjId]:
                
                if str(elem.timeInterval) in resultData[sideObjId][str(elem.date.date())]:
                    resultData[sideObjId][str(elem.date.date())][str(elem.timeInterval)][str(elem.roomId)] = {'plan': elem.plan, 'real': elem.real}
                else:
                    resultData[sideObjId][str(elem.date.date())][str(elem.timeInterval)] = {str(elem.roomId): {'plan': elem.plan, 'real': elem.real}}
                    
            else:
                
                resultData[sideObjId][str(elem.date.date())] = { str(elem.timeInterval) : {str(elem.roomId): {'plan': elem.plan, 'real': elem.real}}}
            
        
        return {'getStatisticsData': True, 'data':{'statistics': resultData}}, 200
    
    
@app.route('/api/getRoomsData', methods=['post'])
@auth.login_required
@cross_origin()
@exceptionProcessing
def getRoomsData():
    global actualRoomsInfo
    return {'getRoomsData': True, 'data':{'rooms': actualRoomsInfo}}, 200
    
    
@app.route('/api/getSportObjects', methods=['get', 'post'])
@auth.login_required
@cross_origin()
@exceptionProcessing
def getSportObjects():
    data = [so.getParamsList() for so in SportObject.getAll()]
    return {'getSportObjects': True, 'data':{'sport objects': data}}, 200
    
    
    
@app.route('/api/register', methods=['post'])
@auth.login_required
@cross_origin()
@exceptionProcessing
def getSportObjects():
    login = request.json['login']
    password = request.json['password']
    OutUser(login, password).save()
    return {'register': True}, 200

@app.route('/api/askChangePassword', methods=['post'])
@cross_origin()
@exceptionProcessing
def askChangePassword():
    login = request.json['login']
    newPassword = request.json['newPassword']
    user = OutUser.getUserByLogin(login)
    if user:
        user.newPasswordHash = generate_password_hash(newPassword)
        user.save()
        return {'askChangePassword': True}
    return {'askChangePassword': False, 'data': {'description': f'No user with login {str(login).upper()}', 'login': login}}

@app.route('/api/permitChangePassword', methods=['post'])
@cross_origin()
@exceptionProcessing
def permitChange():
    login = request.json['login']

    user = OutUser.getUserByLogin(login)
    if user:
        if user.newPasswordHash:
            user.passwordHash = user.newPasswordHash
            user.newPasswordHash = None
            user.save()
            return {'permitChangePassword': True}
        else:
            return {'permitChangePassword': False, 'data': {'description': f'User with login {str(login).upper()} did not ask for password change', 'login': login}}
    return {'permitChangePassword': False, 'data': {'description': f'No user with login {str(login).upper()}', 'login': login}}


@app.route('/api/getUsersToChangePassword', methods=['get'])
@cross_origin()
@exceptionProcessing
def getUsersToChangePassword():
    users = OutUser.getUsersToChangePassword()
    userData = []
    for u in users:
        userData.append(u.login)
    return {'permitChangePassword': True, 'data': {'logins': userData}}
    

