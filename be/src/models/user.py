from src import db
from src.models.fridge import fridge_user


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    unusedItemsPreference = db.Column(db.Integer)
    expiryDatePreference = db.Column(db.Integer)
    fridges = db.relationship('Fridge', secondary=fridge_user, back_populates='users')
    