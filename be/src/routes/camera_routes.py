from flask import Blueprint, request
from models import db, Camera
from models import ma

camera_routes = Blueprint('camera_routes', __name__)

class CameraSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'fridge_id', 'brand', 'model', 'accessURL')

camera_schema = CameraSchema()
cameras_schema = CameraSchema(many=True)

@camera_routes.route('/cameras', methods=['POST'])
def add_camera():
    data = request.json
    if not all(key in data for key in ['fridge_id', 'brand', 'model', 'accessURL']):
        return {"error": "Missing required fields"}, 400

    model = data['model']
    brand = data['brand']
    fridge_id = data['fridge_id']
    accessURL = data['accessURL']

    new_camera = Camera()
    new_camera.model = model
    new_camera.brand = brand
    new_camera.fridge_id = fridge_id
    new_camera.accessURL = accessURL

    db.session.add(new_camera)
    db.session.commit()
    return camera_schema.dump(new_camera), 201



@camera_routes.route('/cameras', methods=['GET'])
def get_cameras():
    all_cameras = Camera.query.all()
    result = cameras_schema.dump(all_cameras) 
    return {"cameras": result}, 200