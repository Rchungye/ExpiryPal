
from src import app
import json
from flask import jsonify, request
from src.controllers import (
    fridgeLogController as FridgeLog,
)

@app.route('/fridges/<int:fridge_id>/logs', methods=['GET'])
def GetFridgeLog(fridge_id):
    """
    Route to get the log of changes for a fridge.

    Args:
        fridge_id (int): The ID of the fridge.

    Returns:
        JSON: A JSON response containing the formatted logs.
    """
    result = FridgeLog.getFridgeLog(fridge_id)
    return result
