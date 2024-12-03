from src import app
import json
from flask import jsonify, request
from src.controllers import (
    fridgeController as Fridge,
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
    return jsonify(result)