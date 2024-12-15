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
print(urlCam)


def obtener_url_camara(entity_id: str, base_url: str):
    ret = {"status": 400, "mensaje": "", "url": ""}
    try:
        client = Client(
            f"{base_url}/api",
            os.getenv("HASS_API_KEY")
        )
        state = client.get_entity(entity_id=entity_id).get_state()
        token = state.attributes["access_token"]
        ret["url"] = f"{base_url}/fridge?token={token}"
        ret["status"] = 200
        ret["mensaje"] = "URL de la cámara generada con éxito."
    except Exception as err:
        ret["mensaje"] = f"Error al obtener la URL de la cámara: {err}"
    return ret