from config import *
from werkzeug.exceptions import *
from flask import request
from sqlalchemy.exc import DatabaseError
from tools.KafkaFactory import *

from datetime import datetime
index = 0
def testDecorator(foo):
    global index
    def inner(*args, **kwargs):
        try:
            return foo(*args, **kwargs)
        except HTTPException as httpe:
            return {request.path[1:]: False, 'data': {'description': 'HTTP error'}}, httpe.code
        except DatabaseError as de:
            return {request.path[1:]: False, 'data': {'description': 'Identy error, such outerId already exist'}}, 200
        except KeyError as jsone:
            return {request.path[1:]: False, 'data': {'description': f'Json error, lost {str(jsone.args[0]).upper()} param', 'param': jsone.args[0]}}, 200
        except Exception as e:
            return {request.path[1:]: False, 'data': {'description': 'Unmatched error', "error": type(e).__name__}}, 200
    inner.__name__ = "inner" + str(index)
    index += 1
    return inner

 
@app.route('/appendDataToRoute', methods=['post'])
@testDecorator 
@cross_origin()
def appendDataToRoute():
    
    SOId = request.json['SOId']
    data = request.json['data'] # data
    print(f'SO{int(SOId)}_local')
    print(app.config["kafkaServer"])
    sender = KafkaPublicSender.getKafkaSender(f'SO{int(SOId)}_local', app.config["kafkaServer"])
    result = sender.sendMessage(json.dumps(data))
    sender.closeConnection()
    
    if result == 1:
        return {request.path[1:]: False, 'data':{'msg':'topic creation error'}}, 200
    elif result == 2:
        return {request.path[1:]: False, 'data':{'msg':'not initializated produver'}}, 200
    elif result == 3:
        return {request.path[1:]: False, 'data':{'msg':'kafka time is out'}}, 200
    return {request.path[1:]: True}, 200
    