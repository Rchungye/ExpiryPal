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
    
def saveCMFToken(data, auth_token):
    print("\n\nData: ", data)
    
    # Accede al token desde el diccionario usando la clave
    token = data.get('token')  # Usa .get() para evitar errores si la clave no existe
    print("\n\nAuth Token: ", auth_token)
    if not token:
        return jsonify({"error": "Token not provided"}), 400
    
    data_payload = User.decode_jwt(token)
    print("\n\nData payload: ", data_payload)
    
    user_id = data_payload.get('user_id') if data_payload else None
    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Guarda el token FCM en la base de datos
    user.save_fcm_token(token)
    return jsonify({"message": "Token saved successfully"}), 200


def get_user_by_fridge(fridge_id):
    """
    Obtiene el usuario asociado a un refrigerador.
    """
    return User.query.filter_by(fridge_id=fridge_id).first()
