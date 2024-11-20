from . import db
from .fridge_user import FridgeUser 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    unusedItemsPreference = db.Column(db.Integer)
    expiryDatePreference = db.Column(db.Integer)
    fridges = db.relationship('Fridge', secondary='fridge_user', back_populates='users')
    def __init__(self, username, unusedItemsPreference, expiryDatePreference):
        self.username = username
        self.unusedItemsPreference = unusedItemsPreference
        self.expiryDatePreference = expiryDatePreference
