from src import app, scheduler
import json
from flask import jsonify, request
from src.controllers import (
    CamaraController as Camera,
    HASSController as HASS
)


@app.route("/camera/all", methods=["GET"])
def GetAllCameras():
    result = Camera.GetAllCameras()
    return result.jsonify()


@app.route("/obtener_url_camara", methods=["GET"])
def obtener_url_camara_route():
    """
    Ruta para obtener la URL de la cámara desde Home Assistant.

    Query Params:
        - entity_id (str): ID de la entidad de la cámara.
        - base_url (str): URL base del servidor de Home Assistant.

    Returns:
        JSON con el estado de la operación y la URL de la cámara.
    """
    entity_id = request.args.get("entity_id")
    base_url = request.args.get("base_url")
    
    if not entity_id or not base_url:
        return jsonify({"status": 400, "mensaje": "Faltan parámetros necesarios."})
    
    resultado = HASS.obtener_url_camara(entity_id, base_url)
    return jsonify(resultado)


@scheduler.task("interval", id="actualizar_url_camara", minutes=0.1)
def actualizar_url_camara_task():
    """
    Tarea programada que obtiene e imprime la URL de la cámara.
    """
    entity_id = "camera.192_168_8_125"
    base_url = "https://hass.mdu-smartroom.se"
    resultado = HASS.obtener_url_camara(entity_id, base_url)

    if resultado["status"] == 200:
        print(f"URL de la cámara obtenida: {resultado['url']}")
    else:
        print(f"Error: {resultado['mensaje']}")