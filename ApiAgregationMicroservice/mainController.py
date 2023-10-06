from config import *
from model.SportObject import *
from model.DataRow import *
from werkzeug.exceptions import *
from flask import request
from sqlalchemy.exc import DatabaseError
import sys
from time import time, sleep
from datetime import datetime
actualRoomsInfo = None
try:
    with open('roomsData.txt', 'e') as file:
        actualRoomsInfo = json.loads(file.read())
except:
    actualRoomsInfo = {}
    with open('roomsData.txt', 'w') as file:
        file.write(json.dumps(actualRoomsInfo))
        

index = 0
def testDecorator(foo):
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
# wtf with decorator?

@app.route('/management/getTest', methods=['get'])
@cross_origin()
def getTest():
    try:
        info = request.args.get('data')
        return {'getTest': True, 'data':{'info': info}}, 200
    except:
        return {'getTest': False}, 200
    
@app.route('/management/SORegister', methods=['post'])
@cross_origin()
@testDecorator
def soRegister():
    
    name = request.json['name']
    outerId = request.json['outerId']
    info = request.json['info']
    so = SportObject(name, outerId, info)
    so.save()
    return {'SORegister': True, 'data':{'SOId': so.id}}, 200
    

#{day:{time: [roomId:{plan:, real:},],},}
@app.route('/management/appendData', methods=['post'])
@cross_origin()
@testDecorator
def appendData():
    global actualRoomsInfo
    data = request.json['data']
    soId = request.json['SOId']
    print(request.json['rooms'])
    actualRoomsInfo[str(SportObject.getByID(int(soId)))] = request.json['rooms']
    
    with open('roomsData.txt', 'w') as file:
        file.write(json.dumps(actualRoomsInfo))
    '''
    {
        day:{
            time: {
                plan: plan,
                counter: counter
            }
        }
    }
    '''
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
                        element.update()
                        
                        counter += 1
                    except Exception as e:
                        print('can not update data', e)
            except Exception as e:
                print('can not getDate', e)
            return {'appendData': True, 'data':{'updated': counter}}, 200

@app.route('/api/getStatisticsData', methods=['get', 'post'])
@cross_origin()
@testDecorator
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
            # print(str(elem.date.date()), resultData[elem.sportObjectId])
            
            if str(elem.date.date()) in resultData[sideObjId]:
                # print('here')
                if str(elem.timeInterval) in resultData[sideObjId][str(elem.date.date())]:
                    resultData[sideObjId][str(elem.date.date())][str(elem.timeInterval)][str(elem.roomId)] = {'plan': elem.plan, 'real': elem.real}
                else:
                    resultData[sideObjId][str(elem.date.date())][str(elem.timeInterval)] = {str(elem.roomId): {'plan': elem.plan, 'real': elem.real}}
                    
            else:
                # print('here 2')
                resultData[sideObjId][str(elem.date.date())] = { str(elem.timeInterval) : {str(elem.roomId): {'plan': elem.plan, 'real': elem.real}}}
            
        
        return {'getStatisticsData': True, 'data':{'statistics': resultData}}, 200
    
    
@app.route('/api/getRoomsData', methods=['post'])
@cross_origin()
@testDecorator
def getRoomsData():
    global actualRoomsInfo
    return {'getRoomsData': True, 'data':{'rooms': actualRoomsInfo}}, 200
    