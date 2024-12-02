from src import db
from datetime import datetime
from src.models.Fridge import Fridge


class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True)
    fridge_id = db.Column(db.Integer, db.ForeignKey('fridge.id'))
    name = db.Column(db.String(50), nullable = True)
    expDate = db.Column(db.Date(), nullable = True)
    notifications = db.relationship('Notification', backref='item')
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(), onupdate=datetime.now())

    def as_dict(self):
        return{
            "id": self.id,
            "fridge_id": self.fridge_id,
            "name": self.name,
            "expDate": self.expDate,
            "notifications": self.notifications,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }