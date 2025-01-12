from sqlalchemy import func
from src import db
from datetime import datetime

class FridgeLog(db.Model):
    __tablename__ = 'fridgeLog'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now(), nullable=False)
    action = db.Column(db.String(255), nullable=False)  # e.g. "Changed expiration date"
    details = db.Column(db.Text, nullable=True)  #  e.g. "From '2021-12-31' to '2022-12-31'"

    item = db.relationship('Item', backref='logs', cascade='all, delete')
    user = db.relationship('User', backref='item_logs')
