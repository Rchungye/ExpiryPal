
from src import app
import json
from flask import jsonify, request
from src.controllers import (
    ItemController as Item,
)


@app.route("/item/all", methods=["GET"])
def GetAllItems():
    result = Item.GetAllItems()
    return result.jsonify()

@app.route("/items/<int:fridge_id>", methods=["GET"])
def GetItemsByFridgeId(fridge_id):
    """
    Route handler for GET /items/<fridge_id>

    Retrieves items associated with a specific fridge.

    Args:
        fridge_id (int): The ID of the fridge in the URL path.

    Returns:
        JSON: A JSON response containing the item data and status code.
    """

    result = Item.GetItemsByFridgeId(fridge_id=fridge_id)
    return result.jsonify()

