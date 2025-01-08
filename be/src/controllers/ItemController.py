from src.models.fridgeLog import FridgeLog
from . import ControllerObject
from datetime import datetime, date, timedelta, timezone
from src import app, db
from src.models.item import Item

def deleteItem(item_id):
    print("\n\nIn deleteItem function from ItemController.py")
    
    item = Item.query.get(item_id)
    if not item:
        return {"error": "Item not found"}, 404

    db.session.delete(item)
    db.session.commit()

    return {"message": "Item deleted successfully"}, 200

def add_items(payload):

    print("\n\nIn add_items function from ItemController.py")
    print(f"payload: {payload}")
    if not payload:
        return {"error": "No items to add"}, 400
        
    items = payload["items"]
    
    print(f"Adding {len(items)} items to the database")
    print (items)

    added_count = 0

    try:
        for item in items:
            name = item.get("name", "Unknown Item")
            image_url = item.get("image_url")
            fridge_id = item.get("fridge_id")

            if not image_url or not fridge_id:
                return {"error": f"Missing required parameters \n image_url:{image_url}\nfridge_id: {fridge_id}\n"}, 400
            
            existing_item = db.session.query(Item).filter_by(imageURL=image_url, fridge_id=fridge_id).first()
            if existing_item:
                print(f"Item with imageURL {image_url} already exists. Skipping...")
                continue

            new_item = Item(
                name=name,
                imageURL=image_url,
                fridge_id=fridge_id,
                expirationDate = (datetime.now(timezone.utc) + timedelta(days=5))
            )
            print(f"Adding item: {new_item}")
            db.session.add(new_item)
            added_count += 1

        db.session.commit()
        print(f"Added {added_count} items to the database")
        if added_count == 0:
            return {"message": "No new items added"}, 200

        return {"message": f"Added {added_count} items to the database"}, 200

    except Exception as e:
        db.session.rollback()
        print(f"Error during commit: {e}")
        return {"error": f"Error adding items to the database: {e}"}, 500
   

def getItemsByFridgeId(fridge_id):
    items = Item.query.filter_by(fridge_id=fridge_id).all()
    return {
        "payload": [item.as_dict() for item in items],
        "status": 200
    }



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
            details=f"'{item.name}' to '{new_name}'"
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
            details=f"'{item.expirationDate}' to '{new_expiration_date}'"
        )
        item.expirationDate = new_expiration_date
        db.session.add(log)
        db.session.commit()

    return {"message": "Item expiration date updated successfully"}, 200

def should_notify_expiration(item, today, days_before_expiration):
    """
    Verifies if an item is about to expire.
    """
    return item.expirationDate and (item.expirationDate - today).days <= days_before_expiration

def should_notify_unused(item, today, unused_days):
    """
    Verifies if an item has been unused for a certain amount of days.
    """
    return item.addedDate and (today - item.addedDate).days >= unused_days