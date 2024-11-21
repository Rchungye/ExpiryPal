from flask_sqlalchemy import SQLAlchemy
from . import db

fridge_user = db.Table(
    'fridge_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('fridge_id', db.Integer, db.ForeignKey('fridge.id'), primary_key=True)
)
