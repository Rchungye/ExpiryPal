from . import ControllerObject
from datetime import datetime, date
from src import app, db
from src.models.notificationPreferences import NotificationPreferences as np

def GetAllNotificationPreferences():
    nps = np.query.all()
    return ControllerObject(
        payload=[nps.as_dict() for np in nps], status=200)

# np = notificationPreferences
# nps = notificationPreferences.query.all()