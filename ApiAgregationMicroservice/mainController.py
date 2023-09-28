from config import *
from model.SportObject import *
from model.DataRow import *

from flask import request

@app.route('/getTest', methods=['get'])
@cross_origin
def getTest():
    try:
        info = request.args.get('data')
        return {'getTest': True, 'data':{'info': info}}, 200
    except:
        return {'getTest': False}, 200