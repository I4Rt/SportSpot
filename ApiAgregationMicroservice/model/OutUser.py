from __future__ import annotations
from config import *
from model.BaseData import *
from werkzeug.security import generate_password_hash, check_password_hash

class OutUser(db.Model, BaseData):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Text, unique=True)
    passwordHash = db.Column(db.Text, unique=False, nullable=True)
    
    def __init__(self, login:str, password:str):
        db.Model.__init__(self)
        BaseData.__init__(self, self.id)
        self.login = login
        self.passwordHash = generate_password_hash(password)
        
        
    def checkUser(self, password):
        return check_password_hash(self.passwordHash, password)
    
    @classmethod
    def getUserByLogin(cls, login):
        return db.session.query(OutUser).filter(cls.login == login).first()
        
    
    
    
        
        
        
        
        