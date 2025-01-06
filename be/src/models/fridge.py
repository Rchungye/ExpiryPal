from src import db
from datetime import datetime

fridge_user = db.Table(
    'fridge_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('fridge_id', db.Integer, db.ForeignKey('fridge.id'), primary_key=True)
)

class Fridge(db.Model):
    __tablename__ = "fridge"
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50))
    brand = db.Column(db.String(50))
    code = db.Column(db.String(50), unique=True)
    cameras = db.relationship('Camera', backref='fridge')
    items = db.relationship('Item', backref='fridge')
    users = db.relationship('User', secondary=fridge_user, back_populates='fridges')
    last_link_attempt = db.Column(db.DateTime, nullable=True)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}