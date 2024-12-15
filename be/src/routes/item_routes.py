
from datetime import timezone, timedelta
import datetime
from src import app, db
import json
from flask import jsonify, request
from src.models import item as Item
from src.controllers import (
    ItemController as ItemController,
)

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

    result = ItemController.GetItemsByFridgeId(fridge_id=fridge_id)
    return result.jsonify()

@app.route("/items/<int:item_id>/updateName", methods=["PUT"])
def updateItemName(item_id):
    """
    Route handler for PUT /items/<item_id>/updateName

    Updates the name of an item.

    Args:
        item_id (int): The ID of the item in the URL path.

    Returns:
        JSON: A JSON response containing the status of the update.
    """

    data = request.get_json()
    new_name = data.get("new_name")
    user_id = data.get("user_id")

    result = ItemController.updateItemName(item_id, user_id, new_name)
    return jsonify(result)

@app.route("/items/<int:item_id>/updateExpirationDate", methods=["PUT"])
def updateItemExpirationDate(item_id):
    """
    Route handler for PUT /items/<item_id>/updateExpirationDate

    Updates the expiration date of an item.

    Args:
        item_id (int): The ID of the item in the URL path.

    Returns:
        JSON: A JSON response containing the status of the update.
    """

    data = request.get_json()
    new_expiration_date = data.get("new_expiration_date") # format: "YYYY-MM-DD"
    user_id = data.get("user_id")

    # Validate the input of the expiration date
    if not new_expiration_date:
        return jsonify({"error": "Expiration date not provided"}), 400
    
    # validate the input of the user_id
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400

     # Validate the format of the expiration date
    try:
        expiration_date_obj = datetime.strptime(new_expiration_date, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. The correct format is YYYY-MM-DD."}), 400

    result = ItemController.updateItemExpirationDate(item_id, user_id, new_expiration_date)
    return jsonify(result)
from datetime import datetime, timezone, timedelta

@app.route('/items/add_batch', methods=['POST'])
def add_items_batch():
    """
    Add a batch of items to the database.

    Body Params:
        - items (list): List of item data (name, image_url, fridge_id).

    Returns:
        JSON with the result of the operation.
    """
    data = request.json
    items = data.get('items')
    print("ITEMS RECEIVED:", items)
    print("DATA RECEIVED:", data)
    if not items or not isinstance(items, list):
        return jsonify({'error': 'El parámetro "items" es requerido y debe ser una lista'}), 400

    try:
        for item_data in items:
            name = item_data.get("name", "Unknown Item")
            image_url = item_data.get("image_url")
            fridge_id = item_data.get("fridge_id")

            # Crear el ítem en la base de datos
            new_item = Item(
                name=name,
                imageURL=image_url,
                fridge_id=fridge_id,
                expirationDate=(datetime.now(timezone.utc) + timedelta(days=5))
            )
            db.session.add(new_item)

        db.session.commit()
        return jsonify({'message': f'{len(items)} items added successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al agregar los ítems', 'details': str(e)}), 500
