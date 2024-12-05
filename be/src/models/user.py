from src import db
from src.models.fridge import fridge_user
from secrets import token_urlsafe

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    auth_token = db.Column(db.String(255), unique=True, nullable=True)
    fridges = db.relationship('Fridge', secondary=fridge_user, back_populates='users')
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def generate_auth_token(self):
        self.auth_token = token_urlsafe(32)  # generate a 32-character token
        db.session.commit()

    