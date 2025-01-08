from src.models.user import User
from src import app
import json
from flask import jsonify, request
from src.controllers import (
    FridgeController as Fridge,
)


@app.route("/fridge/all", methods=["GET"])
def GetAllFridges():
    result = Fridge.GetAllFridges()
    return result.jsonify()

@app.route("/fridges/<int:fridge_id>/cameras", methods=["GET"])
def GetCamerasByFridgeId(fridge_id):
    """
    Route handler for GET /fridges/<fridge_id>/cameras

    Retrieves cameras associated with a specific fridge.

    Args:
        fridge_id (int): The ID of the fridge in the URL path.

    Returns:
        JSON: A JSON response containing the camera data and status code.
    """

    result = Fridge.GetCamerasByFridgeId(fridge_id)
    return jsonify(result)

@app.route("/fridges/<int:fridge_id>/notificationPreferences", methods=["GET"])
def GetNotificationPreferencesByFridgeId(fridge_id):
    """
    Route handler for GET /fridges/<fridge_id>/notificationPreferences

    Retrieves the notification preferences for a specific fridge.

    Args:
        fridge_id (int): The ID of the fridge in the URL path.

    Returns:
        JSON: A JSON response containing the notification preferences data and status code.
    """

    result = Fridge.GetNotificationPreferencesByFridgeId(fridge_id)
    return result.jsonify()

@app.route('/link', methods=['GET'])
def link_user_to_fridge_route():
    """
    Links a user to a fridge via the scanned QR code.
    """
    fridge_code = request.args.get('code')  # Obtén el código del QR

    # Valida que el código esté presente
    if not fridge_code:
        return {
            "error": "Fridge code not provided",
            "status": 400
        }, 400

    # Llama a la lógica para vincular usuario y nevera
    result = Fridge.link_user_to_fridge(fridge_code)  
    return result
    

@app.route('/fridges/<string:fridge_code>/qr', methods=['GET'])
def GetFridgeQr(fridge_code):
    """
    Route to generate a QR code for a specific fridge.

    Args:
        fridge_code (str): The unique code of the fridge.

    Returns:
        JSON: A JSON response containing the Base64 encoded QR code image.
    """
    result = Fridge.GetFridgeQr(fridge_code)
    return result.jsonify()


@app.route('/check_link', methods=['GET'])
def check_user_link():
    """
    Verifica si el usuario ya está vinculado a un refrigerador.
    """
    auth_token = request.cookies.get('auth_token')
    print("\n\n\n***********************************")
    print(auth_token)

    user = Fridge.get_user_from_cookie(auth_token)
    print("\n\n\n***********************************")
    print(user)
    if not user or not user.fridges:
        return jsonify({"is not Linked": False}), 400

    return jsonify({"isLinked": True}), 200
