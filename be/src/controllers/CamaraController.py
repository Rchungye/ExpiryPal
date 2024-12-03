from . import ControllerObject
from datetime import datetime, date
from src import app, db
from src.models.camera import Camera

def GetAllCameras():
    cameras = Camera.query.all()
    return ControllerObject(
        payload=[camera.as_dict() for camera in cameras], status=200)
