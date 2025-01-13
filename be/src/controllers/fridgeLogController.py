from src.models.fridgeLog import FridgeLog
from src.models.item import Item
from src.models.user import User
from src import db
from . import ControllerObject


def getFridgeLog(fridge_id):
    fridge = db.session.query(Item).filter(Item.fridge_id == fridge_id).first()
    if not fridge:
        return ControllerObject(
            title="Error",
            message=f"Fridge with ID {fridge_id} does not exist.",
            payload=None,
            status=404
        ).jsonify()
    
    # bring the logs from the database
    logs = (
        db.session.query(FridgeLog, User, Item)
        .join(User, FridgeLog.user_id == User.id)
        .join(Item, FridgeLog.item_id == Item.id)
        .filter(Item.fridge_id == fridge_id)
        .order_by(FridgeLog.timestamp.desc())
        .all()
    )

    # format the logs
    result = []
    for log, user, item in logs:
        if log.action == "Changed name":
            print(log.details)

            result.append(f"{user.username} changed item name from {log.details.split(' to ')[0]} to {item.name}")
        elif log.action == "Changed expiration date":
            result.append(f"{user.username} changed {item.name} expiration date")
    
    return ControllerObject(
        title="Fridge Log",
        message="Logs retrieved successfully.",
        payload={"logs": result},
        status=200
    ).jsonify()

