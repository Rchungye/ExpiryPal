
from src import app
import json
from flask import jsonify, request
from src.controllers import (
    notificationPreferencesController as np,
)


@app.route("/notificationPreferences/all", methods=["GET"])
def GetAllNotificationPreferences():
    result = np.GetAllNotificationPreferences()
    return result.jsonify()

@app.route("/notificationPreferences/<int:fridge_id>", methods=["GET"])
def get_notification_preferences(fridge_id):
    preferences = np.GetNotificationPreferencesByFridgeId(fridge_id)
    
    return preferences.jsonify()


@app.route("/notificationPreferences", methods=["POST"])
def save_notification_preferences():
    data = request.get_json()
    expiration = data.get("expiration")
    unusedItem = data.get("unusedItem")
    fridge_id = data.get("fridgeId")

    result = np.save_preferences(expiration, unusedItem, fridge_id)
    return result.jsonify()