from . import ControllerObject
from datetime import datetime, date
from src import app, db
from src.models.user import User
from flask import request, jsonify

def GetAllUsers():
    try:
        users = User.query.all()
        return ControllerObject(
            payload=[user.as_dict() for user in users],
            status=200
        )
    except Exception as e:
        return ControllerObject(
            title="Error",
            message=str(e),
            status=500
        )
    
def saveCMFToken(data, cookies):
    try:
        user_cookies = User.decode_jwt(cookies.get('auth_token'))
        print("Decoded JWT: ", user_cookies)
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    if not user_cookies:
        return jsonify({"error": "No auth token provided"}), 400

    fcm_token = data.get('token')
    if not fcm_token:
        return jsonify({"error": "Token not provided"}), 400

    user_id = user_cookies.get('user_id')
    if not user_id:
        return jsonify({"error": "Invalid user_id in saveCMFToken"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    print(f"User found: {user.as_dict()}")
    print(f"Attempting to save fcm_token: {fcm_token}")

    try:
        user.fcm_token = fcm_token
        db.session.commit()
        db.session.refresh(user)  # Refresca el estado del usuario
        print(f"CMF token successfully saved for user {user_id}: {user.cmf_token}")
        return jsonify({"message": "Token saved successfully"}), 200
    except Exception as e:
        print("Error saving CMF token:", e)
        db.session.rollback()
        return jsonify({"error": "Failed to save token"}), 500



def checkIfCMFToken(data):
    """
    Check if the current user has a FCM token saved.
    """    
    # Decodificar el auth_token
    decoded = User.decode_jwt(data.get('auth_token'))
    print("decoded: ", decoded)
    
    # Obtener user_id del token decodificado
    user_id = decoded.get('user_id')
    print("user_id: ", user_id)

    # Buscar el usuario en la base de datos
    user = User.query.filter_by(id=user_id).first()
    if not user:
        print("User not found")
        return jsonify({"error": f"User with id {user_id} not found"}), 404

    FCM_token = user.fcm_token
    if not FCM_token:
        print("FCM Token not found for user ", user_id)
        return jsonify({"error": f"FCM Token for user {user_id} not found"}), 404
    
    return jsonify({"token": FCM_token}), 200
