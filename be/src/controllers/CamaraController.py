from flask import g, jsonify
from src.controllers.HASSController import get_camera_url
from . import ControllerObject
from datetime import datetime, date
from src import app, db
from src.models.camera import Camera
import cloudinary
import cloudinary.uploader
import requests
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from io import BytesIO


APP_ROOT = os.path.join(os.path.dirname(__file__), "..")
dotenv_path = os.path.join(APP_ROOT, ".env")
load_dotenv(dotenv_path)
ML_URL = os.getenv("ML_URL")


def GetAllCameras():
    cameras = Camera.query.all()
    return ControllerObject(
        payload=[camera.as_dict() for camera in cameras], status=200)


def get_camera_by_fridge(fridge_id):
    """
    Obtiene el objeto de la cámara asociada a un refrigerador.
    Args:
        fridge_id (int): ID del refrigerador.
    Returns:
        Camera: Objeto de la cámara asociada al refrigerador o None si no existe.
    """
    return Camera.query.filter_by(fridge_id=fridge_id).first()


def get_entity_id_by_fridge(fridge_id):
    """
    Obtiene el ID de la entidad de la cámara asociada a un refrigerador.
    Args:
        fridge_id (int): ID del refrigerador.
    Returns:
        str: ID de la entidad de la cámara asociada.
    """
    camera = Camera.query.filter_by(fridge_id=fridge_id).first()
    return camera.entity_id if camera else None


def takeScreenshotAsBytes(page_url):
    """
    Take a screenshot of the page using Playwright and return the bytes.
    Args:
        page_url (str): Page URL to take the screenshot from.
    Returns:
        BytesIO: Image taken as bytes.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(page_url, wait_until="networkidle")  # wait for the page to load
            screenshot_bytes = page.screenshot(path=None)  # take the screenshot
            browser.close()
        print("Screenshot taken successfully and saved in memory.")
        return BytesIO(screenshot_bytes)  # return the image as bytes
    except Exception as err:
        print(f"Error taking screenshot with Playwright: {err}")
        return None


def upload_image_to_cloudinary_from_bytes(image_bytes, fridge_id, tags=None ):
    """
    Uploads the image taken from the fridge to cloudinary 
    Args:
        image_bytes (BytesIO): Image in binary format.
        tags (list[str]): Tags to assign to the image.
    Returns:
        str: uploaded image URL.
    """
    if not isinstance(image_bytes, BytesIO):
        raise ValueError("Image obj not valid (must be BytesIO).")
    # FOLDER PATH
    folder_path = f"Fridges/{fridge_id}/ImagesFromFridge"
    try:
        # Subir la imagen con las etiquetas
        response = cloudinary.uploader.upload(
            file=image_bytes,
            folder=folder_path,
            tags=tags  # asign tags to the image
        )
        print("Image uploaded successfully:", response.get("url"))
        return response.get("url")
    except Exception as err:
        print(f"Error uploading image to Cloudinary: {err}")
        return None


def upload_last_picture_from_fridgeCam_to_cloudinary(entity_id, base_url, fridge_id):
    """
    process the camera, take a screenshot, and upload it to Cloudinary.
    Args:
        entity_id (str): Camera entity ID.
        base_url (str): Home Assistant server base URL.
        fridge_id (str): fridge ID.
    Returns:
        dict: Resultado del procesamiento.
    """
    url_data = get_camera_url(entity_id, base_url)
    if url_data["status"] != 200:
        return {"status": 400, "message": "Camera URL not obtained."}
    if not fridge_id:
        return {"status": 400, "message": "Fridge ID no es válido."}
    
    try:
        # Capturar el pantallazo en memoria como bytes
        # print("/nTaking screenshot for fridge:", fridge_id, "from URL:", url_data["url"])
        screenshot_bytes = takeScreenshotAsBytes(url_data["url"])
        if not screenshot_bytes:
            return {"status": 500, "message": "Screenshot not captured."}
        # Subir los bytes a Cloudinary
        tags = [f"fridge_{fridge_id}", "last_image_from_fridge"]
        uploaded_url = upload_image_to_cloudinary_from_bytes(screenshot_bytes, fridge_id, tags=tags)
        if not uploaded_url:
            return {"status": 500, "message": "Error uploading image to Cloudinary."}
        Camera.last_picture_url = uploaded_url
        db.session.commit()
        
        return {"status": 200, "message": "last_picture_url updated successfully.", "uploaded_url": uploaded_url}

    except Exception as err:
        return {"status": 500, "message": f"Error updating last picture url in camera model: {err}"}


def compare_items(payload):
    """
    Send items in the fridge to the ML model for comparison with last picture taken from the fridge.
    Args:
        payload (dict): Contains 'items_in_fridge', 'last_img_url', and 'fridge_id'.
    Returns:
        dict: Response from the ML model.
    """
    for item in payload["items_in_fridge"]["payload"]:
        for key, value in item.items():
            if isinstance(value, (datetime, date)):
                item[key] = value.isoformat()  # Convertir cualquier fecha a formato ISO
    try:
        route = f'{ML_URL}ml/compare_items_from_fridge'
        response = requests.post(route, json=payload)
        if response.status_code == 200:
            print("Image comparison successfully processed by ML model.")
            return response.json()
        else:
            print(f"Error processing comparison of items in ML model: {response.text}")
            return {"status": "error", "message": response.text}
    except Exception as e:
        print(f"Error connecting to ML model: {e}")
        return {"status": "error", "message": str(e)}


def get_last_picture_url(camera_id):
    """
    Retrieve the last picture URL for a given camera.
    Args:
        camera_id (int): The ID of the camera.
    Returns:
        dict: A dictionary containing the last picture URL or an error message.
    """
    camera = Camera.query.get(camera_id)
    if not camera:
        return {"status": "error", "message": "Camera not found"}
    if not camera.last_picture_url:
        return {"status": "first_run", "message": "No previous picture available for this camera"}
    return {"status": "success", "last_picture_url": camera.last_picture_url}

