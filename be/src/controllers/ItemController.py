from . import ControllerObject
from datetime import datetime, date
from src import app, db
from src.models.item import Item

def GetAllItems():
    items = Item.query.all()
    return ControllerObject(
        payload=[items.as_dict() for item in items], status=200)

def GetItemsByFridgeId(fridge_id):
    items = Item.query.filter_by(fridge_id=fridge_id).all()
    return ControllerObject(
        payload=[item.as_dict() for item in items], status=200)
