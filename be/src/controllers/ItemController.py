from . import ControllerObject
from datetime import datetime, date
from src import app, db
from src.models.item import Item

def GetAllItems():
    items = Item.query.all()
    return ControllerObject(
        payload=[items.as_dict() for item in items], status=200)
