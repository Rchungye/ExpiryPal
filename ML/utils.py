import cv2
from io import BytesIO
import torch
import cloudinary.uploader
import os
import requests

def enhance_contrast(img, alpha=3.0, beta=30):
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

def extract_features(image, clip_model, clip_processor):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    inputs = clip_processor(images=image, return_tensors="pt")
    with torch.no_grad():
        features = clip_model.get_image_features(**inputs)
    return features.cpu().numpy().flatten()

def extract_items(image_path, model, fridge_id, clip_model, clip_processor):
    img = cv2.imread(image_path)
    img_contrast = enhance_contrast(img)
    results = model(img_contrast)

    items_metadata = []

    for i, box in enumerate(results[0].boxes):
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        class_id = int(box.cls)
        class_name = results[0].names[class_id]

        cropped_img = img[y1:y2, x1:x2]

        # Convert cropped image to bytes for Cloudinary upload
        _, img_encoded = cv2.imencode('.jpg', cropped_img)
        image_bytes = BytesIO(img_encoded.tobytes())

        folder_path = f"Fridges/{fridge_id}/cropped_items"
        try:
            response = cloudinary.uploader.upload(
                file=image_bytes,
                folder=folder_path,
                public_id=f"{class_name}_{i+1}"
            )
            items_metadata.append({
                "name": class_name,
                "image_url": response.get("url"),
                "fridge_id": fridge_id
            })
        except Exception as e:
            print(f"Error uploading fragment {class_name}_{i+1}: {e}")

    return items_metadata

def upload_to_cloudinary(file_path, folder_name):
    response = cloudinary.uploader.upload(file_path, folder=folder_name)
    return response['secure_url']

def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
    else:
        raise Exception(f"Failed to download image from {url}")
