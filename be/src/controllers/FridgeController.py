from src.models.user import User
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

def GetNotificationPreferencesByFridgeId(fridge_id):
    fridge = Fridge.query.filter_by(id=fridge_id).first()
    if not fridge:
        return ControllerObject(
            payload={"error": "Fridge not found"},
            status=404
        )

    preferences = {}
    return ControllerObject(
        payload=preferences,
        status=200
    )

def link_user_to_fridge(code, username="Anonymous"):
    # validate the fridge code exists
    print(code)
    fridge = Fridge.query.filter_by(code=code).first()
    if not fridge:
        return ControllerObject(
            title="Error",
            mensaje="Fridge not found",
            status=404
        )
    
    # create user
    user = User(username=username)
    user.generate_auth_token()
    db.session.add(user)

    # Create the relationship between the user and the fridge
    user.fridges.append(fridge)
    db.session.commit()

    # and return the auth token
    return ControllerObject(
        title="Success",
        mensaje="User linked to fridge successfully",
        payload={"auth_token": user.auth_token},
        status=200
    )