from flask import render_template, flash, redirect, url_for, make_response
from config import *
from tools.jwtHolder import *
from model.TestTable import *
from model.User import *
from flask_jwt_extended import *
import json



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
    testData = TestTable.getAll()
    result = {"data": []}
    for data in testData:
        result["data"].append(data.getJson())
    resp = make_response(result)
    resp.headers['Content-Type'] = "application/json"
    return resp