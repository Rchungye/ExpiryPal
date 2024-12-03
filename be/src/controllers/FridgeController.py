from . import ControllerObject
from datetime import datetime, date
from src import app, db
from src.models.fridge import Fridge

def GetAllFridges():
    fridges = Fridge.query.all()
    return ControllerObject(
        payload=[fridges.as_dict() for Fridge in fridges], status=200)
