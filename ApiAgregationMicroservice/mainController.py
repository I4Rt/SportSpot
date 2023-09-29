from config import *
from model.SportObject import *
from model.DataRow import *
from werkzeug.exceptions import *
from flask import request
from sqlalchemy.exc import DatabaseError
import sys

from datetime import datetime
 
def testDecorator(foo):
    def inner(*args, **kwargs):
        try:
            return foo(*args, **kwargs)
        except HTTPException as httpe:
            return {'SORegister': False, 'data': {'description': 'HTTP error'}}, httpe.code
        except DatabaseError as de:
            return {'SORegister': False, 'data': {'description': 'Identy error, such outerId already exist'}}, 200
        except KeyError as jsone:
            return {'SORegister': False, 'data': {'description': f'Json error, lost {str(jsone.args[0]).upper()} param', 'param': jsone.args[0]}}, 200
        except Exception as e:
            return {'SORegister': False, 'data': {'description': 'Unmatched error', "error": type(e).__name__}}, 200
    return inner

@app.route('/management/getTest', methods=['get'])
@cross_origin()
def getTest():
    try:
        info = request.args.get('data')
        return {'getTest': True, 'data':{'info': info}}, 200
    except:
        return {'getTest': False}, 200
    
@testDecorator  
@app.route('/management/SORegister', methods=['post'])
@cross_origin()
def soRegister():
    name = request.json['name']
    outerId = request.json['outerId']
    info = request.json['info']
    so = SportObject(name, outerId, info)
    so.save()
    return {'SORegister': True, 'data':{'SOId': so.id}}, 200

@testDecorator
@app.route('/management/appendData', methods=['post'])
@cross_origin()
def appendData():
    data = request.json['data']
    soId = request.json['SOId']
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
                date = datetime.strptime(dayStamp, '%d-%m-%Y').date()
                timeInterval = datetime.strptime(timeStamp, '%H:%M:%S').time()
                element = DataRow(soId, date, timeInterval, data[dayStamp][timeStamp]['plan'], data[dayStamp][timeStamp]['real'])
                element.update()
                counter += 1
            except:
                pass
            
    return {'appendData': True, 'data':{'updated': counter}}, 200

@testDecorator
@app.route('/api/getData', methods=['post'])
@cross_origin()
def getData():
    begin = datetime.strptime(request.json['begin'], '%d-%m-%Y %H:%M:%S')
    end = datetime.strptime(request.json['end'], '%d-%m-%Y %H:%M:%S')
    
    beginDate = begin.date()
    beginTime = begin.time()
    
    endDate = end.date()
    endTime = end.time()
    
    data = DataRow.getInInterval(beginDate, beginTime, endDate, endTime)
    print(len(data))
    
    resultData = {}
    for elem in data:
        if not (elem.sportObjectId in resultData):
            resultData[elem.sportObjectId] = {}
        # print(str(elem.date.date()), resultData[elem.sportObjectId])
        
        if str(elem.date.date()) in resultData[elem.sportObjectId]:
            print('here')
            resultData[elem.sportObjectId][str(elem.date.date())][str(elem.timeInterval)] = {'plan': elem.plan, 'real': elem.real}
        else:
            print('here 2')
            resultData[elem.sportObjectId][str(elem.date.date())] = { str(elem.timeInterval) : {'plan': elem.plan, 'real': elem.real} }
        
    
    return {'appendData': True, 'data':{'statistics': resultData}}, 200
    
    
    
    
    
    
    