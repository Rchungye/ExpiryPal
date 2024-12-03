from . import ControllerObject
from datetime import datetime, date
from src import app, db
from src.models.user import User

def GetAllUsers():
    users = User.query.all()
    return ControllerObject(
        payload=[users.as_dict() for user in users], status=200)

# np = notificationPreferences
# nps = notificationPreferences.query.all()