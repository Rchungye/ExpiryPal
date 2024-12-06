
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


@app.route("/notificationPreferences", methods=["POST", "PUT"])
def handle_notification_preferences():
    data = request.get_json()
    response, status_code = np.save_preferences(data)
    return jsonify(response), status_code