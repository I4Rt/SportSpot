from config import *
from werkzeug.exceptions import *
from flask import request
from sqlalchemy.exc import DatabaseError
from tools.KafkaFactory import *

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

@testDecorator  
@app.route('/appendDataToRoute', methods=['post'])
@cross_origin()
def appendDataToRoute():
    SOId = request.json['SOId']
    data = request.json['data'] # data
    
    sender = KafkaPublicSender.getKafkaSender(app.config["kafkaServer"], f'SO{int(SOId)}_local')
    result = sender.sendMessage(json.dumps(data))
    sender.closeConnection()
    
    if result == 1:
        return {'SORegister': False, 'data':{'msg':'topic creation error'}}, 200
    elif result == 2:
        return {'SORegister': False, 'data':{'msg':'not initializated produver'}}, 200
    elif result == 3:
        return {'SORegister': False, 'data':{'msg':'kafka time is out'}}, 200
    return {'SORegister': True}, 200


    
    