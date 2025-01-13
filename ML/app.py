from io import BytesIO
import shutil
from flask import Flask, request, render_template, jsonify, send_from_directory
from ultralytics import YOLO
import os
from dotenv import load_dotenv
load_dotenv()
import cv2
from sklearn.metrics.pairwise import cosine_similarity
from transformers import CLIPProcessor, CLIPModel
import torch
import cloudinary
import requests
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import numpy as np
import tempfile
import uuid


# Configuration       
cloudinary.config( 
    CLOUD_NAME= os.getenv("CLOUDINARY_CLOUD_NAME"),
    API_KEY= os.getenv("CLOUDINARY_API_KEY"),
    API_SECRET= os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

BE_URL = os.getenv("BE_URL")

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

alpha = 3.0
beta = 30.0

def extract_items(image_path, model):
    img = cv2.imread(image_path)  # Read the image in color (default)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))  # Adjust clipLimit and tileGridSize as needed
    img_clahe = clahe.apply(img_gray)  # Apply CLAHE to the grayscale image

    # Convert the CLAHE-enhanced grayscale image to 3-channel format (RGB)
    img_clahe_rgb = cv2.cvtColor(img_clahe, cv2.COLOR_GRAY2BGR)  # Convert to RGB (3 channels)

    #Enhance contrast on the CLAHE image
    img_contrast = enhance_contrast(img_clahe_rgb, alpha, beta)

    # Pass the enhanced image to the YOLO model
    results = model(img_contrast)
    #os.makedirs(output_folder, exist_ok=True)

    items = []
    for i, box in enumerate(results[0].boxes):
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        class_id = int(box.cls)
        class_name = results[0].names[class_id]

        # Crop the CLAHE-enhanced grayscale image
        cropped_img = img_clahe[y1:y2, x1:x2]
        #output_path = os.path.join(output_folder, f"{class_name}{i+1}.jpg")
       # cv2.imwrite(output_path, cropped_img)

        # Extract CLIP features
        features = extract_features(cropped_img)

        _, img_encoded = cv2.imencode('.jpg', cropped_img)
        if img_encoded is None:
            raise ValueError(f"Failed to encode cropped image for item {class_name}.")

        # Convert encoded image to BytesIO
        image_bytes = BytesIO(img_encoded.tobytes())
        image_bytes.seek(0)  # Ensure the stream is at the beginning
        features = extract_features(cropped_img)

        items.append({
            'name': class_name,
            #path': output_path,
            'features': features,
            'image': image_bytes  # Store image for visualization
        })

      #  print(f"Saved {output_path}")

    return items



def extractitems(image_path, model):
    """
    extract items from an image and return their data
    """
    img = cv2.imread(image_path)
    img_contrast = enhance_contrast(img)
    results = model(img_contrast)

    items = []

    for i, box in enumerate(results[0].boxes):
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        class_id = int(box.cls)
        class_name = results[0].names[class_id]

        cropped_img = img[y1:y2, x1:x2]

        _, img_encoded = cv2.imencode('.jpg', cropped_img)
        if img_encoded is None:
            raise ValueError(f"Failed to encode cropped image for item {class_name}.")

        # Convert encoded image to BytesIO
        image_bytes = BytesIO(img_encoded.tobytes())
        image_bytes.seek(0)  # Ensure the stream is at the beginning
        features = extract_features(cropped_img)

        items.append({
            'name': class_name,
            'features': features,
            'image_bytes': image_bytes
        })

    return items


# def extract_items(image_path, model, fridge_id):
#     img = cv2.imread(image_path)
#     img_contrast = enhance_contrast(img)
#     results = model(img_contrast)

#     items = []
#     output_folder = f"Fridges/{fridge_id}/cropped_items"


#     for i, box in enumerate(results[0].boxes):
#         x1, y1, x2, y2 = map(int, box.xyxy[0])
#         class_id = int(box.cls)
#         class_name = results[0].names[class_id]

#         cropped_img = img[y1:y2, x1:x2]

#         output_path = os.path.join(output_folder, f"{class_name}_{i+1}.jpg")
#         cv2.imwrite(output_path, cropped_img)

#         features = extract_features(cropped_img)
#         items.append({'name': class_name, 'features': features, 'cropped_img': output_path})

#     return items


    #     # Convert cropped image to bytes for Cloudinary upload
    #     _, img_encoded = cv2.imencode('.jpg', cropped_img)
    #     image_bytes = BytesIO(img_encoded.tobytes())

    #     folder_path = f"Fridges/{fridge_id}/cropped_items"
    #     try:
    #         response = cloudinary.uploader.upload(
    #             file=image_bytes,
    #             folder=folder_path,
    #             public_id=f"{class_name}_{i+1}",
    #             tags=["cropped_item_", i+1]
    #         )
    #         items_metadata.append({
    #             "name": class_name,
    #             "image_url": response.get("url"),
    #             "fridge_id": fridge_id
    #         })
    #     except Exception as e:
    #         print(f"Error uploading fragment {class_name}_{i+1}: {e}")

    # print(f"Extracted Items Metadata: {items_metadata}")
    # return items_metadata


    

# Function to compare items between two sets
def compare_items(items1, items2, similarity_threshold=0.75):
    print("\n\n\n****************in compare_items function")
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


def download_image_from_url(url):
    """
    downloads an image from a URL and returns it as a numpy array 
    """
    response = requests.get(url)
    if response.status_code == 200:
        image_bytes = BytesIO(response.content)
        img_array = np.frombuffer(image_bytes.read(), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return img
    else:
        raise Exception(f"Error al descargar la imagen: {response.status_code}")

def upload_to_cloudinary(file, folder_name, public_id=None):
    if isinstance(file, BytesIO):
        file.seek(0)  # Ensure the BytesIO stream is at the start
    try:
        response = cloudinary.uploader.upload(
            file,
            folder=folder_name,
            public_id=public_id
        )
        return response['secure_url']
    except Exception as e:
        print(f"Error uploading to Cloudinary: {e}")
        raise


@app.route('/')
def index():
    return render_template('index_dynamic.html')

@app.route('/ml/upload_items_if_first_time', methods=['POST'])
def upload_items_if_first_time():
    """
    Upload cropped items to Cloudinary if it is the first time the fridge is being used.
    """
    data = request.json
    fridge_id = data.get('fridge_id')
    camera_id = data.get('camera_id')
    last_picture_taken_from_fridge = data.get('last_img_url')
    uploaded_items = []

    if not fridge_id or not camera_id or not last_picture_taken_from_fridge:
        return jsonify({'error': 'Missing required parameters'}), 400

    if not last_picture_taken_from_fridge or not last_picture_taken_from_fridge.startswith("http"):
        return jsonify({'error': 'Invalid last_picture_taken_from_fridge URL'}), 400
   
    
    # Download the last picture taken from the fridge
    try:
        last_img = download_image_from_url(last_picture_taken_from_fridge)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
            temp_file_name = temp_file.name
            cv2.imwrite(temp_file_name, last_img)

        print(f"Extracting items from the last image taken from the fridge...")
        items = extract_items(temp_file_name, model)
        for item in items:
            print("in for loop")
           
            public_id = str(uuid.uuid4())
            print(f"Uploading {item['name']} to Cloudinary...")
            print(item['image'])
            print(item['name'])
            print("lllolololol")
            uploaded_url = upload_to_cloudinary(
                file=item['image'],  
                folder_name=f"Fridges/{fridge_id}/cropped_items",
                public_id=public_id
            )
            print(f"\nUploaded {item['name']} to {uploaded_url}")
            uploaded_items.append({
                'name': item['name'],
                'public_id': public_id,
                'fridge_id': fridge_id,
                'image_url': uploaded_url,
            })

            print(f"\nUploaded {item['name']} to {uploaded_url}")
    except Exception as e:
        return jsonify({'error': f'Error uploading images for the first time: {str(e)}'}), 500
    
    try:
        print(f"Sending items to backend for fridge {fridge_id}")
        print(f"Items: {uploaded_items}")
        add_batch_be_url = f"{BE_URL}items/add_items"
        backend_response = requests.post(add_batch_be_url, json={"items": uploaded_items})
        if backend_response.status_code != 200:
            return jsonify({
                'error': 'Error al enviar los datos al backend',
                'details': backend_response.text
            }), backend_response.status_code
    except Exception as e:
        return jsonify({'error': f'Error sending items to backend: {str(e)}'}), 500
    
    return jsonify({'status': 'success', 'message': 'Cropped items uploaded successfully'})
            

# @app.route('/ml/extract_items', methods=['POST'])
# def extract_items():
#     """
#     Extract items from an image and return their data.
#     """
#     data = request.json
#     last_img_taken_from_fridge = data.get('last_img_taken_from_fridge')
    
def convert_ndarray_to_list(items):
    """
    Recursively converts numpy.ndarray values in a list of dictionaries to lists.
    """
    for item in items:
        for key, value in item.items():
            if isinstance(value, np.ndarray):
                item[key] = value.tolist()  # Convert ndarray to list
    return items

@app.route('/ml/compare_items_from_fridge', methods=['POST'])
def compare_items_from_fridge():
    """
    Process two images, fragment items from the last image, and send their data to the backend.
    """
    print("\n\nProcessing images and comparing items...\n")

    data = request.json
    items_in_fridge = data.get('items_in_fridge', {}).get('payload', [])    
    last_picture_taken_from_fridge = data.get('last_img_url')
    fridge_id = data.get('fridge_id')

    if not last_picture_taken_from_fridge or not isinstance(last_picture_taken_from_fridge, str):
        return jsonify({'error': 'Invalid "last_img_url"'}), 400

    if not fridge_id or not isinstance(fridge_id, int):
        return jsonify({'error': 'Invalid "fridge_id"'}), 400

    if not items_in_fridge or not isinstance(items_in_fridge, list):
        return jsonify({'error': 'Invalid "items_in_fridge"'}), 400
    
    print("parameters validated")

    try:
        last_img = download_image_from_url(last_picture_taken_from_fridge)

        if last_img is None:
            return jsonify({'error': 'Failed to download image from URL'}), 500
        print("Image downloaded from URL")

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
            temp_file_name = temp_file.name
            cv2.imwrite(temp_file_name, last_img)
        print("Image saved to temp file")

        last_items = extract_items(temp_file_name, model)

        for item in items_in_fridge:
            img = download_image_from_url(item['imageURL'])

            if img is None or not isinstance(img, np.ndarray):
                print(f"Failed to download or invalid image format for URL: {item['imageURL']}")
                continue
            
            img_contrast = enhance_contrast(img)

            if img_contrast is None or not isinstance(img_contrast, np.ndarray):
                print(f"Failed to enhance contrast for image from URL: {item['imageURL']}")
                continue
                        
            _, img_encoded = cv2.imencode('.jpg', img_contrast)

            image_bytes = BytesIO(img_encoded.tobytes())
            image_bytes.seek(0)  

            img_array = np.frombuffer(image_bytes.read(), np.uint8)
            image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if image is None or not isinstance(image, np.ndarray):
                print(f"Failed to decode image for item {item['name']}")
                continue

            print(f"Extracting features for item {item['name']}...")
            item['features'] = extract_features(image)

        print("Items extracted from the fridge and last image")
        print("Comparing items...")
        print(f"number of items in fridge: {len(items_in_fridge)}")
        print(f"number of items in last image: {len(last_items)}")
        added_items, removed_items = compare_items(items_in_fridge, last_items)

        print(f"Added items: {len(added_items)}")
        print(f"Removed items: {len(removed_items)}")   

        # Upload images of added items to Cloudinary and replace the image bytes with URLs
        for item in added_items:
            item["fridge_id"] = fridge_id
            image_bytes = item.pop('image', None)
            if image_bytes:
                try:
                    public_id = str(uuid.uuid4())
                    uploaded_url = upload_to_cloudinary(
                        file=image_bytes,
                        folder_name=f"Fridges/{fridge_id}/added_items",
                        public_id=public_id
                    )
                    item['image_url'] = uploaded_url
                    print(f"Uploaded image for item {item['name']} to {uploaded_url}")
                except Exception as e:
                    print(f"Error uploading image for item {item['name']}: {e}")
                    continue

        for item in removed_items:
            item["fridge_id"] = fridge_id
            item.pop('features', None)  # Remove 'features' key
        
        for item in added_items:
            item.pop('features', None)  # Remove 'features' key


        print("after for loop")
        if added_items:
            print("\n\nAdding items to the backend...")
            add_items_url = f"{BE_URL}items/add_items"
            print("be url: ", add_items_url) 
            print("added items: ", added_items)
            payload = {"items": added_items}
            response = requests.post(add_items_url, json=payload)  
            print("response: ", response) 
            if response.status_code != 200:
                print(f"Error adding items: {response.text}")
            else:
                print(f"Added items successfully: {response.json()}")

        if removed_items:
            print("\n\nRemoving items from the backend...")
            for item in removed_items:
                item_id = item.get("id")
                if not item_id:
                    print(f"Missing item_id for item: {item}")
                    continue

                delete_item_url = f"{BE_URL}/items/{item_id}"
                print(f"Deleting item {item_id} from the backend...")
                print("delete url: ", delete_item_url)
                response = requests.delete(delete_item_url)
                print("response: ", response)
                if response.status_code != 200:
                    print(f"Error deleting item {item_id}: {response.text}")
                else:
                    print(f"Deleted item {item_id} successfully.")
        return jsonify({
                    'status': 'success',
                    'added_items': added_items,
                    'removed_items': removed_items
                }), 200

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
