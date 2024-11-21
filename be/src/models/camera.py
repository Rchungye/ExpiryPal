from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
from . import db

class Camera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fridge_id = db.Column(db.Integer, db.ForeignKey('fridge.id'))
    model = db.Column(db.String(50))
    brand = db.Column(db.String(50))
    accessURL = db.Column(db.String(2048))