from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fridge_id = db.Column(db.Integer, db.ForeignKey('fridge.id'))
    name = db.Column(db.String(50))
    addedDate = db.Column(db.Date)
    expirationDate = db.Column(db.Date)
    notifications = db.relationship('Notification', backref='item')