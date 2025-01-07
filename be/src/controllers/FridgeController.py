from src.models.user import User
from . import ControllerObject
from datetime import datetime, timezone, timedelta
from src import app, db
from src.models.fridge import Fridge, fridge_user
from src.models.camera import Camera
import qrcode
from io import BytesIO
import base64
import os
import jwt
from dotenv import load_dotenv
from flask import jsonify, make_response, request
from math import floor
from sqlalchemy.orm import joinedload


APP_ROOT = os.path.join(os.path.dirname(__file__), "..")
dotenv_path = os.path.join(APP_ROOT, ".env")
load_dotenv(dotenv_path)
RUNNING_SERVER_IP = os.getenv("RUNNING_SERVER_IP")
SECRET_KEY = "a70bdb3ac58cedf0a4e0a13836ee06c3ee9d73ec0ffdef981b27dabf119495ca"

def get_user_from_cookie():
    """
    Obtiene al usuario decodificando el JWT de la cookie.
    """
    auth_token = request.cookies.get('auth_token')
    if not auth_token:
        return None

    user_id = decode_jwt(auth_token)
    if not user_id:
        return None

    return User.query.get(user_id)

def is_duplicate_request(auth_token):
    """
    Verifica si la solicitud es duplicada basándose en el `iat` del JWT.
    """
    user_id = decode_jwt(auth_token)
    if not user_id:
        return False

    payload = jwt.decode(auth_token, SECRET_KEY, algorithms=["HS256"])
    last_attempt = payload.get("iat")
    if not last_attempt:
        return False

    now = int(datetime.utcnow().timestamp())
    if now - last_attempt < 5:
        return True  # Es duplicada
    return False

def generate_jwt(user_id):
    """
    Genera un token JWT con un nuevo `iat`.
    """
    payload = {
        "user_id": user_id,
        "iat": int(datetime.utcnow().timestamp()),  # Marca de tiempo actual
        "exp": datetime.utcnow() + timedelta(days=180)  # Expira en 6 meses
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_jwt(token):
    """
    Decodifica el JWT para obtener el ID del usuario.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def link_user_to_fridge(fridge_code):
    """
    Vincula al usuario con el refrigerador mediante un código QR.
    """
    fridge = Fridge.query.filter_by(code=fridge_code).first()
    if not fridge:
        return make_response(jsonify({"error": "Fridge not found"}), 404)

    auth_token = request.cookies.get('auth_token')
    if not auth_token:
        return make_response(jsonify({"error": "Authentication required"}), 401)

    if is_duplicate_request(auth_token):
        return make_response(jsonify({"error": "Duplicate request detected"}), 429)

    user = get_user_from_cookie()
    if not user:
        user = User(username="ExpiryUser")
        db.session.add(user)
        db.session.commit()

    # Actualiza el JWT con un nuevo `iat`
    user.auth_token = generate_jwt(user.id)
    db.session.commit()

    if fridge not in user.fridges:
        user.fridges.append(fridge)
        db.session.commit()
    else:
        return make_response(jsonify({"message": "Already linked"}), 200)

    response = make_response(jsonify({"message": "Linked successfully"}), 200)
    response.set_cookie(
        'auth_token',
        user.auth_token,
        httponly=True,
        samesite='None',
        secure=True,
        max_age=60 * 60 * 24 * 30 * 6
    )
    return response


def GetAllFridges():
    fridges = Fridge.query.all()
    return ControllerObject(
        payload=[fridges.as_dict() for Fridge in fridges], status=200)

@staticmethod
def GetCamerasByFridgeId(fridge_id):
    """
    Retrieves cameras associated with a specific fridge.

    Args:
        fridge_id (int): The ID of the fridge.

    Returns:
        ControllerObject: An object containing the camera data and status code.
    """

    cameras = Camera.query.filter_by(fridge_id=fridge_id).all()
    return ControllerObject(
        payload=[camera.as_dict() for camera in cameras], status=200
    )

def GetNotificationPreferencesByFridgeId(fridge_id):
    fridge = Fridge.query.filter_by(id=fridge_id).first()
    if not fridge:
        return ControllerObject(
            payload={"error": "Fridge not found"},
            status=404
        )

    preferences = {}
    return ControllerObject(
        payload=preferences,
        status=200
    )


def GetFridgeQr(fridge_code):
    """
    Generates a QR code for a given fridge. The QR contains a URL
    that links to the fridge with its unique code.

    Args:
        fridge_code (str): The unique code of the fridge.

    Returns:
        ControllerObject: Contains the QR code path and URL.
    """
    # Validate fridge existence
    fridge = Fridge.query.filter_by(code=fridge_code).first()
    if not fridge:
        return ControllerObject(
            payload={"error": "Fridge not found"},
            status=404
        )

    # Generate the QR code URL
    qr_url = f"{RUNNING_SERVER_IP}/link?code={fridge_code}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)

    # Save the QR code
    qr_code_dir = os.path.join(os.path.dirname(__file__), "../qrcodes")
    os.makedirs(qr_code_dir, exist_ok=True)
    save_path = os.path.join(qr_code_dir, f"{fridge_code}.png")
    qr.make_image(fill_color="black", back_color="white").save(save_path)

    return ControllerObject(
        payload={"qr_code_path": save_path, "qr_url": qr_url},
        status=200
    )


def get_user_fridge_id(auth_token):
    """
    Obtiene el fridge_id vinculado al usuario basado en el auth_token.

    Args:
        auth_token (str): Token de autenticación del usuario.

    Returns:
        int: ID del refrigerador vinculado al usuario.
    """
    user = User.query.filter_by(auth_token=auth_token).first()
    if not user or not user.fridges:
        return None  # El usuario no está vinculado a ningún refrigerador
    return user.fridges[0].id  # Retorna el primer refrigerador vinculado (puedes manejar múltiples si es necesario)
