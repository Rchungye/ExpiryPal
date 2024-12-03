from sqlalchemy import func
from src import db
from datetime import datetime


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    fridge_id = db.Column(db.Integer, db.ForeignKey('fridge.id'))
    name = db.Column(db.String(50))
    addedDate = db.Column(db.Date, default=func.now())
    expirationDate = db.Column(db.Date)

