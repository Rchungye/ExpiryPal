from flask import request, jsonify, render_template, send_from_directory
import os
import cv2
from utils import extract_items
from comparison import compare_items

def register_routes(app, model, clip_model, clip_processor):
    
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
        items1 = extract_items(image1_path, os.path.join(app.config['RESULT_FOLDER'], 'image1'), model, clip_model, clip_processor)
        items2 = extract_items(image2_path, os.path.join(app.config['RESULT_FOLDER'], 'image2'), model, clip_model, clip_processor)

        added_items, removed_items = compare_items(items1, items2)

        # Save added items in the "added" folder
        for i, item in enumerate(added_items):
            output_path = os.path.join(added_folder, f"{item['name']}_{i+1}.jpg")
            cropped_img_path = item['cropped_img']
            cropped_img = cv2.imread(cropped_img_path)
            cv2.imwrite(output_path, cropped_img)

        # Save removed items in the "removed" folder
        for i, item in enumerate(removed_items):
            output_path = os.path.join(removed_folder, f"{item['name']}_{i+1}.jpg")
            cropped_img_path = item['cropped_img']
            cropped_img = cv2.imread(cropped_img_path)
            cv2.imwrite(output_path, cropped_img)

        # Return paths to display images on the web
        added_images = [os.path.join('results', 'added', f"{item['name']}_{i+1}.jpg") for i, item in enumerate(added_items)]
        removed_images = [os.path.join('results', 'removed', f"{item['name']}_{i+1}.jpg") for i, item in enumerate(removed_items)]
        available_items = [os.path.join('results', 'image2', f"{item['name']}_{i+1}.jpg") for i, item in enumerate(items2)]

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
