from src import db

class Camera(db.Model):
    __tablename__ = "camera"
    id = db.Column(db.Integer, primary_key=True)
    fridge_id = db.Column(db.Integer, db.ForeignKey('fridge.id'))
    model = db.Column(db.String(50))
    brand = db.Column(db.String(50))
    accessURL = db.Column(db.String(2048))
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}