from config import *
from werkzeug.exceptions import *
from flask import request
from sqlalchemy.exc import DatabaseError
from tools.KafkaFactory import *

from datetime import datetime


localReceiverStorage = {}
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
    
    query = request.json['query']
    data = request.json['data'] # data

    print('query to write', query)
    
    print(app.config["kafkaServer"])
    print('data', list(data.keys()))
    sender = KafkaPublicSender.getKafkaSender(query, app.config["kafkaServer"])
    result = sender.sendMessage(json.dumps(data))
    sender.closeConnection()
    
    if result == 1:
        return {request.path[1:]: False, 'data':{'msg':'topic creation error'}}, 200
    elif result == 2:
        return {request.path[1:]: False, 'data':{'msg':'not initializated produver'}}, 200
    elif result == 3:
        return {request.path[1:]: False, 'data':{'msg':'kafka time is out'}}, 200
    return {request.path[1:]: True}, 200
    
    
@app.route('/readData', methods=['get', 'post'])
@testDecorator 
@cross_origin()
def readDataFromRoute():
    global localReceiverStorage
    topicName = request.args.get('topic')
    
    if not (topicName in localReceiverStorage):
        localReceiverStorage[topicName] = KafkaPublicReciever.getKafkaReciever(topicName, app.config["kafkaServer"], True).recieve()
    try:
        taskData = next(localReceiverStorage[topicName])
    except Exception as e:
        print('got exception', e)
        localReceiverStorage[topicName] = KafkaPublicReciever.getKafkaReciever(topicName, app.config["kafkaServer"]).recieve()
        taskData = next(localReceiverStorage[topicName])
    
        
    print(type(taskData.value), taskData.value)
    try:
        return {request.path[1:]: True, 'data':{'message': json.loads(taskData.value)}}, 200
    except:
        raise Exception('error was here')


@app.teardown_request
def teardown(exception=None):
    if exception:
        print(f'exception is {exception}')
    


    


    
    