from src.models.fridgeLog import FridgeLog
from . import ControllerObject
from datetime import datetime, date
from src import app, db
from src.models.item import Item

def GetItemsByFridgeId(fridge_id):
    items = Item.query.filter_by(fridge_id=fridge_id).all()
    return ControllerObject(
        payload=[item.as_dict() for item in items], status=200)

def updateItemName(item_id, user_id, new_name):
    item = Item.query.get(item_id)
    if not item:
        return {"error": "Item not found"}, 404

    if new_name != item.name:
        # Register the change in FridgeLog
        log = FridgeLog(
            item_id=item.id,
            user_id=user_id,
            action="Changed name",
            details=f"From '{item.name}' to '{new_name}'"
        )
        item.name = new_name
        db.session.add(log)
        db.session.commit()

    return {"message": "Item name updated successfully"}, 200


def updateItemExpirationDate(item_id, user_id, new_expiration_date):
    item = Item.query.get(item_id)
    if not item:
        return {"error": "Item not found"}, 404

    if new_expiration_date != item.expirationDate:
        # Register the change in FridgeLog
        log = FridgeLog(
            item_id=item.id,
            user_id=user_id,
            action="Changed expiration date",
            details=f"From '{item.expirationDate}' to '{new_expiration_date}'"
        )
        item.expirationDate = new_expiration_date
        db.session.add(log)
        db.session.commit()

    return {"message": "Item expiration date updated successfully"}, 200
