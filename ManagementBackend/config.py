from flask import Flask, request, json
from time import time
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from flask_cors import CORS, cross_origin
from datetime import timedelta




app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path = '')
app.config['SPORT_OBJECT_ID'] = '001'
app.config['TIME'] = time()
app.config['SIZE'] = 1000

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwerty@localhost:5432/sport_object_main'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


# app has been set and configured

db = SQLAlchemy(app)
Session(app)

app.config["JWT_SECRET_KEY"] = "you better not change it, because i will lose access"
jwt = JWTManager(app)


#side
app.config['id'] = 'yarigina-local-'
app.config['groop'] = app.config['id'] + 'recieve-task-groop'
app.config['topic'] = app.config['id'] + 'recieve-task-topic'



def sessionly(foo, *args,**kwargs):
    def inner(*args,**kwargs):
        Session(app)
        res = foo(*args,**kwargs)
        db.session.commit()
        # db.session.close()
        return res
    return inner