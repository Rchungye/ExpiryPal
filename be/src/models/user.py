from src import db
from src.models.fridge import fridge_user


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    fridges = db.relationship('Fridge', secondary=fridge_user, back_populates='users')
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}