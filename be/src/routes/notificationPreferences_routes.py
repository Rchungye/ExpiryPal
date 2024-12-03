
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

