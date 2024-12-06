from src import db
from datetime import datetime


class NotificationPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fridge_id = db.Column(db.Integer, db.ForeignKey('fridge.id'), unique=True)
    expiration = db.Column(db.Integer)  # Notify me x days before expiration
    unusedItem = db.Column(db.Integer)  # Notify me if the item has not been used in x days

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
