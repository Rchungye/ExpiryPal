from . import ControllerObject
from datetime import datetime, date
from src import app, db
from src.models.fridge import Fridge
from src.models.camera import Camera

def GetAllFridges():
    fridges = Fridge.query.all()
    return ControllerObject(
        payload=[fridges.as_dict() for Fridge in fridges], status=200)

@staticmethod
def GetCamerasByFridgeId(fridge_id):
    """
    Retrieves cameras associated with a specific fridge.

    Args:
        fridge_id (int): The ID of the fridge.

    Returns:
        ControllerObject: An object containing the camera data and status code.
    """

    cameras = Camera.query.filter_by(fridge_id=fridge_id).all()
    return ControllerObject(
        payload=[camera.as_dict() for camera in cameras], status=200
    )