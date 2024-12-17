from flask import request, jsonify, render_template, send_from_directory
import os
import shutil
from utils import extract_items, upload_to_cloudinary, download_image
from comparison import compare_items

def register_routes(app, model, clip_model, clip_processor):
    
    @app.route('/')
    def index():
        return render_template('index_dynamic.html')

    @app.route('/upload', methods=['POST'])
    def upload():
        data = request.json
        previous_img_url = data.get('previous_img_url')
        last_img_url = data.get('last_img_url')
        fridge_id = data.get('fridge_id')

        if not last_img_url or not isinstance(last_img_url, str):
            return jsonify({'error': 'Invalid "last_img_url"'}), 400

        if not fridge_id or not isinstance(fridge_id, int):
            return jsonify({'error': 'Invalid "fridge_id"'}), 400

        try:
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            last_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'last_image.jpg')

            # Download the last image
            download_image(last_img_url, last_image_path)

            # Extract items from the last image
            last_items = extract_items(last_image_path, model, fridge_id, clip_model, clip_processor)

            backend_url = "http://127.0.0.1:5001/items/add_batch"
            backend_response = requests.post(backend_url, json={"items": last_items})
            if backend_response.status_code != 200:
                return jsonify({
                    'error': 'Error sending data to backend',
                    'details': backend_response.text
                }), backend_response.status_code

            return jsonify({
                'status': 'success',
                'last_items': last_items
            })

        except Exception as e:
            return jsonify({'error': 'Error processing images', 'details': str(e)}), 500

    @app.after_request
    def cleanup_temp_files(response):
        if os.path.exists(app.config['UPLOAD_FOLDER']):
            shutil.rmtree(app.config['UPLOAD_FOLDER'])
        return response

    @app.route('/results/<folder>/<filename>')
    def serve_result(folder, filename):
        return send_from_directory(os.path.join(app.config['RESULT_FOLDER'], folder), filename)
