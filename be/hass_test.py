from homeassistant_api import Client
import os
from dotenv import load_dotenv
load_dotenv()
HASS_BASE_URL = os.getenv("HASS_BASE_URL")
HASS_API_KEY = os.getenv("HASS_API_KEY")

client = Client(HASS_BASE_URL + '/api', HASS_API_KEY)

print(client.get_entity(entity_id="camera.192_168_8_125"))
state = client.get_entity(entity_id="camera.192_168_8_125").get_state()
# print(state)
state = dict(state)
# print(state)
token = state['attributes']['access_token']
urlCam = HASS_BASE_URL + '/fridge?token=' + token
print(urlCam)


