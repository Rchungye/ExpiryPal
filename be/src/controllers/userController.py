from . import ControllerObject
from datetime import datetime, date
from src import app, db
from src.models.user import User

def GetAllUsers():
    try:
        users = User.query.all()
        return ControllerObject(
            payload=[user.as_dict() for user in users],
            status=200
        )
    except Exception as e:
        return ControllerObject(
            title="Error",
            mensaje=str(e),
            status=500
        )


# np = notificationPreferences
# nps = notificationPreferences.query.all()

