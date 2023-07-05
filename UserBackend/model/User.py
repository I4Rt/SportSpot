from __future__ import annotations
from config import *
from typing import List

class User(db.Model):
    
    
    
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False)
    surname = db.Column(db.String(150), unique=False)
    login = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(300), unique=False)
    role = db.Column(db.String(120))
    
    def __init__(self, 
                 name:str, surname:str, 
                 login:str, password:str, 
                 role:str = "USER"):
        self.name = name
        self.surname = surname
        self.login = login
        self.password = password
        self.role = role
        
    def access(self, route):
        USER = ['main']
        ADMIN = ['cameras', 'rooms', 'confirmations']
        ALL = ['login']
        if (self.role == "USER" and route in USER) or (self.role == "ADMIN" and route in ADMIN) or (route in ALL):
            return True
        return False
    
    @staticmethod
    def getByName(userLogin:str) -> List[User]:
        return User.query.filter_by(login = userLogin).all()
    
        
        