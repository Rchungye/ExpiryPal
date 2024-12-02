from src import db
from src.models.Fridge import Fridge

class Camera(db.Model):
    __tablename__ = "camara"
    id = db.Column(db.Integer, primary_key=True)
    fridge_id = db.Column(db.Integer, db.ForeignKey('fridge.id'), nullable = False)
    fridge = db.relationship('Fridge')
    model = db.Column(db.String(50), nullable = True)
    brand = db.Column(db.String(50), nullable = True)
    accessURL = db.Column(db.String(2048), nullable = True)

    def as_dict(self):
        return{
            "id": self.id,
            "fridge_id": self.fridge_id,
            "fridge": self.fridge.toDict(),
            "model": self.model,
            "brand": self.brand,
            "accessURL": self.accessURL
        }