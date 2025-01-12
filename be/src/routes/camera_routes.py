from src import app, scheduler, db
import json
import requests
from flask import g, jsonify, request
from src.models.user import User
from src.controllers import (
    CamaraController as Camera,
    ItemController as Item,
    HASSController as HASS
)
ml_endpoint = "http://127.0.0.1:5000/"


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
        return jsonify({"status": 400, "message": "Faltan parámetros necesarios."})
    
    resultado = HASS.obtener_url_camara(entity_id, base_url)
    return jsonify(resultado)

@scheduler.task("interval", id="actualizar_url_camara", minutes=1)
def actualizar_url_camara_task():
    """
    Scheduled task to process cameras, upload images to Cloudinary, 
    and send the images to the ML model.
    """
    with app.app_context():
        if not is_any_user_linked_to_a_fridge():
            print("No users linked to any fridge. Skipping task.")
            return

        users = User.query.all()
        for user in users:
            if not user.fridges:
                continue

            for fridge in user.fridges:
                print(f"Processing fridge {fridge.id} for user {user.id}")
                camera = Camera.get_camera_by_fridge(fridge.id)
                if not camera:
                    print(f"No camera found for fridge {fridge.id}.")
                    continue
                
                
                base_url = "https://hass.mdu-smartroom.se"
                result = Camera.upload_last_picture_from_fridgeCam_to_cloudinary(camera.entity_id, base_url, fridge.id)

                if result.get("status") != 200:
                    print(f"Error uploading last picture taken from camera {camera.id} of fridge {fridge.id} to cloudinary: {result.get('message')}")
                    continue  

                uploaded_url = result.get("uploaded_url")
                if not uploaded_url:
                    print(f"Error: uploaded_url is missing in the response for fridge {fridge.id}")
                    continue

                # print(f"Image from camera {camera.id} of fridge {fridge.id} successfully uploaded to cloudinary: {uploaded_url}")
                
                if not uploaded_url:
                    print(f"New image URL not found for fridge {fridge.id}. Skipping.")
                    continue
                # print(f"New image URL: {uploaded_url}")
                
                items_in_fridge = Item.getItemsByFridgeId(fridge.id)
                
                if not items_in_fridge["payload"]:
                    # print(f"No items found in fridge {fridge.id}. Uploading found items")
                    ml_payload = {
                        "fridge_id": fridge.id,
                        "camera_id": camera.id,
                        "last_img_url": uploaded_url
                    }
                    upload_cropped_items_if_first_time(ml_payload)
                    return
                else:
                  #  print(f"Items found in fridge {fridge.id}... \n {items_in_fridge}\n\n")
                    # Enviar ambas imágenes al modelo ML
                    ml_payload = {
                        "last_img_url": uploaded_url,
                        "items_in_fridge": items_in_fridge,
                        "fridge_id": fridge.id
                    }

                    ml_result = Camera.compare_items(ml_payload)

                    if ml_result.get("status") == "error":
                        print(f"Error sending image pair to ML model: {ml_result.get('message')}")
                    else:
                        print(f"ML model processed image pair for fridge {fridge.id}: {ml_result}")
        
@staticmethod
def upload_cropped_items_if_first_time(payload):
    """
    Upload cropped items to Cloudinary if it is the first time the fridge is being used.

    Args:
        payload (dict): Contains 'items', 'fridge_id', and 'camera_id'.

    Returns:
        dict: Response from Cloudinary.
    """
    fridge_id = payload.get("fridge_id")
    camera_id = payload.get("camera_id")

    if  not fridge_id or not camera_id:
        return {"status": 400, "message": "Missing required parameters"}

    last_picture_taken_from_fridge = Camera.get_last_picture_url(camera_id)
    
    if last_picture_taken_from_fridge["status"] == "error":
        return {"status": 500, "message": "Error getting last picture URL from camera"}
    
    # print("payload sent to ML: ", payload)
    try:
        response = requests.post(f"{ml_endpoint}ml/upload_items_if_first_time", json=payload)
        if response.status_code == 200:
            print("Cropped items successfully uploaded to Cloudinary.")
            return response.json()
        else:
            print(f"Error uploading cropped items to Cloudinary: {response.text}")
            return {"status": "error", "message": response.text}
    except Exception as e:
        print(f"Error uploading cropped items for the first time: {e}")
        return {"status": "error", "message": str(e)}


def is_any_user_linked_to_a_fridge():
    """
    Verifica si hay algún usuario vinculado a un refrigerador.

    Returns:
        bool: True si hay al menos un usuario vinculado, False en caso contrario.
    """
    return db.session.query(User).join(User.fridges).count() > 0


@app.route("/camera/<int:camera_id>/last_image", methods=["GET"])
def get_last_image(camera_id):
    """
    Get the last picture URL taken by a specific camera.

    Args:
        camera_id (int): The ID of the camera.

    Returns:
        JSON containing the last picture URL.
    """
    result = Camera.get_last_picture_url(camera_id)

    if result["status"] == "error":
        return jsonify({"error": result["message"]}), 404

    return jsonify({"last_picture_url": result["last_picture_url"]}), 200

    # def send_to_ml(image_url):
    #     """
    #     Envía la URL de la imagen al modelo de ML.
    #     """
    #     ml_endpoint = "URL_DEL_ENDPOINT_DEL_MODELO"
    #     payload = {"image_url": image_url}
    #     headers = {"Content-Type": "application/json"}

    #     response = requests.post(ml_endpoint, json=payload, headers=headers)
    #     if response.status_code == 200:
    #         return response.json()  # Respuesta del modelo (fragmentos de la imagen)
    #     else:
    #         return {"error": "Error al enviar la imagen al modelo", "status_code": response.status_code}

    # # Llamada al modelo
    # print("enviar a modelo: ", send_to_ml("https://res.cloudinary.com/dqfjzjzjg/image/upload/v1630040196/1.jpg"))
    # model_response = Camera.enviar_a_modelo_ml(uploaded_url)
    # print(f"Respuesta del modelo: {model_response}")


