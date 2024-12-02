from src import db
from src.models.User import User
from src.models.Fridge import Fridge
from src.models.Item import Item

fridge_user = db.Table(
    'fridge_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('fridge_id', db.Integer, db.ForeignKey('fridge.id'), primary_key=True)
)


class Fridge(db.Model):
    __tablename__ = "camara"
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50), nullable = True)
    brand = db.Column(db.String(50), nullable = True)
    code = db.Column(db.String(50), unique=True)
    cameras = db.relationship('Camera', backref='fridge')
    items = db.relationship('Item', backref='fridge')
    users = db.relationship('User', secondary=fridge_user, back_populates='fridges')
    
    def as_dict(self):
        return{
            "id": self.id,
            "model": self.model,
            "brand": self.brand,
            "code": self.code,
            "cameras": self.cameras,
            "items": self.items,
            "users": self.users,
        }
    

class FridgeLog(db.Model):
    __tablename__ = "fridgelog"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = True)
    description = db.Column(db.String(500), nullable = True)

    def as_dict(self):
        return{
            "id": self.id,
            "item_id": self.item_id,
            "user_id": self.user_id,
            "description": self.description
        }
    
