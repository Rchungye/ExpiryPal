from src.models.user import User
from . import ControllerObject
from datetime import datetime, timezone, timedelta
from src import app, db
from src.models.fridge import Fridge, fridge_user
from src.models.camera import Camera
from src.models.user import User
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


def get_user_from_cookie(auth_token):
    """
    Obtiene al usuario decodificando el JWT de la cookie.
    """
    if not auth_token:
        print("No auth_token provided")
        return None
    user_payload = User.decode_jwt(auth_token)
    print(user_payload)
    user_id = user_payload.get("user_id")
    if not user_id:
        print("Invalid or expired token")
        return None
    user = User.query.get(user_id)
    if not user:
        print(f"User not found for user_id: {user_id}")
    return user


def is_duplicate_request(auth_token):
    """
    Verifica si la solicitud es duplicada basándose en el `iat` del JWT.
    """
    user_id = User.decode_jwt(auth_token)
    if not user_id:
        return False
    payload = User.decode_jwt(auth_token)
    last_attempt = payload.get("iat")
    if not last_attempt:
        return False
    now = int(datetime.now(timezone.utc).timestamp())
    if now - last_attempt < 5:
        return True  # Es duplicada
    return False


def link_user_to_fridge(fridge_code):
    """
    Vincula al usuario con el refrigerador mediante un código QR.
    """
    print(f"Linking user to fridge with code: {fridge_code}")
    # Verifica que el refrigerador existe
    fridge = Fridge.query.filter_by(code=fridge_code).first()
    if not fridge:
        print("Fridge not found")
        return make_response(jsonify({"error": "Fridge not found"}), 404)
    user = User(username="ExpiryUser")
    db.session.add(user)
    db.session.commit()
    print("User created")
    # Genera un nuevo JWT para el usuario
    auth_token = User.generate_auth_token(user)
    user.auth_token = auth_token
    db.session.commit()

    # Verifica solicitudes duplicadas
    # if is_duplicate_request(auth_token):
    #     print("Duplicate request detected")
    #     return make_response(jsonify({"error": "Duplicate request detected"}), 429)

    # Vincula el usuario al refrigerador si no está ya vinculado
    if fridge not in user.fridges:
        user.fridges.append(fridge)
        db.session.commit()
    else:
        return make_response(jsonify({"message": "Already linked"}), 200)

    # Devuelve una respuesta con la cookie del auth_token
    response = make_response(jsonify({"message": "Linked successfully"}), 200)
    response.set_cookie(
        'auth_token',
        user.auth_token,
        httponly=True,
        samesite='None',
        secure=True,
        max_age=60 * 60 * 24 * 30 * 6  # 6 meses
    )
    return response


def GetAllFridges():
    fridges = Fridge.query.all()
    return fridges


def get_user_by_fridge(fridge_id):
    """
    Obtiene los usuarios asociados a un refrigerador (por su fridge_id).
    """
    # Buscar el refrigerador por su id
    fridge = Fridge.query.get(fridge_id)
    if fridge:
        # Devuelve la lista de usuarios asociados a este refrigerador
        return fridge.users  # Esto devuelve la lista de objetos 'User'
    else:
        return None  # Si no se encuentra el refrigerador


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
