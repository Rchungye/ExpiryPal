from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class FridgeUser(db.Model):
    __tablename__ = 'fridge_user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    fridge_id = db.Column(db.Integer, db.ForeignKey('fridge.id'))

    
from .user import User