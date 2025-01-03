from . import ControllerObject
from src import app, db
from src.models.notificationPreferences import NotificationPreferences as np
from src.schemas.notificationPreferencesSchema import NotificationPreferencesSchema
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update

def GetAllNotificationPreferences():
    return np.query.all()

def GetNotificationPreferencesByFridgeId(fridge_id):
    """
    Retrieves the notification preferences for a specific fridge.

    Args:
        fridge_id (int): The ID of the fridge.

    Returns:
        ControllerObject: Contains the notification preferences data and status code.
    """
    preferences = np.query.filter_by(fridge_id=fridge_id).first()
    if preferences is None:
        return ControllerObject(
            title="Not Found",
            message=f"No notification preferences found for fridge_id: {fridge_id}",
            payload=None,
            status=404
        )
    return ControllerObject(payload=preferences.as_dict(), status=200)

def save_preferences(data):
    """
    Saves or updates notification preferences for a fridge.
    """
    schema = NotificationPreferencesSchema()

    # Validate the data
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
        # First, try to find existing preferences
        existing = db.session.query(np).filter_by(fridge_id=fridge_id).first()
        
        if existing:
            # Update existing record using SQL UPDATE
            stmt = update(np).where(np.fridge_id == fridge_id).values(
                expiration=expiration,
                unusedItem=unusedItem
            )
            db.session.execute(stmt)
        else:
            # Create new record
            new_preferences = np(
                fridge_id=fridge_id,
                expiration=expiration,
                unusedItem=unusedItem
            )
            db.session.add(new_preferences)

        db.session.commit()
        
        # Fetch and return the updated/created record
        result = db.session.query(np).filter_by(fridge_id=fridge_id).first()
        return {
            "success": True,
            "message": "Preferences saved successfully.",
            "data": result.as_dict()
        }, 200

    except Exception as e:
        db.session.rollback()
        print(f"Error saving preferences: {e}")
        return {
            "success": False,
            "message": "Failed to save preferences",
            "error": str(e)
        }, 500