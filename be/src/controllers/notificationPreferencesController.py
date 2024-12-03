from . import ControllerObject
from datetime import datetime, date
from src import app, db
from src.models.notificationPreferences import NotificationPreferences as np

def GetAllNotificationPreferences():
    nps = np.query.all()
    return ControllerObject(
        payload=[nps.as_dict() for np in nps], status=200)

def GetNotificationPreferencesByFridgeId(fridge_id):
    """
    Retrieves the notification preferences for a specific fridge.

    Args:
        fridge_id (int): The ID of the fridge.

    Returns:
        ControllerObject: Contains the notification preferences data and status code.
    """
    preferences = np.query.get(fridge_id)
    if preferences is None:
        return ControllerObject(
            title="Not Found",
            mensaje=f"No notification preferences found for fridge_id: {fridge_id}",
            payload=None,
            status=404
        )
    return ControllerObject(payload=preferences.as_dict(), status=200)



# np = notificationPreferences
# nps = notificationPreferences.query.all()

def save_preferences(expiration_days, unused_days, fridge_id):
    try:
        query = """
        INSERT INTO notification_preferences (fridge_id, expiration, unusedItem)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE expiration = %s, unusedItem = %s
        """
        
        db.execute(query, (fridge_id, expiration_days, unused_days, expiration_days, unused_days))
        return True
    except Exception as e:
        print(f"Error saving preferences: {e}")
        return False
