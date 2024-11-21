from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
from .fridge_user import fridge_user
from . import db

class Fridge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50))
    brand = db.Column(db.String(50))
    code = db.Column(db.String(50), unique=True)
    cameras = db.relationship('Camera', backref='fridge')
    items = db.relationship('Item', backref='fridge')
    users = db.relationship('User', secondary=fridge_user, back_populates='fridges')
    
    def __init__(self, model, brand, code):
        self.model = model
        self.brand = brand
        self.code = code