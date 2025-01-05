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
from dotenv import load_dotenv
from flask import jsonify, make_response, request
from math import floor



APP_ROOT = os.path.join(os.path.dirname(__file__), "..")
dotenv_path = os.path.join(APP_ROOT, ".env")
load_dotenv(dotenv_path)
RUNNING_SERVER_IP = os.getenv("RUNNING_SERVER_IP")


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


from datetime import datetime, timezone, timedelta
from math import floor
from flask import jsonify, make_response, request

def link_user_to_fridge(fridge_code):
    """
    Links a user to a fridge via the scanned QR code.

    Args:
        fridge_code (str): The unique code of the fridge.

    Returns:
        A message indicating the success or failure of the operation.
    """
    # Look up the fridge by its unique code
    fridge = Fridge.query.filter_by(code=fridge_code).first()
    if not fridge:
        return make_response(
            jsonify({"error": "Fridge not found"}), 
            404
        )

    # Validate that the request is not a duplicate
    now = datetime.now(timezone.utc)
    if fridge.last_link_attempt:
        # Ensure last_link_attempt is timezone-aware
        last_attempt = fridge.last_link_attempt
        if last_attempt.tzinfo is None:  # If naive, make it timezone-aware
            last_attempt = last_attempt.replace(tzinfo=timezone.utc)
        
        # Calculate time difference in whole seconds
        time_diff = (now - last_attempt).total_seconds()
        print(f"Time difference (seconds): {time_diff}")
        
        if time_diff < 5:
            print("Duplicate request detected")
            return make_response(
                jsonify({
                    "error": f"Duplicate request detected. Please wait {5 - floor(time_diff)} seconds."
                }), 
                429
            )

    # Get the user from the auth token
    auth_token = request.cookies.get('auth_token')
    user = None
    if auth_token:
        user = User.query.filter_by(auth_token=auth_token).first()

    # If the user does not exist, create a new one
    if not user:
        user = User(username="ExpiryUser")
        user.generate_auth_token()
        db.session.add(user)
        db.session.commit()

    # Link the user to the fridge
    if fridge not in user.fridges:
        user.fridges.append(fridge)
        # Update the last link attempt after a successful process
        fridge.last_link_attempt = now
        db.session.commit()
    else:
        return make_response(
            jsonify({"message": "User is already linked to this fridge"}), 
            200
        )

    # Generate a response with the auth token
    response = make_response(
        jsonify({"message": "User successfully linked to fridge", "auth_token": user.auth_token}), 
        200
    )

    max_age_6_months = 60 * 60 * 24 * 30 * 6
    # samesite needs to be evaluated
    # http only needs to be changed to True, but it is False for testing purposes

    response.set_cookie(
    'auth_token',
    user.auth_token,
    httponly=True,   # La cookie no es accesible desde JavaScript
    samesite='None', # Permite el uso en sitios cruzados
    secure=False,    # Desactiva 'secure' para permitir HTTP
    max_age=60 * 60 * 24 * 30 * 6  # 6 meses
)

    
    # response.set_cookie(
    # 'auth_token',
    # user.auth_token,
    # httponly=True,  # Solo accesible desde el backend
    # secure=True,  # Requiere HTTPS
    # samesite='None',  # Permite el uso cross-origin
    # max_age=60 * 60 * 24 * 30 * 6  # 6 meses


    return response


@app.route('/check_link', methods=['GET'])
def check_user_link():
    """
    Verifica si el usuario ya está vinculado a un refrigerador.
    """
    auth_token = request.cookies.get('auth_token')
    if not auth_token:
        return jsonify({"isLinked": False}), 200

    # Busca el usuario por auth_token
    user = User.query.filter_by(auth_token=auth_token).first()
    if not user:
        return jsonify({"isLinked": False}), 200

    # Comprueba si el token coincide y está vinculado a al menos un refrigerador
    if user.auth_token != auth_token or not user.fridges:
        return jsonify({"isLinked": False}), 200

    return jsonify({"isLinked": True}), 200


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
