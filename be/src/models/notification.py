from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
from . import db


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    notificationDate = db.Column(db.DateTime)
    message = db.Column(db.Text)