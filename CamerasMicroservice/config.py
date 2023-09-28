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


