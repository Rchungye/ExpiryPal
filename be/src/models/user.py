import datetime
from datetime import timedelta
from src import db
from src.models.fridge import fridge_user
from secrets import token_urlsafe
import jwt
import os
from dotenv import load_dotenv
load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    fridges = db.relationship('Fridge', secondary=fridge_user, back_populates='users')
    auth_token = db.Column(db.String(512), unique=True, nullable=True)
    fcm_token = db.Column(db.Text, nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def generate_auth_token(self):
        """
        Genera un JWT para el usuario con información relevante.
        """
        payload = {
            "user_id": self.id,  # Incluye el ID del usuario en el payload
            "iat": datetime.datetime.now().timestamp(),  # Marca de tiempo actual
            "exp": datetime.datetime.utcnow() + timedelta(days=180)  # Expira en 6 meses
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
        self.auth_token = token
        db.session.commit()
        return token

    @staticmethod
    def decode_jwt(token):
        """
        Decodifica el JWT para obtener el ID del usuario.
        """
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return None
        except jwt.InvalidTokenError:
            print("Invalid token")
            return None

