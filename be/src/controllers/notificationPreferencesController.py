from . import ControllerObject
from datetime import datetime, date
from src import app, db
from src.models.notificationPreferences import NotificationPreferences as np
from src.schemas.notificationPreferencesSchema import NotificationPreferencesSchema

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


def save_preferences(data):
    schema = NotificationPreferencesSchema()

    # validate the data received from the client
    errors = schema.validate(data)
    if errors:
        return {
            "success": False,
            "message": "Validation errors",
            "errors": errors
        }, 400

    fridge_id = data["fridge_id"]
    expiration = data["expiration"]
    unusedItem = data["unusedItem"]

    try:
        # look for existing preferences
        preferences = np.query.get(fridge_id)

        if preferences:
            # if exist, update the existing preferences
            preferences.expiration = expiration
            preferences.unusedItem = unusedItem
        else:
            # if not, create new preferences
            preferences = np(
                fridge_id=fridge_id,
                expiration=expiration,
                unusedItem=unusedItem,
            )
            db.session.add(preferences)

        db.session.commit()

        return {
            "success": True,
            "message": "Preferences saved successfully.",
            "data": preferences.as_dict()
        }, 200

    except Exception as e:
        db.session.rollback()
        print(f"Error saving preferences: {e}")
        return {
            "success": False,
            "message": "Internal server error",
            "error": str(e)
        }, 500
