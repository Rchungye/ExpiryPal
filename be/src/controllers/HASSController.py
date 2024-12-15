from homeassistant_api import Client
import os
from dotenv import load_dotenv
load_dotenv()


client = Client(
    'https://hass.mdu-smartroom.se/api',
    os.getenv("HASS_API_KEY")
)


state = client.get_entity(entity_id="camera.192_168_8_125").get_state()
state = dict(state)
token = state['attributes']['access_token']
urlCam = 'https://hass.mdu-smartroom.se/fridge?token='
urlCam = urlCam + token

def get_camera_url(entity_id: str, base_url: str):
    """
    Generates the camera URL from Home Assistant.

    Args:
        entity_id (str): camera entity ID.
        base_url (str): Home Assistant server base URL.

    Returns:
        A dictionary containing the status, message, and camera URL.
    """
    ret = {"status": 400, "message": "", "url": ""}
    try:
        client = Client(f"{base_url}/api", os.getenv("HASS_API_KEY"))
        state = client.get_entity(entity_id=entity_id).get_state()
        token = state.attributes["access_token"]
        ret["url"] = f"{base_url}/fridge?token={token}"
        ret["status"] = 200
        ret["message"] = "Camera URL obtained successfully."
    except Exception as err:
        ret["message"] = f"Error while obtaining camera URL. {err}"
    return ret