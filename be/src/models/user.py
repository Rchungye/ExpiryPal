from src import db
from src.models.Fridge import fridge_user, Fridge


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    unusedItemsPref = db.Column(db.Integer, nullable=True)
    expDatePref = db.Column(db.Integer, nullable=True)
    fridges = db.relationship('Fridge', secondary=fridge_user, back_populates='users')
    
    def as_dict(self):
        return{
            "id": self.id,
            "username": self.username,
            "unusedItemsPref": self.unusedItemsPref,
            "expDatePref": self.expDatePref,
            "fridges": self.fridges
        }