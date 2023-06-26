from flask import render_template, flash, redirect, url_for
from config import *
from tools.jwtHolder import *
from model.User import *
from flask_jwt_extended import *
import json

@jwt_required()
@app.route('/', methods=['GET'])
def main():
    print(verify_jwt_in_request())
    print(get_jwt())
    #user = get_jwt_identity()
    #print(user)
    return "OK"


@app.route('/authorize', methods=['get', 'post',])
def authorize():
    login = request.form['login']
    password = request.form['password']
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
    return "not valid data"
    