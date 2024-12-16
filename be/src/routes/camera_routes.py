from src import app, scheduler, db
import json
import requests
from flask import g, jsonify, request
from src.models.user import User
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

                # Obtener la última URL antes de actualizar
                last_image_result = Camera.get_last_picture_url(camera.id)
                if last_image_result.get("status") != "success":
                    print(f"Error retrieving last image for camera {camera.id}: {last_image_result.get('message')}")
                    last_image_url = None
                else:
                    last_image_url = last_image_result.get("last_picture_url")

                # Procesar la cámara y actualizar el URL
                base_url = "https://hass.mdu-smartroom.se"
                result = Camera.procesar_camara(camera.entity_id, base_url, fridge.id)

                if result["status"] == 200:
                    print(f"Image uploaded successfully for fridge {fridge.id}: {result['uploaded_url']}")

                    # Obtener la nueva URL de la imagen
                    new_image_url = result.get("uploaded_url")
                    if not new_image_url:
                        print(f"New image URL not found for fridge {fridge.id}. Skipping.")
                        continue

                    # Si no hay imagen previa, usar la nueva imagen para ambas
                    if not last_image_url:
                        print(f"No previous image available for fridge {fridge.id}. Using the new image as both.")
                        last_image_url = new_image_url

                    print(f"Previous image URL: {last_image_url}")
                    print(f"New image URL: {new_image_url}")

                    # Enviar ambas imágenes al modelo ML
                    ml_payload = {
                        "previous_img_url": last_image_url,
                        "last_img_url": new_image_url,
                        "fridge_id": fridge.id
                    }
                    ml_result = Camera.send_image_pair_to_ml(ml_payload)
                    if ml_result.get("status") == "error":
                        print(f"Error sending image pair to ML model: {ml_result.get('message')}")
                    else:
                        print(f"ML model processed image pair for fridge {fridge.id}: {ml_result}")
                else:
                    print(f"Error for fridge {fridge.id}: {result['message']}")


@staticmethod
def send_image_pair_to_ml(payload):
    """
    Send the previous and last picture URLs of a fridge to the ML model.

    Args:
        payload (dict): Contains 'previous_img_url', 'last_img_url', and 'fridge_id'.

    Returns:
        dict: Response from the ML model.
    """
    ml_endpoint = "http://127.0.0.1:5000/upload"
    try:
        response = requests.post(ml_endpoint, json=payload)
        if response.status_code == 200:
            print("Image pair successfully processed by ML model.")
            return response.json()  # Devuelve la respuesta del modelo
        else:
            print(f"Error processing image pair in ML model: {response.text}")
            return {"status": "error", "message": response.text}
    except Exception as e:
        print(f"Error connecting to ML model: {e}")
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


