from io import BytesIO
import shutil
from flask import Flask, request, render_template, jsonify, send_from_directory
from ultralytics import YOLO
import os
import cv2
from sklearn.metrics.pairwise import cosine_similarity
from transformers import CLIPProcessor, CLIPModel
import torch
import cloudinary
import requests
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from dotenv import load_dotenv


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'results'

# Load YOLO and CLIP models
model = YOLO("yolov8x-seg.pt")
clip_model = CLIPModel.from_pretrained("clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("clip-vit-base-patch32")
load_dotenv()

cloudinary.config(
    CLOUD_NAME=os.getenv("CLOUDINARY_CLOUD_NAME"),
    API_KEY=os.getenv("CLOUDINARY_API_KEY"),
    API_SECRET=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

print("Cloudinary Config:", cloudinary.config().api_key, cloudinary.config().api_secret, cloudinary.config().cloud_name)
print("Cloudinary Config Before Upload:")
print("Cloud Name:", cloudinary.config().cloud_name)
print("API Key:", cloudinary.config().api_key)
print("API Secret:", cloudinary.config().api_secret)


# Function to enhance image contrast
def enhance_contrast(img, alpha=3.0, beta=30):
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)


# Function to extract CLIP features
def extract_features(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    inputs = clip_processor(images=image, return_tensors="pt")
    with torch.no_grad():
        features = clip_model.get_image_features(**inputs)
    return features.cpu().numpy().flatten()

def extract_items(image_path, model, fridge_id):
    items_metadata = []

    try:
        img = cv2.imread(image_path)
        img_contrast = enhance_contrast(img)
        results = model(img_contrast)

        for i, box in enumerate(results[0].boxes):
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            class_id = int(box.cls)
            class_name = results[0].names[class_id]

            cropped_img = img[y1:y2, x1:x2]

            # Guardar la imagen temporalmente
            temp_image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{class_name}_{i+1}.jpg")
            cv2.imwrite(temp_image_path, cropped_img)

            # Subir a Cloudinary
            response = cloudinary.uploader.upload(
                temp_image_path,
                folder=f"Fridges/{fridge_id}/Fragments",
                public_id=f"{class_name}_{i+1}"
            )
            items_metadata.append({
                "name": class_name,
                "image_url": response.get("url"),
                "fridge_id": fridge_id
            })
            os.remove(temp_image_path)
            print("ITEM METADATA:", items_metadata)
    except Exception as e:
        print(f"Error processing fragments: {e}")

    return items_metadata

    #     output_path = os.path.join(output_folder, f"{class_name}_{i+1}.jpg")
    #     cv2.imwrite(output_path, cropped_img)

    #     features = extract_features(cropped_img)
    #     items.append({'name': class_name, 'features': features, 'cropped_img': output_path})

    # return items


# Function to compare items between two sets
def compare_items(items1, items2, similarity_threshold=0.75):
    added_items = []
    removed_items = []

    for item2 in items2:
        match_found = False
        for item1 in items1:
            if item1['name'] == item2['name']:
                similarity = cosine_similarity([item1['features']], [item2['features']])[0, 0]
                if similarity > similarity_threshold:
                    match_found = True
                    break
        if not match_found:
            added_items.append(item2)

    for item1 in items1:
        match_found = False
        for item2 in items2:
            if item1['name'] == item2['name']:
                similarity = cosine_similarity([item1['features']], [item2['features']])[0, 0]
                if similarity > similarity_threshold:
                    match_found = True
                    break
        if not match_found:
            removed_items.append(item1)

    return added_items, removed_items


@app.route('/')
def index():
    return render_template('index_dynamic.html')


@app.route('/upload', methods=['POST'])
def upload():
    """
    Process an image, fragment items, and send their data to the backend.

    Body Params:
        - image_url (str): URL of the image in Cloudinary.
        - fridge_id (int): ID of the fridge.

    Returns:
        JSON with the results of the operation.
    """
    data = request.json
    image_url = data.get('image_url')
    fridge_id = data.get('fridge_id')

    print("Processing image:", image_url)
    print("Fridge ID:", fridge_id)
    if not image_url or not isinstance(image_url, str):
        return jsonify({'error': 'Invalid "image_url"'}), 400

    if not fridge_id or not isinstance(fridge_id, int):
        return jsonify({'error': 'Invalid "fridge_id"'}), 400

    try:
        # Descargar la imagen desde la URL
        response = requests.get(image_url)
        if response.status_code != 200:
            return jsonify({'error': 'No se pudo descargar la imagen'}), 400

        # Guardar temporalmente la imagen
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.jpg')
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        with open(image_path, 'wb') as f:
            f.write(response.content)

        # Extraer y subir los fragmentos
        items_metadata = extract_items(image_path, model, fridge_id)

        # Enviar los datos al backend
        backend_url = "http://127.0.0.1:5001/items/add_batch"
        backend_response = requests.post(backend_url, json={"items": items_metadata})
        
        if backend_response.status_code != 200:
            return jsonify({
                'error': 'Error al enviar los datos al backend',
                'details': backend_response.text
            }), backend_response.status_code

        return jsonify({'fragment_urls': [item['image_url'] for item in items_metadata]})

    except Exception as e:
        return jsonify({'error': 'Error al procesar la imagen', 'details': str(e)}), 500

# @app.route('/upload', methods=['POST'])
# def upload():
#     if 'image1' not in request.files or 'image2' not in request.files:
#         return jsonify({'error': 'Both images are required!'}), 400

#     image1 = request.files['image1']
#     image2 = request.files['image2']

#     if image1.filename == '' or image2.filename == '':
#         return jsonify({'error': 'Both images must have valid filenames!'}), 400

#     os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
#     image1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image1.jpg')
#     image2_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image2.jpg')

#     image1.save(image1_path)
#     image2.save(image2_path)

#     # Create result folders for added and removed items
#     added_folder = os.path.join(app.config['RESULT_FOLDER'], 'added')
#     removed_folder = os.path.join(app.config['RESULT_FOLDER'], 'removed')
#     os.makedirs(added_folder, exist_ok=True)
#     os.makedirs(removed_folder, exist_ok=True)

#     # Extract items from both images
#     items1 = extract_items(image1_path, os.path.join(app.config['RESULT_FOLDER'], 'image1'), model)
#     items2 = extract_items(image2_path, os.path.join(app.config['RESULT_FOLDER'], 'image2'), model)

#     added_items, removed_items = compare_items(items1, items2)

#     # Save added items in the "added" folder
#     for i, item in enumerate(added_items):
#         output_path = os.path.join(added_folder, f"{item['name']}_{i+1}.jpg")
#         cropped_img_path = item['cropped_img']
#         cropped_img = cv2.imread(cropped_img_path)
#         cv2.imwrite(output_path, cropped_img)

#     # Save removed items in the "removed" folder
#     for i, item in enumerate(removed_items):
#         output_path = os.path.join(removed_folder, f"{item['name']}_{i+1}.jpg")
#         cropped_img_path = item['cropped_img']
#         cropped_img = cv2.imread(cropped_img_path)
#         cv2.imwrite(output_path, cropped_img)

#     # Return paths to display images on the web
#     added_images = [os.path.join('results', 'added', f"{item['name']}_{i+1}.jpg") for i, item in enumerate(added_items)]
#     removed_images = [os.path.join('results', 'removed', f"{item['name']}_{i+1}.jpg") for i, item in enumerate(removed_items)]
#     available_items = [os.path.join('results', 'image2', f"{item['name']}_{i+1}.jpg") for i, item in enumerate(items2)]

#     return jsonify({
#         'added_items': [item['name'] for item in added_items],
#         'removed_items': [item['name'] for item in removed_items],
#         'added_images': added_images,
#         'removed_images': removed_images,
#         'available_items': available_items
#     })

@app.after_request
def cleanup_temp_files(response):
    """
    Limpia la carpeta de imágenes temporales después de cada solicitud.
    """
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        shutil.rmtree(app.config['UPLOAD_FOLDER'])
    return response

@app.route('/results/<folder>/<filename>')
def serve_result(folder, filename):
    return send_from_directory(os.path.join(app.config['RESULT_FOLDER'], folder), filename)


if __name__ == '__main__':
    app.run(debug=True)
