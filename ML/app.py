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

# Configuration       
cloudinary.config( 
    CLOUD_NAME="dqwutjyjh",
    API_KEY="132533594763411",
    API_SECRET="cW4iHQs41fcqnnOFGSyDKVQJel8",
    secure=True
)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'results'

# Load YOLO and CLIP models
model = YOLO("yolov8x-seg.pt")
clip_model = CLIPModel.from_pretrained("clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("clip-vit-base-patch32")


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

    print(f"Extracted Items Metadata: {items_metadata}")
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


# Function to upload image to Cloudinary
def upload_to_cloudinary(file_path, folder_name):
    response = cloudinary.uploader.upload(file_path, folder=folder_name)
    return response['secure_url']


@app.route('/')
def index():
    return render_template('index_dynamic.html')
@app.route('/upload', methods=['POST'])
def upload():
    """
    Process two images, fragment items from the last image, and send their data to the backend.
    """
    data = request.json
    previous_img_url = data.get('previous_img_url')
    last_img_url = data.get('last_img_url')
    fridge_id = data.get('fridge_id')

    print("DATA RECEIVED:", data)

    # Validar parámetros
    if not last_img_url or not isinstance(last_img_url, str):
        return jsonify({'error': 'Invalid "last_img_url"'}), 400

    if not fridge_id or not isinstance(fridge_id, int):
        return jsonify({'error': 'Invalid "fridge_id"'}), 400

    print("Parameters validated.")
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Descargar y guardar la última imagen
        print("Downloading last image...")
        last_response = requests.get(last_img_url)
        if last_response.status_code != 200:
            return jsonify({'error': 'Failed to download last image'}), 400

        last_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'last_image.jpg')
        with open(last_image_path, 'wb') as f:
            f.write(last_response.content)

        # Extraer ítems de la última imagen
        print("Extracting items from last image...")
        last_items = extract_items(last_image_path, model, fridge_id)

        print("Extracted Items from Last Image:", last_items)

        # Enviar `last_items` al backend
        backend_url = "http://127.0.0.1:5001/items/add_batch"
        backend_response = requests.post(backend_url, json={"items": last_items})
        if backend_response.status_code != 200:
            return jsonify({
                'error': 'Error al enviar los datos al backend',
                'details': backend_response.text
            }), backend_response.status_code

        return jsonify({
            'status': 'success',
            'last_items': last_items
        })

    except Exception as e:
        return jsonify({'error': 'Error processing images', 'details': str(e)}), 500


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
