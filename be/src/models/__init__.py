from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

from .fridge import Fridge
from .camera import Camera
from .item import Item
from .notification import Notification
from .fridge_user import FridgeUser

class FridgeUser(db.Model):
    __tablename__ = 'fridge_user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    fridge_id = db.Column(db.Integer, db.ForeignKey('fridge.id'))

from .user import User