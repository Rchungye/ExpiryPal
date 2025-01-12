from flask import Flask, request, render_template, jsonify, send_from_directory
from ultralytics import YOLO
import os
import cv2
from sklearn.metrics.pairwise import cosine_similarity
from transformers import CLIPProcessor, CLIPModel
import torch
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'results'

# Configure Cloudinary
cloudinary.config(
    cloud_name='dqwutjyjh',
    api_key='132533594763411',
    api_secret='cW4iHQs41fcqnnOFGSyDKVQJel8'
)

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


# Function to upload image to Cloudinary
def upload_to_cloudinary(file_path, folder_name):
    response = cloudinary.uploader.upload(file_path, folder=folder_name)
    return response['secure_url']


# Function to extract objects/items from the image
def extract_items(image_path, output_folder, model):
    img = cv2.imread(image_path)
    img_contrast = enhance_contrast(img)
    results = model(img_contrast)
    os.makedirs(output_folder, exist_ok=True)

    items = []
    for i, box in enumerate(results[0].boxes):
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        class_id = int(box.cls)
        class_name = results[0].names[class_id]

        cropped_img = img[y1:y2, x1:x2]
        output_path = os.path.join(output_folder, f"{class_name}_{i+1}.jpg")
        cv2.imwrite(output_path, cropped_img)

        # Upload cropped image to Cloudinary
        cloudinary_url = upload_to_cloudinary(output_path, folder_name='cropped_items')

        features = extract_features(cropped_img)
        items.append({'name': class_name, 'features': features, 'cropped_img': output_path, 'cloudinary_url': cloudinary_url})

    return items


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
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({'error': 'Both images are required!'}), 400

    image1 = request.files['image1']
    image2 = request.files['image2']

    if image1.filename == '' or image2.filename == '':
        return jsonify({'error': 'Both images must have valid filenames!'}), 400

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    image1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image1.jpg')
    image2_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image2.jpg')

    image1.save(image1_path)
    image2.save(image2_path)

    # Create result folders for added and removed items
    added_folder = os.path.join(app.config['RESULT_FOLDER'], 'added')
    removed_folder = os.path.join(app.config['RESULT_FOLDER'], 'removed')
    os.makedirs(added_folder, exist_ok=True)
    os.makedirs(removed_folder, exist_ok=True)

    # Extract items from both images
    items1 = extract_items(image1_path, os.path.join(app.config['RESULT_FOLDER'], 'image1'), model)
    items2 = extract_items(image2_path, os.path.join(app.config['RESULT_FOLDER'], 'image2'), model)

    added_items, removed_items = compare_items(items1, items2)

    # Save added items in the "added" folder
    for i, item in enumerate(added_items):
        output_path = os.path.join(added_folder, f"{item['name']}_{i+1}.jpg")
        cropped_img_path = item['cropped_img']
        cropped_img = cv2.imread(cropped_img_path)
        cv2.imwrite(output_path, cropped_img)
        item['cloudinary_url'] = upload_to_cloudinary(output_path, folder_name='added_items')

    # Save removed items in the "removed" folder
    for i, item in enumerate(removed_items):
        output_path = os.path.join(removed_folder, f"{item['name']}_{i+1}.jpg")
        cropped_img_path = item['cropped_img']
        cropped_img = cv2.imread(cropped_img_path)
        cv2.imwrite(output_path, cropped_img)
        item['cloudinary_url'] = upload_to_cloudinary(output_path, folder_name='removed_items')

    # Return paths to display images on the web
    added_images = [item['cloudinary_url'] for item in added_items]
    removed_images = [item['cloudinary_url'] for item in removed_items]
    available_items = [item['cloudinary_url'] for item in items2]

    return jsonify({
        'added_items': [item['name'] for item in added_items],
        'removed_items': [item['name'] for item in removed_items],
        'added_images': added_images,
        'removed_images': removed_images,
        'available_items': available_items
    })


@app.route('/results/<folder>/<filename>')
def serve_result(folder, filename):
    return send_from_directory(os.path.join(app.config['RESULT_FOLDER'], folder), filename)


if __name__ == '__main__':
    app.run(debug=True)
